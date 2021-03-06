# pylint: disable=protected-access,redefined-outer-name
"""Test backup_source setup process."""
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant

from custom_components.backup_source.sensor import async_setup_platform

from .const import MOCK_CONFIG


async def test_async_setup_platform(hass: HomeAssistant):
    """Test platform setup."""
    async_add_entities = MagicMock()

    await async_setup_platform(hass, MOCK_CONFIG, async_add_entities, None)
    assert async_add_entities.called
