#  Copyright (c) 2022, Andrey "Limych" Khrolenok <andrey@khrolenok.ru>
#  Creative Commons BY-NC-SA 4.0 International Public License
#  (see LICENSE.md or https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""Sensor platform for backup_source."""
from __future__ import annotations

from homeassistant.components.weather import (
    ATTR_FORECAST,
    ATTR_WEATHER_HUMIDITY,
    ATTR_WEATHER_OZONE,
    ATTR_WEATHER_PRESSURE,
    ATTR_WEATHER_TEMPERATURE,
    ATTR_WEATHER_VISIBILITY,
    ATTR_WEATHER_WIND_BEARING,
    ATTR_WEATHER_WIND_SPEED,
    PLATFORM_SCHEMA,
    Forecast,
    WeatherEntity,
)
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
    async_add_entities([BackupSourceWeather(hass, config)])


class BackupSourceWeather(BackupSourceEntity, WeatherEntity):
    """Backup Source Weather class."""

    @property
    def condition(self):
        """Return the current condition."""
        return self._state.state

    @property
    def temperature(self):
        """Return the platform temperature in native units (i.e. not converted)."""
        return self._state.attributes.get(ATTR_WEATHER_TEMPERATURE)

    @property
    def temperature_unit(self) -> str:
        """Return the native unit of measurement for temperature."""
        return self.hass.config.units.temperature_unit

    @property
    def pressure(self):
        """Return the pressure in native units."""
        return self._state.attributes.get(ATTR_WEATHER_PRESSURE)

    @property
    def pressure_unit(self) -> str:
        """Return the native unit of measurement for pressure."""
        return self.hass.config.units.pressure_unit

    @property
    def humidity(self):
        """Return the humidity in native units."""
        return self._state.attributes.get(ATTR_WEATHER_HUMIDITY)

    @property
    def wind_speed(self):
        """Return the wind speed in native units."""
        return self._state.attributes.get(ATTR_WEATHER_WIND_SPEED)

    @property
    def wind_speed_unit(self) -> str:
        """Return the native unit of measurement for wind speed."""
        return self.hass.config.units.wind_speed_unit

    @property
    def wind_bearing(self):
        """Return the wind bearing."""
        return self._state.attributes.get(ATTR_WEATHER_WIND_BEARING)

    @property
    def ozone(self):
        """Return the ozone level."""
        return self._state.attributes.get(ATTR_WEATHER_OZONE)

    @property
    def visibility(self):
        """Return the visibility in native units."""
        return self._state.attributes.get(ATTR_WEATHER_VISIBILITY)

    @property
    def visibility_unit(self) -> str:
        """Return the native unit of measurement for visibility."""
        return self.hass.config.units.length_unit

    @property
    def forecast(self):
        """Return the forecast in native units."""
        forecast = []
        for forecast_entry in self._state.attributes.get(ATTR_FORECAST):
            forecast_entry: Forecast = forecast_entry
            forecast.append(forecast_entry)

        return forecast

    @property
    def precipitation_unit(self) -> str:
        """Return the native unit of measurement for accumulated precipitation."""
        return self.hass.config.units.accumulated_precipitation_unit
