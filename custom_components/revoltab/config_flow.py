from homeassistant import config_entries
from homeassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN, CLIENT_ID, SCOPES


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        return await self.async_step_oauth2()

    async def async_step_oauth2(self, user_input=None):
        return await config_entry_oauth2_flow.async_oauth2_flow(
            self,
            OAUTH2_AUTHORIZE,
            OAUTH2_TOKEN,
            CLIENT_ID,
            None,
            SCOPES,
        )