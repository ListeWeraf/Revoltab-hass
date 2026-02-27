import aiohttp
import asyncio

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
            result = await resp.json()
            self._token = result["access_token"]

    async def discover_device(self):
        url = f"{API_BASE}/accounts"

        headers = {"Authorization": f"Bearer {self._token}"}

        async with self._session.get(url, headers=headers) as resp:
            accounts = await resp.json()

        self._account_id = accounts[0]["accountId"]

        url = f"{API_BASE}/accounts/{self._account_id}/devices"
        async with self._session.get(url, headers=headers) as resp:
            devices = await resp.json()

        self._device_id = devices[0]["deviceId"]

    async def async_setup(self):
        await self.login()
        await self.discover_device()

    async def send(self, attr_id, value):
        url = f"{API_BASE}/accounts/{self._account_id}/devices/{self._device_id}/requests"

        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }

        payload = [{
            "type": "attribute_write",
            "attrId": attr_id,
            "value": str(value),
        }]

        async with self._session.post(url, json=payload, headers=headers) as resp:
            if resp.status == 401:
                await self.login()
                return await self.send(attr_id, value)
