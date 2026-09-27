import hashlib
import secrets
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from urllib.parse import quote

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import get_settings
from app.core.security import hash_password
from app.exceptions.auth import AuthenticationError
from app.models.password_reset import PasswordResetToken
from app.repositories.password_reset import PasswordResetRepository
from app.repositories.user import UserRepository


class PasswordResetService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)
        self.tokens = PasswordResetRepository(session)

    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    async def request_reset(self, email: str) -> None:
        settings = get_settings()
        user = await self.users.get_by_email(email)
        now = datetime.now(timezone.utc)

        # Always perform the same high-level operation regardless of whether
        # the account exists to avoid account enumeration through the response.
        if user is None or not user.is_active:
            return

        await self.tokens.invalidate_for_user(user.id, now)
        raw_token = secrets.token_urlsafe(48)
        reset_token = PasswordResetToken(
            user_id=user.id,
            token_hash=self._hash_token(raw_token),
            expires_at=now + timedelta(minutes=settings.password_reset_expire_minutes),
        )
        await self.tokens.add(reset_token)
        await self.session.flush()

        reset_url = (
            f"{settings.app_base_url.rstrip('/')}/auth/reset-password?token={quote(raw_token)}"
        )
        try:
            if settings.smtp_host:
                self._deliver_reset_email(user.email, reset_url)
            elif settings.debug:
                print(f"[Headhunter] Password reset link for {user.email}: {reset_url}")
            else:
                raise RuntimeError("SMTP is not configured for password reset emails.")
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    @staticmethod
    def _deliver_reset_email(email: str, reset_url: str) -> None:
        settings = get_settings()
        if not settings.smtp_host:
            if settings.debug:
                return
            raise RuntimeError("SMTP is not configured for password reset emails.")

        message = EmailMessage()
        message["Subject"] = "Reset your Headhunter password"
        message["From"] = settings.smtp_from_email
        message["To"] = email
        message.set_content(
            "You requested a Headhunter password reset.\n\n"
            f"Use this link within {settings.password_reset_expire_minutes} minutes:\n"
            f"{reset_url}\n\n"
            "If you did not request this, you can safely ignore this email."
        )

        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as smtp:
            if settings.smtp_use_tls:
                smtp.starttls()
            if settings.smtp_username:
                smtp.login(settings.smtp_username, settings.smtp_password)
            smtp.send_message(message)

    async def reset_password(self, raw_token: str, new_password: str) -> None:
        settings = get_settings()
        now = datetime.now(timezone.utc)
        token = await self.tokens.get_valid(self._hash_token(raw_token), now)
        if token is None:
            raise AuthenticationError("This password reset link is invalid or expired.")

        user = await self.users.get_by_id(token.user_id)
        if user is None or not user.is_active:
            raise AuthenticationError("This password reset link is invalid or expired.")

        user.password_hash = hash_password(new_password)
        user.updated_at = now
        token.used_at = now
        await self.tokens.invalidate_for_user(user.id, now)
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise


class PasswordChangeService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.users = UserRepository(session)

    async def change_password(self, user_id: int, current_password: str, new_password: str) -> None:
        user = await self.users.get_by_id(user_id)
        if user is None or not user.is_active:
            raise AuthenticationError("Authentication required.")
        from app.core.security import verify_password
        if not verify_password(current_password, user.password_hash):
            raise AuthenticationError("Current password is incorrect.")
        user.password_hash = hash_password(new_password)
        user.updated_at = datetime.now(timezone.utc)
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
