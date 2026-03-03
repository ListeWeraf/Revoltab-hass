from homeassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN


class ConfigFlow(config_entry_oauth2_flow.AbstractOAuth2FlowHandler):
    """Handle OAuth2 flow for Revoltab."""

    DOMAIN = DOMAIN

    async def async_oauth_create_entry(self, data):
        return self.async_create_entry(
            title="Revoltab",
            data=data,
        )