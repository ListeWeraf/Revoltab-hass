from .const import DOMAIN
from .api import RevoltabAPI
from .coordinator import RevoltabCoordinator

PLATFORMS = ["switch", "fan"]

async def async_setup_entry(hass, entry):
    api = RevoltabAPI(
        entry.data["email"],
        entry.data["password"]
    )

    await api.async_setup()

    coordinator = RevoltabCoordinator(hass, api)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True
