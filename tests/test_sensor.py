# pylint: disable=protected-access,redefined-outer-name
"""Test backup_source setup process."""
from unittest.mock import MagicMock

from custom_components.backup_source.sensor import async_setup_platform
from homeassistant.core import HomeAssistant

from .const import TEST_CONFIG


async def test_async_setup_platform(hass: HomeAssistant):
    """Test platform setup."""
    async_add_entities = MagicMock()

    await async_setup_platform(hass, TEST_CONFIG, async_add_entities, None)
    assert async_add_entities.called
