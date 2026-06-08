from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed
)

from .api import BakalariApi
from .const import CONF_IGNORED_GROUPS

_LOGGER = logging.getLogger(__name__)


class BakalariCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, entry):
        self.api = BakalariApi(
            entry.data["url"],
            entry.data.get(CONF_IGNORED_GROUPS, "")
        )

        super().__init__(
            hass,
            _LOGGER,
            name="bakalari",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        try:
            return await self.hass.async_add_executor_job(
                self.api.fetch_timetable
            )

        except Exception as err:
            raise UpdateFailed(str(err)) from err