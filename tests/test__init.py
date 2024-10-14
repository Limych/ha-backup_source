# pylint: disable=protected-access,redefined-outer-name
"""Test backup_source setup process."""

import pytest
from homeassistant.components.sensor import DOMAIN as DOMAIN_SENSOR
from homeassistant.components.template import DOMAIN as DOMAIN_TEMPLATE
from homeassistant.components.template.const import CONF_AVAILABILITY_TEMPLATE
from homeassistant.const import (
    CONF_NAME,
    CONF_PLATFORM,
    CONF_SENSORS,
    CONF_UNIQUE_ID,
    CONF_VALUE_TEMPLATE,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.core import State
from homeassistant.helpers.typing import ConfigType
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import assert_setup_component

from custom_components.backup_source import (
    CONF_SKIP_NO_VALUE,
    CONF_SOURCES,
    DOMAIN,
    BackupSourceEntity,
    async_setup,
)


@pytest.fixture(name="config")
def config_fixture() -> ConfigType:
    """Return default config for tests."""
    return {
        CONF_PLATFORM: DOMAIN,
        CONF_UNIQUE_ID: "test_id",
        CONF_NAME: "test",
        CONF_SKIP_NO_VALUE: True,
        CONF_SOURCES: ["sensor.test_monitored"],
    }


@pytest.fixture(name="test_entities")
async def async_setup_test_entities_fixture(hass):
    """Mock test entities."""
    config = {
        DOMAIN_SENSOR: {
            CONF_PLATFORM: DOMAIN_TEMPLATE,
            CONF_SENSORS: {
                "test_monitored": {
                    CONF_VALUE_TEMPLATE: "{{ 20 }}",
                },
                "test_unavailable": {
                    CONF_VALUE_TEMPLATE: "{{ 10 }}",
                    CONF_AVAILABILITY_TEMPLATE: "{{ False }}",
                },
            },
        },
    }
    with assert_setup_component(1, DOMAIN_SENSOR):
        assert await async_setup_component(hass, DOMAIN_SENSOR, config)
    await hass.async_block_till_done()


async def test_async_setup(hass, caplog, config):
    """Test component setup."""
    assert hass.data.get(DOMAIN) is None
    assert len(caplog.records) == 0

    await async_setup(hass, config)

    assert hass.data.get(DOMAIN) is not None
    assert len(caplog.records) == 1


async def test_async_setup_entity(hass, config):
    """Test entity setup."""
    entity = BackupSourceEntity(hass, config)

    assert entity.unique_id == "test_id"
    assert entity.name == "test"
    assert entity.sources == ["sensor.test_monitored"]
    assert entity.skip_no_value is True
    assert entity.state is STATE_UNAVAILABLE


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (None, False),
        ("", False),
        ("None", False),
        (STATE_UNKNOWN, False),
        (STATE_UNAVAILABLE, False),
        ("123", True),
        (456, True),
    ],
)
async def test__has_state(hass, config, state, expected):
    """Test BackupSourceEntity._has_state method."""
    entity = BackupSourceEntity(hass, config)

    assert entity._has_state(State("sensor.test", state)) == expected


async def test__async_update(hass, caplog, test_entities, config):
    """Test BackupSourceEntity.async_update method."""
    entity = BackupSourceEntity(hass, config)

    hass.states.async_set("sensor.test_monitored", 123)
    await hass.async_block_till_done()

    caplog.clear()
    await entity.async_update()
    assert len(caplog.records) == 1
    assert "Processing entity" in caplog.text
    assert entity.available
    assert entity.state == "123"
    assert entity.unit_of_measurement is None
    assert entity.assumed_state is False
    assert entity.attribution is None
    assert entity.device_class is None
    assert entity.entity_picture is None
    assert entity.extra_state_attributes == {"source": "sensor.test_monitored"}
    assert entity.icon is None
    assert entity.supported_features is None

    hass.states.async_set("sensor.test_monitored", None)
    await hass.async_block_till_done()

    caplog.clear()
    await entity.async_update()
    assert len(caplog.records) == 2
    assert "has state with no value" in caplog.text
    assert entity.state == "None"

    entity.sources = ["sensor.nonexistent"]

    caplog.clear()
    await entity.async_update()
    assert len(caplog.records) == 2
    assert "Unable to find an entity" in caplog.text
