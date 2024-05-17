# pylint: disable=protected-access,redefined-outer-name
"""Test backup_source setup process."""
import pytest
from pytest_homeassistant_custom_component.common import assert_setup_component

from custom_components.backup_source import DOMAIN, BackupSourceEntity, async_setup
from homeassistant.const import CONF_PLATFORM, STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.core import HomeAssistant, State
from homeassistant.setup import async_setup_component

from tests.const import TEST_CONFIG


async def async_setup_test_entities(hass: HomeAssistant):
    """Mock test entities."""
    with assert_setup_component(2, "sensor"):
        assert await async_setup_component(
            hass,
            "sensor",
            {
                "sensor": [
                    TEST_CONFIG,
                    {
                        CONF_PLATFORM: "template",
                        "sensors": {
                            "test_monitored": {
                                "value_template": "{{ 20 }}",
                            },
                            "test_unavailable": {
                                "value_template": "{{ 10 }}",
                                "availability_template": "{{ False }}",
                            },
                        },
                    },
                ],
            },
        )
    await hass.async_block_till_done()


async def test_async_setup(hass: HomeAssistant, caplog):
    """Test component setup."""
    assert hass.data.get(DOMAIN) is None
    assert len(caplog.records) == 0

    await async_setup(hass, TEST_CONFIG)

    assert hass.data.get(DOMAIN) is not None
    assert len(caplog.records) == 1


async def test_async_setup_entity(hass: HomeAssistant):
    """Test entity setup."""
    entity = BackupSourceEntity(hass, TEST_CONFIG)

    assert entity.unique_id == "test_id"
    assert entity.name == "test"
    assert entity.sources == ["sensor.test_monitored"]
    assert entity.skip_no_value is True
    assert entity.state is STATE_UNAVAILABLE


@pytest.mark.parametrize(
    "state, expected",
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
async def test__has_state(hass: HomeAssistant, state, expected):
    """Test BackupSourceEntity._has_state method."""
    entity = BackupSourceEntity(hass, TEST_CONFIG)

    assert entity._has_state(State("sensor.test", state)) == expected


async def test__async_update(hass: HomeAssistant, caplog):
    """Test BackupSourceEntity.async_update method."""
    await async_setup_test_entities(hass)

    entity = BackupSourceEntity(hass, TEST_CONFIG)

    hass.states.async_set("sensor.test_monitored", 123)
    await hass.async_block_till_done()

    caplog.clear()
    await entity.async_update()
    assert len(caplog.records) == 1
    assert "Processing entity" in caplog.text
    assert entity.state == "123"
    assert entity.extra_state_attributes == {"source": "sensor.test_monitored"}

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
