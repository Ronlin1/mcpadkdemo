import os
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

ROOT = Path(__file__).resolve().parents[1]


def load_workspace_token(token_file: str) -> Credentials:
    path = ROOT / token_file
    if not path.exists():
        raise RuntimeError(
            f"Missing {path}. Run: python -m speakerops.oauth_login"
        )

    creds = Credentials.from_authorized_user_file(path)

    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            path.write_text(creds.to_json(), encoding="utf-8")
        else:
            raise RuntimeError(
                "Workspace OAuth token is invalid; re-run speakerops.oauth_login."
            )

    return creds


async def workspace_headers(context):
    token_file = os.getenv("WORKSPACE_TOKEN_FILE", ".workspace_token.json")
    creds = load_workspace_token(token_file)
    return {"Authorization": f"Bearer {creds.token}"}
