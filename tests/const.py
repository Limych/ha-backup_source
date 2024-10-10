"""Constants for tests."""

from typing import Final

from homeassistant.const import CONF_NAME, CONF_PLATFORM, CONF_UNIQUE_ID

from custom_components.backup_source import CONF_SKIP_NO_VALUE, CONF_SOURCES, DOMAIN

# Mock config data to be used across multiple tests
TEST_CONFIG: Final = {
    CONF_PLATFORM: DOMAIN,
    CONF_UNIQUE_ID: "test_id",
    CONF_NAME: "test",
    CONF_SKIP_NO_VALUE: True,
    CONF_SOURCES: ["sensor.test_monitored"],
}
