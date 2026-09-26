from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import BASE_DIR, get_settings
from app.exceptions.base import FileValidationError

ALLOWED_CATEGORIES = {
    "certificate",
    "academic_document",
    "project_document",
    "professional_credential",
    "portfolio_file",
    "photograph",
}

ALLOWED_EXTENSIONS = {
    ".pdf": {"application/pdf"},
    ".jpg": {"image/jpeg"},
    ".jpeg": {"image/jpeg"},
    ".png": {"image/png"},
    ".webp": {"image/webp"},
    ".doc": {"application/msword"},
    ".docx": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
}

MAX_FILE_SIZE = 10 * 1024 * 1024


def get_upload_root() -> Path:
    settings = get_settings()
    root = (BASE_DIR.parent / settings.upload_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


def _signature_matches(extension: str, content: bytes) -> bool:
    if extension == ".pdf":
        return content.startswith(b"%PDF-")
    if extension in {".jpg", ".jpeg"}:
        return content.startswith(b"\xff\xd8\xff")
    if extension == ".png":
        return content.startswith(b"\x89PNG\r\n\x1a\n")
    if extension == ".webp":
        return len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WEBP"
    if extension == ".doc":
        return content.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1")
    if extension == ".docx":
        return content.startswith(b"PK\x03\x04")
    return False


async def save_upload(upload: UploadFile, category: str) -> tuple[str, str, int, str]:
    if category not in ALLOWED_CATEGORIES:
        raise FileValidationError("Invalid document category.")

    original_filename = Path(upload.filename or "").name
    if not original_filename:
        raise FileValidationError("A filename is required.")

    extension = Path(original_filename).suffix.lower()
    allowed_mimes = ALLOWED_EXTENSIONS.get(extension)
    if allowed_mimes is None:
        raise FileValidationError("This file type is not allowed.")

    if upload.content_type not in allowed_mimes:
        raise FileValidationError("The file type does not match its extension.")

    content = await upload.read(MAX_FILE_SIZE + 1)
    if not content:
        raise FileValidationError("The uploaded file is empty.")
    if len(content) > MAX_FILE_SIZE:
        raise FileValidationError("The file exceeds the 10 MB size limit.")
    if not _signature_matches(extension, content):
        raise FileValidationError("The uploaded file content is invalid.")

    stored_filename = f"{uuid4().hex}{extension}"
    category_dir = get_upload_root() / category
    category_dir.mkdir(parents=True, exist_ok=True)
    target = (category_dir / stored_filename).resolve()

    if get_upload_root() not in target.parents:
        raise FileValidationError("Invalid file destination.")

    target.write_bytes(content)
    relative_path = target.relative_to(BASE_DIR.parent).as_posix()
    return original_filename, stored_filename, len(content), relative_path


def delete_stored_file(relative_path: str) -> None:
    root = BASE_DIR.parent.resolve()
    target = (BASE_DIR.parent / relative_path).resolve()
    if root not in target.parents:
        return
    if target.is_file():
        target.unlink()
