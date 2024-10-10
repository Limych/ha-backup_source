#  Copyright (c) 2022, Andrey "Limych" Khrolenok <andrey@khrolenok.ru>
#  Creative Commons BY-NC-SA 4.0 International Public License
#  (see LICENSE.md or https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""Sensor platform for backup_source."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import PLATFORM_SCHEMA, BinarySensorEntity
from homeassistant.const import STATE_ON

if TYPE_CHECKING:
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
    discovery_info: DiscoveryInfoType | None = None,  # noqa: ARG001
) -> None:
    """Set up the backup sensor."""
    async_add_entities([BackupSourceBinarySensor(hass, config)])


class BackupSourceBinarySensor(BackupSourceEntity, BinarySensorEntity):
    """Backup Source Binary Sensor class."""

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        return self._state.state == STATE_ON
