#  Copyright (c) 2022, Andrey "Limych" Khrolenok <andrey@khrolenok.ru>
#  Creative Commons BY-NC-SA 4.0 International Public License
#  (see LICENSE.md or https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""Constants for backup_source."""

from typing import Final

import voluptuous as vol
from homeassistant.const import CONF_NAME, CONF_UNIQUE_ID, Platform
from homeassistant.helpers import config_validation as cv

# Base component constants
NAME: Final = "Backup Source"
DOMAIN: Final = "backup_source"
VERSION: Final = "1.0.2-alpha"
ATTRIBUTION: Final = ""
ISSUE_URL: Final = "https://github.com/Limych/ha-backup_source/issues"

STARTUP_MESSAGE: Final = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have ANY issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

# Platforms
PLATFORMS: Final = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.WEATHER,
]

# Configuration and options
CONF_SOURCES: Final = "sources"
CONF_SKIP_NO_VALUE: Final = "skip_no_value"

# Attributes
ATTR_SOURCE: Final = "source"

# Common schemas
COMMON_BACKUP_SCHEMA: Final = {
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_SOURCES): cv.entity_ids,
    vol.Optional(CONF_UNIQUE_ID): cv.string,
    vol.Optional(CONF_SKIP_NO_VALUE, default=True): cv.boolean,
}
