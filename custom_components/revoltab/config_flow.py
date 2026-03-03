raise Exception("CONFIG_FLOW LOADED")
import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN
from .oauth import RevoltabOAuth


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                oauth = RevoltabOAuth(self.hass)
                tokens = await oauth.login(
                    user_input["email"],
                    user_input["password"],
                )

                return self.async_create_entry(
                    title="Revoltab",
                    data=tokens,
                )

            except Exception:
                errors["base"] = "auth_failed"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("email"): str,
                vol.Required("password"): str,
            }),
            errors=errors,
        )