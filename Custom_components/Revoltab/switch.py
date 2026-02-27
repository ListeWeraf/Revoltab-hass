from homeassistant.components.switch import SwitchEntity
from .const import ATTR_POWER

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data["revoltab"][entry.entry_id]
    async_add_entities([RevoltabSwitch(coordinator)])

class RevoltabSwitch(SwitchEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._is_on = False

    @property
    def name(self):
        return "Revoltab Diffusor"

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        await self.coordinator.api.send(ATTR_POWER, 1)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self.coordinator.api.send(ATTR_POWER, 0)
        self._is_on = False
        self.async_write_ha_state()
