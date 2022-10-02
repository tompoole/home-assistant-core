"""KSTAR Sensor Platform."""

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

__LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the KSTAR sensor platform."""

    __LOGGER.info("Creating KSTAR sensors")

    kstar = hass.data[DOMAIN][entry.entry_id]["data"]

    entities: list[KstarSensor] = []

    entities.append(KstarSensor(kstar))

    async_add_entities(entities, True)


class KstarSensor(SensorEntity):
    """Represents a KSTAR Inverter Entity."""

    def __init__(self, kstar) -> None:
        """Create the KSTAR entity."""
        super().__init__()

        self._logger = logging.getLogger(__name__)
        self._kstar = kstar

        self._logger.info("Creating sensor woo!")

    @property
    def unique_id(self) -> str:
        """Return unique ID."""
        return "entity_name"

    @property
    def name(self) -> str:
        """Return entity name."""
        return "Entity Name"

    @property
    def native_value(self):
        """Return native value."""
        return self._kstar.some_value

    def update(self) -> None:
        """Perform sensor update."""
        self._logger.info("Updating sensor value...!")
