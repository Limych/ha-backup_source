# pylint: disable=protected-access,redefined-outer-name
"""Test backup_source setup process."""

from homeassistant.core import HomeAssistant

from custom_components.backup_source import DOMAIN, async_setup

from tests.const import MOCK_CONFIG


async def test_async_setup(hass: HomeAssistant, caplog):
    """Test component setup."""
    assert hass.data.get(DOMAIN) is None
    assert len(caplog.records) == 0

    await async_setup(hass, MOCK_CONFIG)

    assert hass.data.get(DOMAIN) is not None
    assert len(caplog.records) == 1
