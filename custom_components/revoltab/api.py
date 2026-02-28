import aiohttp
import asyncio
from urllib.parse import urlencode, urlparse, parse_qs

BASE_URL = "https://auth1.o80y8sax.afero.net"
REALM = "rvt"
CLIENT_ID = "rvt_ios"
REDIRECT_URI = "rvt://auth"

class RevoltabAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar())
        self.access_token = None
        self.refresh_token = None

    async def login(self):
        # 1️⃣ Authorization Request
        params = {
            "client_id": CLIENT_ID,
            "response_type": "code",
            "scope": "openid",
            "redirect_uri": REDIRECT_URI,
        }

        auth_url = f"{BASE_URL}/auth/realms/{REALM}/protocol/openid-connect/auth?{urlencode(params)}"

        async with self.session.get(auth_url, allow_redirects=True) as resp:
            text = await resp.text()

        # 2️⃣ Extract login action URL
        login_action = str(resp.url)

        # 3️⃣ Submit credentials
        payload = {
            "username": self.username,
            "password": self.password,
            "credentialId": ""
        }

        async with self.session.post(login_action, data=payload, allow_redirects=False) as resp:
            location = resp.headers.get("Location")

        if not location:
            raise Exception("Login failed – no redirect received")

        # 4️⃣ Extract authorization code
        parsed = urlparse(location)
        query = parse_qs(parsed.query)

        if "code" not in query:
            raise Exception("Authorization code not found")

        code = query["code"][0]

        # 5️⃣ Exchange code for tokens
        token_url = f"{BASE_URL}/auth/realms/{REALM}/protocol/openid-connect/token"

        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
        }

        async with self.session.post(token_url, data=token_data) as resp:
            token_json = await resp.json()

        if "access_token" not in token_json:
            raise Exception(f"Token exchange failed: {token_json}")

        self.access_token = token_json["access_token"]
        self.refresh_token = token_json["refresh_token"]

        return True

    async def refresh(self):
        token_url = f"{BASE_URL}/auth/realms/{REALM}/protocol/openid-connect/token"

        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": CLIENT_ID,
        }

        async with self.session.post(token_url, data=data) as resp:
            token_json = await resp.json()

        if "access_token" not in token_json:
            raise Exception("Refresh failed")

        self.access_token = token_json["access_token"]
        self.refresh_token = token_json["refresh_token"]

        return True

    async def close(self):
        await self.session.close()