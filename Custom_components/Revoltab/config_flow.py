import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_EMAIL, CONF_PASSWORD
from .api import RevoltabAPI

class RevoltabConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            api = RevoltabAPI(
                user_input[CONF_EMAIL],
                user_input[CONF_PASSWORD]
            )
            await api.async_setup()

            return self.async_create_entry(
                title="Revoltab",
                data=user_input
            )

        schema = vol.Schema({
            vol.Required(CONF_EMAIL): str,
            vol.Required(CONF_PASSWORD): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema)
