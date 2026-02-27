from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from datetime import timedelta

class RevoltabCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api):
        super().__init__(
            hass,
            logger=None,
            name="revoltab",
            update_interval=timedelta(seconds=30),
        )
        self.api = api

    async def _async_update_data(self):
        return {}
