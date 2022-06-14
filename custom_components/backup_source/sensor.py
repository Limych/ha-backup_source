#  Copyright (c) 2022, Andrey "Limych" Khrolenok <andrey@khrolenok.ru>
#  Creative Commons BY-NC-SA 4.0 International Public License
#  (see LICENSE.md or https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""Sensor platform for backup_source."""
from __future__ import annotations

from homeassistant.components.sensor import (
    ATTR_LAST_RESET,
    PLATFORM_SCHEMA,
    SensorEntity,
)
from homeassistant.const import ATTR_UNIT_OF_MEASUREMENT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import BackupSourceEntity
from .const import COMMON_BACKUP_SCHEMA

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(COMMON_BACKUP_SCHEMA)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the backup sensor."""
    async_add_entities([BackupSourceSensor(hass, config)])


class BackupSourceSensor(BackupSourceEntity, SensorEntity):
    """Backup Source Sensor class."""

    @property
    def native_value(self):
        """Return the value reported by the sensor."""
        return self._state.state

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement of the sensor, if any."""
        return self._state.attributes.get(ATTR_UNIT_OF_MEASUREMENT)

    @property
    def last_reset(self):
        """Return the time when the sensor was last reset, if any."""
        return self._state.attributes.get(ATTR_LAST_RESET)
