from homeassistant.components.fan import FanEntity
from .const import ATTR_INTENSITY

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["revoltab"][entry.entry_id]
    async_add_entities([RevoltabFan(coordinator)])

class RevoltabFan(FanEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._percentage = 0

    @property
    def name(self):
        return "Revoltab Intensität"

    @property
    def percentage(self):
        return self._percentage

    async def async_set_percentage(self, percentage):
        await self.coordinator.api.send(ATTR_INTENSITY, percentage)
        self._percentage = percentage
        self.async_write_ha_state()
