#  Copyright (c) 2022-2024, Andrey "Limych" Khrolenok <andrey@khrolenok.ru>
#  Creative Commons BY-NC-SA 4.0 International Public License
#  (see LICENSE.md or https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""Sensor platform for backup_source."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.weather import (
    ATTR_WEATHER_HUMIDITY,
    ATTR_WEATHER_OZONE,
    ATTR_WEATHER_PRECIPITATION_UNIT,
    ATTR_WEATHER_PRESSURE,
    ATTR_WEATHER_PRESSURE_UNIT,
    ATTR_WEATHER_TEMPERATURE,
    ATTR_WEATHER_TEMPERATURE_UNIT,
    ATTR_WEATHER_VISIBILITY,
    ATTR_WEATHER_VISIBILITY_UNIT,
    ATTR_WEATHER_WIND_BEARING,
    ATTR_WEATHER_WIND_SPEED,
    ATTR_WEATHER_WIND_SPEED_UNIT,
    PLATFORM_SCHEMA,
    WeatherEntity,
)

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
    async_add_entities([BackupSourceWeather(hass, config)])


class BackupSourceWeather(BackupSourceEntity, WeatherEntity):
    """Backup Source Weather class."""

    @property
    def condition(self) -> str | None:
        """Return the current condition."""
        return self._state.state

    @property
    def native_temperature(self) -> float | None:
        """Return the platform temperature in native units (i.e. not converted)."""
        return self._state.attributes.get(ATTR_WEATHER_TEMPERATURE)

    @property
    def native_temperature_unit(self) -> str | None:
        """Return the native unit of measurement for temperature."""
        return self._state.attributes.get(ATTR_WEATHER_TEMPERATURE_UNIT)

    @property
    def native_pressure(self) -> float | None:
        """Return the pressure in native units."""
        return self._state.attributes.get(ATTR_WEATHER_PRESSURE)

    @property
    def native_pressure_unit(self) -> str | None:
        """Return the native unit of measurement for pressure."""
        return self._state.attributes.get(ATTR_WEATHER_PRESSURE_UNIT)

    @property
    def humidity(self) -> float | None:
        """Return the humidity in native units."""
        return self._state.attributes.get(ATTR_WEATHER_HUMIDITY)

    @property
    def native_wind_speed(self) -> float | None:
        """Return the wind speed in native units."""
        return self._state.attributes.get(ATTR_WEATHER_WIND_SPEED)

    @property
    def native_wind_speed_unit(self) -> str | None:
        """Return the native unit of measurement for wind speed."""
        return self._state.attributes.get(ATTR_WEATHER_WIND_SPEED_UNIT)

    @property
    def wind_bearing(self) -> float | str | None:
        """Return the wind bearing."""
        return self._state.attributes.get(ATTR_WEATHER_WIND_BEARING)

    @property
    def ozone(self) -> float | None:
        """Return the ozone level."""
        return self._state.attributes.get(ATTR_WEATHER_OZONE)

    @property
    def native_visibility(self) -> float | None:
        """Return the visibility in native units."""
        return self._state.attributes.get(ATTR_WEATHER_VISIBILITY)

    @property
    def native_visibility_unit(self) -> str | None:
        """Return the native unit of measurement for visibility."""
        return self._state.attributes.get(ATTR_WEATHER_VISIBILITY_UNIT)

    @property
    def native_precipitation_unit(self) -> str | None:
        """Return the native unit of measurement for accumulated precipitation."""
        return self._state.attributes.get(ATTR_WEATHER_PRECIPITATION_UNIT)
