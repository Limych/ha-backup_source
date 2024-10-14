# pylint: disable=protected-access,redefined-outer-name
"""Test backup_source binary_sensor setup process."""

from unittest.mock import MagicMock

import pytest
from homeassistant.components.binary_sensor import DOMAIN as DOMAIN_BINARY_SENSOR
from homeassistant.components.template import DOMAIN as DOMAIN_TEMPLATE
from homeassistant.const import (
    CONF_NAME,
    CONF_PLATFORM,
    CONF_SENSORS,
    CONF_UNIQUE_ID,
    CONF_VALUE_TEMPLATE,
)
from homeassistant.helpers.typing import ConfigType
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import assert_setup_component

from custom_components.backup_source import CONF_SKIP_NO_VALUE, CONF_SOURCES, DOMAIN
from custom_components.backup_source.binary_sensor import (
    BackupSourceBinarySensor,
    async_setup_platform,
)


@pytest.fixture(name="test_entities")
async def async_setup_test_entities_fixture(hass):
    """Mock test entities."""
    config = {
        DOMAIN_BINARY_SENSOR: {
            CONF_PLATFORM: DOMAIN_TEMPLATE,
            CONF_SENSORS: {
                "test_monitored": {
                    CONF_VALUE_TEMPLATE: "{{ True }}",
                },
            },
        },
    }
    with assert_setup_component(1, DOMAIN_BINARY_SENSOR):
        assert await async_setup_component(hass, DOMAIN_BINARY_SENSOR, config)
    await hass.async_block_till_done()


@pytest.fixture(name="config")
def config_fixture() -> ConfigType:
    """Return default config for tests."""
    return {
        CONF_PLATFORM: DOMAIN,
        CONF_UNIQUE_ID: "test_id",
        CONF_NAME: "test",
        CONF_SKIP_NO_VALUE: True,
        CONF_SOURCES: ["binary_sensor.test_monitored"],
    }


async def test_async_setup_platform(hass, config):
    """Test platform setup."""
    async_add_entities = MagicMock()

    await async_setup_platform(hass, config, async_add_entities, None)
    assert async_add_entities.called


async def test_binary_sensor(hass, caplog, test_entities, config):
    """Test binary_sensor entity."""
    entity = BackupSourceBinarySensor(hass, config)

    caplog.clear()
    await entity.async_update()
    assert len(caplog.records) == 1
    assert "Processing entity" in caplog.text
    assert entity.is_on
