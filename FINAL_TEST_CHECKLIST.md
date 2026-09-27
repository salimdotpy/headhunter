# Headhunter Final Verification Checklist

Run this checklist locally after installing requirements and applying migrations.

## Setup

```powershell
pip install -r requirements.txt
alembic upgrade head
npm install
npm run build:css
```

## Automated tests

```powershell
pytest -q
```

## Authentication

- Register with full name, email, password, confirmation.
- Reject duplicate email.
- Reject mismatched passwords.
- Login with valid credentials.
- Reject invalid credentials.
- Logout successfully.
- Accessing protected routes while logged out redirects to login.
- Change password with the current password.
- Reject an incorrect current password.
- Request password reset with an existing and non-existing email; response should not reveal whether an account exists.
- Use a valid reset link once.
- Verify expired/used reset links are rejected.

## Ownership and authorization

- User A cannot edit/delete User B's CV records.
- User A cannot download User B's documents.
- User A cannot access User B's private portfolio data.
- Normal users cannot access `/admin/*`.
- Inactive accounts cannot authenticate or expose public portfolios.

## CV builder

- Education CRUD.
- Experience CRUD.
- Skills CRUD.
- Certification CRUD.
- Project CRUD.

## Documents

- Upload every supported category.
- Reject unsupported extensions.
- Reject mismatched MIME types.
- Reject invalid file signatures.
- Reject files over 10 MB.
- Download own documents.
- Delete own documents.
- Confirm deleted files are removed from storage.

## Portfolio

- Preview portfolio.
- Publish portfolio.
- Public URL works while published.
- Unpublished portfolio returns 404 publicly.
- Public contact visibility settings are respected.
- Public documents are not exposed through the uploads directory.
- Public portfolio is responsive.

## Dashboard

- Completion percentage updates.
- CV/document statistics are correct.
- Publication status is correct.
- Recent activity records changes.
- Quick actions work.

## Admin

- Admin dashboard statistics are correct.
- User search/filter works.
- Account activation/deactivation works.
- Portfolio monitoring works.
- Activity monitoring works.
- Website content management works.
- Platform settings work.

## Responsive/usability

Check desktop, tablet, and mobile widths for:

- Home
- About
- Login/register
- Dashboard
- CV forms/lists
- Documents
- Portfolio preview/public portfolio
- Admin pages

Verify clear success, error, empty, validation, and destructive-action states.
