"""Revoltab Integration for Home Assistant."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import RevoltabAuth

DOMAIN = "revoltab"

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Revoltab component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Revoltab from a config entry."""
    username = entry.data["username"]
    password = entry.data["password"]

    auth = RevoltabAuth(username, password)

    try:
        await auth.login()
    except Exception as e:
        _LOGGER.error("Login failed: %s", e)
        return False

    # Speichern der Auth-Instanz
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = auth

    _LOGGER.info("Revoltab login successful")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    auth = hass.data[DOMAIN].pop(entry.entry_id)

    await auth.close()

    return True