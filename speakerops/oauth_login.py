import os
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from dotenv import load_dotenv
from google_auth_oauthlib.flow import Flow

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

CLIENT_SECRET = ROOT / "client_secret.json"
TOKEN_FILE = ROOT / os.getenv("WORKSPACE_TOKEN_FILE", ".workspace_token.json")
REDIRECT_URI = "http://localhost:8765/oauth2callback"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/calendar",
]


class CallbackHandler(BaseHTTPRequestHandler):
    authorization_response = None

    def do_GET(self):
        CallbackHandler.authorization_response = (
            f"{REDIRECT_URI}{self.path.split('/oauth2callback', 1)[-1]}"
        )
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"OAuth complete. You can close this browser tab and return to the terminal."
        )

    def log_message(self, format, *args):
        return


def main():
    if not CLIENT_SECRET.exists():
        raise RuntimeError(
            f"Missing {CLIENT_SECRET}. Download an OAuth client JSON and save it as client_secret.json."
        )

    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRET),
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    authorization_url, _ = flow.authorization_url(
        access_type="offline",
        prompt="consent",
        include_granted_scopes="true",
    )

    print("Opening browser for Google OAuth...")
    webbrowser.open(authorization_url)

    server = HTTPServer(("localhost", 8765), CallbackHandler)
    while CallbackHandler.authorization_response is None:
        server.handle_request()

    server.server_close()

    flow.fetch_token(
        authorization_response=CallbackHandler.authorization_response
    )

    TOKEN_FILE.write_text(flow.credentials.to_json(), encoding="utf-8")
    print(f"Saved OAuth token to {TOKEN_FILE}")


if __name__ == "__main__":
    main()
