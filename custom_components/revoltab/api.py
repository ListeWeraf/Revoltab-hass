import aiohttp
import logging

from .const import AUTH_BASE, API_BASE

_LOGGER = logging.getLogger(__name__)

class RevoltabAPI:
    def __init__(self, email, password):
        self._email = email
        self._password = password
        self._token = None
        self._account_id = None
        self._device_id = None
        self._session = aiohttp.ClientSession()

    async def login(self):
        url = f"{AUTH_BASE}/auth/realms/rvt/protocol/openid-connect/token"

        data = {
            "grant_type": "password",
            "client_id": "rvt_ios",
            "username": self._email,
            "password": self._password,
        }

        async with self._session.post(url, data=data) as resp:
            text = await resp.text()

            if resp.status != 200:
                _LOGGER.error("Login failed: %s", text)
                raise Exception(f"Login failed: {resp.status}")

            result = await resp.json()
            self._token = result.get("access_token")

            if not self._token:
                raise Exception("No access token received")

    async def discover_device(self):
        headers = {"Authorization": f"Bearer {self._token}"}

        url = f"{API_BASE}/accounts"
        async with self._session.get(url, headers=headers) as resp:
            if resp.status != 200:
                raise Exception("Failed to fetch accounts")

            accounts = await resp.json()

        if not accounts:
            raise Exception("No accounts found")

        self._account_id = accounts[0]["accountId"]

        url = f"{API_BASE}/accounts/{self._account_id}/devices"
        async with self._session.get(url, headers=headers) as resp:
            if resp.status != 200:
                raise Exception("Failed to fetch devices")

            devices = await resp.json()

        if not devices:
            raise Exception("No devices found")

        self._device_id = devices[0]["deviceId"]

    async def async_setup(self):
        await self.login()
        await self.discover_device()

    async def send(self, attr_id, value):
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }

        url = f"{API_BASE}/accounts/{self._account_id}/devices/{self._device_id}/requests"

        payload = [{
            "type": "attribute_write",
            "attrId": attr_id,
            "value": str(value),
        }]

        async with self._session.post(url, json=payload, headers=headers) as resp:
            if resp.status == 401:
                await self.login()
                return await self.send(attr_id, value)

            if resp.status != 200:
                text = await resp.text()
                _LOGGER.error("Command failed: %s", text)
