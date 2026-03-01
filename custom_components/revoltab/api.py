from urllib.parse import urlencode, urlparse, parse_qs
from homeassistant.helpers.aiohttp_client import async_get_clientsession

BASE_URL = "https://auth1.o80y8sax.afero.net"
REALM = "rvt"
CLIENT_ID = "rvt_ios"
REDIRECT_URI = "rvt://auth"


class RevoltabAuth:
    def __init__(self, hass, username, password):
        self.hass = hass
        self.username = username
        self.password = password
        self.session = async_get_clientsession(hass)
        self.access_token = None
        self.refresh_token = None

    async def login(self):
        params = {
            "client_id": CLIENT_ID,
            "response_type": "code",
            "scope": "openid",
            "redirect_uri": REDIRECT_URI,
        }

        auth_url = (
            f"{BASE_URL}/auth/realms/{REALM}/protocol/openid-connect/auth?"
            f"{urlencode(params)}"
        )

        async with self.session.get(auth_url, allow_redirects=True) as resp:
            login_action = str(resp.url)

        payload = {
            "username": self.username,
            "password": self.password,
            "credentialId": "",
        }

        async with self.session.post(
            login_action, data=payload, allow_redirects=False
        ) as resp:
            location = resp.headers.get("Location")

        if not location:
            raise Exception("Login failed – no redirect")

        parsed = urlparse(location)
        query = parse_qs(parsed.query)

        if "code" not in query:
            raise Exception("Authorization code missing")

        code = query["code"][0]

        token_url = (
            f"{BASE_URL}/auth/realms/{REALM}/protocol/openid-connect/token"
        )

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