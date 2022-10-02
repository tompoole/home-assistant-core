"""The KStar Solar Inverter integration."""
from datetime import timedelta
import logging
from random import randint

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(seconds=10)

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up KStar Solar Inverter from a config entry."""

    _LOGGER.info("Setting up KSTAR inverter")
    _LOGGER.info("Inverter address is %s", entry.data[CONF_HOST])

    coordinator = KstarInverterDataUpdateCoordinator(hass, None, entry.entry_id)

    hass.data[DOMAIN][entry.entry_id] = {COORDINATOR: coordinator}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class KstarInverterDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the NOAA Aurora API."""

    def __init__(self, hass: HomeAssistant, api, name) -> None:
        """Initialize the data updater."""

        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=name,
            update_interval=timedelta(seconds=30),
        )

        self.api = api

    async def _async_update_data(self):
        """Fetch the data from the inverter."""

        return {"some_value": randint(1, 500)}


class KstarEntity(CoordinatorEntity[KstarInverterDataUpdateCoordinator]):
    """Implementation of the base."""

    def __init__(
        self, coordinator: KstarInverterDataUpdateCoordinator, name: str
    ) -> None:
        """Initialize the Aurora Entity."""

        super().__init__(coordinator=coordinator)

        self._attr_name = name
        self._attr_unique_id = name

    @property
    def device_info(self) -> DeviceInfo:
        """Define the device based on name."""
        return DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, str(self.unique_id))},
            manufacturer="KStar",
            model="Solar Inverter",
            name=self.coordinator.name,
        )
