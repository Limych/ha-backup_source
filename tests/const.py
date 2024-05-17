"""Constants for tests."""
from typing import Final

from homeassistant.const import CONF_NAME, CONF_PLATFORM

from custom_components.backup_source import DOMAIN, CONF_SOURCES

# Mock config data to be used across multiple tests
MOCK_CONFIG: Final = {
    CONF_PLATFORM: DOMAIN,
    CONF_NAME: "test",
    CONF_SOURCES: ["sensor.test_monitored"],
}
