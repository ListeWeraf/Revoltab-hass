import aiohttp
import base64
import hashlib
import os
import re
from urllib.parse import urlencode, urlparse, parse_qs

BASE_URL = "https://auth1.o80y8sax.afero.net"
REALM = "rvt"
CLIENT_ID = "rvt_ios"
REDIRECT_URI = "rvt-app://loginredirect"


def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode().rstrip("=")
    sha256 = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(sha256).decode().rstrip("=")
    return code_verifier, code_challenge


class RevoltabOAuth:

    def __init__(self, hass):
        self.hass = hass

    async def login(self, username, password):
        code_verifier, code_challenge = generate_pkce()
        state = base64.urlsafe_b64encode(os.urandom(24)).decode().rstrip("=")
        nonce = base64.urlsafe_b64encode(os.urandom(24)).decode().rstrip("=")

        params = {
            "prompt": "login",
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": "openid offline_access",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "state": state,
            "nonce": nonce,
        }

        auth_url = (
            f"{BASE_URL}/auth/realms/{REALM}/protocol/openid-connect/auth?"
            f"{urlencode(params)}"
        )

        async with aiohttp.ClientSession() as session:

            async with session.get(auth_url) as resp:
                html = await resp.text()

            match = re.search(r'action="([^"]+login-actions/authenticate[^"]+)"', html)
            if not match:
                raise Exception("Login form not found")

            login_action = match.group(1)
            if login_action.startswith("/"):
                login_action = BASE_URL + login_action

            payload = {
                "username": username,
                "password": password,
                "credentialId": "",
            }

            async with session.post(login_action, data=payload, allow_redirects=False) as resp:
                location = resp.headers.get("Location")

            if not location:
                raise Exception("No redirect")

            parsed = urlparse(location)
            query = parse_qs(parsed.query)

            if "code" not in query:
                raise Exception("No code returned")

            code = query["code"][0]

            token_url = f"{BASE_URL}/auth/realms/{REALM}/protocol/openid-connect/token"

            token_data = {
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "code_verifier": code_verifier,
            }

            async with session.post(token_url, data=token_data) as resp:
                token_json = await resp.json()

            if "access_token" not in token_json:
                raise Exception("Token exchange failed")

            return {
                "access_token": token_json["access_token"],
                "refresh_token": token_json["refresh_token"],
                "expires_in": token_json["expires_in"],
            }
