from datetime import datetime, timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .oauth import RevoltabOAuth


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})

    oauth = RevoltabOAuth(hass)

    token_data = dict(entry.data)

    expires_at = datetime.utcnow() + timedelta(
        seconds=token_data["expires_in"]
    )

    hass.data[DOMAIN][entry.entry_id] = {
        "oauth": oauth,
        "tokens": token_data,
        "expires_at": expires_at,
    }

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN].pop(entry.entry_id)
    return True