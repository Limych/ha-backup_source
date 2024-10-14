# pylint: disable=protected-access,redefined-outer-name
"""Test backup_source setup process."""

from unittest.mock import MagicMock

import pytest
from homeassistant.components.template import DOMAIN as DOMAIN_TEMPLATE
from homeassistant.components.template.weather import (
    CONF_CONDITION_TEMPLATE,
    CONF_HUMIDITY_TEMPLATE,
    CONF_TEMPERATURE_TEMPLATE,
)
from homeassistant.components.weather import DOMAIN as DOMAIN_WEATHER
from homeassistant.const import (
    CONF_NAME,
    CONF_PLATFORM,
    CONF_UNIQUE_ID,
    UnitOfLength,
    UnitOfPressure,
    UnitOfSpeed,
    UnitOfTemperature,
)
from homeassistant.helpers.typing import ConfigType
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import assert_setup_component

from custom_components.backup_source import CONF_SKIP_NO_VALUE, CONF_SOURCES, DOMAIN
from custom_components.backup_source.weather import (
    BackupSourceWeather,
    async_setup_platform,
)


@pytest.fixture(name="test_entities")
async def async_setup_test_entities_fixture(hass):
    """Mock test entities."""
    config = {
        DOMAIN_WEATHER: {
            CONF_PLATFORM: DOMAIN_TEMPLATE,
            CONF_NAME: "test_monitored",
            CONF_CONDITION_TEMPLATE: "{{ 'sunny' }}",
            CONF_TEMPERATURE_TEMPLATE: "{{ 20 }}",
            CONF_HUMIDITY_TEMPLATE: "{{ 34 }}",
        },
    }
    with assert_setup_component(1, DOMAIN_WEATHER):
        assert await async_setup_component(hass, DOMAIN_WEATHER, config)
    await hass.async_block_till_done()


@pytest.fixture(name="config")
def config_fixture() -> ConfigType:
    """Return default config for tests."""
    return {
        CONF_PLATFORM: DOMAIN,
        CONF_UNIQUE_ID: "test_id",
        CONF_NAME: "test",
        CONF_SKIP_NO_VALUE: True,
        CONF_SOURCES: ["weather.test_monitored"],
    }


async def test_async_setup_platform(hass, config):
    """Test platform setup."""
    async_add_entities = MagicMock()

    await async_setup_platform(hass, config, async_add_entities, None)
    assert async_add_entities.called


async def test_weather(hass, caplog, test_entities, config):
    """Test weather entity."""
    entity = BackupSourceWeather(hass, config)

    caplog.clear()
    await entity.async_update()
    assert len(caplog.records) == 1
    assert "Processing entity" in caplog.text
    assert entity.condition == "sunny"
    assert entity.native_temperature == 20
    assert entity.native_temperature_unit == UnitOfTemperature.CELSIUS
    assert entity.native_pressure is None
    assert entity.native_pressure_unit == UnitOfPressure.HPA
    assert entity.humidity == 34
    assert entity.native_wind_speed is None
    assert entity.native_wind_speed_unit == UnitOfSpeed.KILOMETERS_PER_HOUR
    assert entity.wind_bearing is None
    assert entity.ozone is None
    assert entity.native_visibility is None
    assert entity.native_visibility_unit == UnitOfLength.KILOMETERS
    assert entity.native_precipitation_unit == UnitOfLength.MILLIMETERS
