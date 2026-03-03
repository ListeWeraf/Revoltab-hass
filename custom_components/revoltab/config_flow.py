from homeassistant import config_entries
from homeassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN, CLIENT_ID, SCOPES


class RevoltabOAuth2Implementation(
    config_entry_oauth2_flow.LocalOAuth2Implementation
):
    """OAuth2 implementation."""

    def __init__(self, hass):
        super().__init__(
            hass,
            DOMAIN,
            CLIENT_ID,
            None,
            OAUTH2_AUTHORIZE,
            OAUTH2_TOKEN,
            SCOPES,
        )


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        implementation = RevoltabOAuth2Implementation(self.hass)

        return await config_entry_oauth2_flow.async_init(
            self.hass,
            DOMAIN,
            context={"source": self.source},
            implementation=implementation,
        )