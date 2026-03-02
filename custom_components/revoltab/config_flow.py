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


class ConfigFlow(config_entry_oauth2_flow.AbstractOAuth2FlowHandler):
    """Handle a config flow for Revoltab."""

    domain = DOMAIN

    async def async_oauth_create_entry(self, data):
        return self.async_create_entry(
            title="Revoltab",
            data=data,
        )

    async def async_step_user(self, user_input=None):
        implementation = RevoltabOAuth2Implementation(self.hass)
        return await self.async_step_oauth2(implementation)