import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD
from .api import RevoltabAuth


class RevoltabConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            auth = RevoltabAuth(
                user_input[CONF_EMAIL],
                user_input[CONF_PASSWORD],
            )

            try:
                await auth.login()

                return self.async_create_entry(
                    title="Revoltab",
                    data=user_input,
                )

            except Exception:
                errors["base"] = "cannot_connect"

            finally:
                # 🔥 GANZ WICHTIG
                await auth.close()

        schema = vol.Schema(
            {
                vol.Required(CONF_EMAIL): str,
                vol.Required(CONF_PASSWORD): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )