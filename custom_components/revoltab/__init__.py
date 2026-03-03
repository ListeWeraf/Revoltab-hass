from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Revoltab."""

    session = config_entry_oauth2_flow.OAuth2Session(
        hass,
        entry,
        config_entry_oauth2_flow.async_get_config_entry_implementation(
            hass, entry
        ),
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = session

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data[DOMAIN].pop(entry.entry_id)
    return True