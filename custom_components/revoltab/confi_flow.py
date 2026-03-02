from homeassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN, CLIENT_ID, SCOPES


class RevoltabOAuth2Implementation(
    config_entry_oauth2_flow.LocalOAuth2Implementation
):
    """OAuth2 implementation for Revoltab."""

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


class RevoltabConfigFlow(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler
):
    """Config flow for Revoltab."""

    DOMAIN = DOMAIN

    async def async_oauth_create_entry(self, data):
        """Create entry after OAuth."""
        return self.async_create_entry(
            title="Revoltab",
            data=data,
        )

    async def async_step_user(self, user_input=None):
        """Start OAuth flow."""
        implementation = RevoltabOAuth2Implementation(self.hass)
        return await self.async_step_oauth2(implementation)