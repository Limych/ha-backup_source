#  Copyright (c) 2022-2024, Andrey "Limych" Khrolenok <andrey@khrolenok.ru>
#  Creative Commons BY-NC-SA 4.0 International Public License
#  (see LICENSE.md or https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""
Custom integration to integrate backup_source with Home Assistant.

For more details about this integration, please refer to
https://github.com/Limych/ha-backup_source
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.components.group import expand_entity_ids
from homeassistant.components.recorder.models import LazyState  # noqa: F401
from homeassistant.const import (
    ATTR_ASSUMED_STATE,
    ATTR_ATTRIBUTION,
    ATTR_DEVICE_CLASS,
    ATTR_ENTITY_PICTURE,
    ATTR_ICON,
    ATTR_SUPPORTED_FEATURES,
    ATTR_UNIT_OF_MEASUREMENT,
    CONF_NAME,
    CONF_UNIQUE_ID,
    EVENT_HOMEASSISTANT_START,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from homeassistant.core import (
    Event,
    HomeAssistant,
    State,
    callback,
)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_state_change_event

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Mapping

    from homeassistant.helpers.typing import ConfigType, StateType

from .const import (
    ATTR_SOURCE,
    CONF_SKIP_NO_VALUE,
    CONF_SOURCES,
    DOMAIN,
    STARTUP_MESSAGE,
)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:  # noqa: ARG001
    """Set up this integration using YAML."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    return True


class BackupSourceEntity(Entity):
    """Backup Source Entity class."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, config: ConfigType) -> None:
        """Initialize the sensor."""
        self.hass = hass

        self._attr_unique_id = config.get(CONF_UNIQUE_ID)
        self._attr_name = config.get(CONF_NAME)

        self.sources = expand_entity_ids(hass, config.get(CONF_SOURCES))
        self.skip_no_value = config.get(CONF_SKIP_NO_VALUE)

        self._state = hass.states.get(self.sources[0]) or State(
            self.sources[0], STATE_UNAVAILABLE
        )

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""

        # pylint: disable=unused-argument
        @callback
        async def async_sensor_state_listener(event: Event) -> None:  # noqa: ARG001
            """Handle device state changes."""
            last_state = self._state
            await self.async_update()
            if last_state != self._state:
                self.async_schedule_update_ha_state(force_refresh=True)

        # pylint: disable=unused-argument
        @callback
        async def async_sensor_startup(event: Event) -> None:  # noqa: ARG001
            """Update template on startup."""
            async_track_state_change_event(
                self.hass, self.sources, async_sensor_state_listener
            )
            await self.async_update()
            self.async_schedule_update_ha_state()

        self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, async_sensor_startup)

    @staticmethod
    def _has_state(state: State) -> bool:
        """Return True if state has any value."""
        return state.state is not None and state.state not in [
            STATE_UNKNOWN,
            STATE_UNAVAILABLE,
            "None",
            "",
        ]

    async def async_update(self) -> None:
        """Update sensor state."""
        for entity_id in self.sources:
            _LOGGER.debug('Processing entity "%s"', entity_id)

            state = self.hass.states.get(entity_id)  # type: LazyState
            if state is None:
                _LOGGER.debug('Unable to find an entity "%s"', entity_id)
                continue
            if self.skip_no_value and not self._has_state(state):
                _LOGGER.debug('Entity "%s" has state with no value', entity_id)
                continue

            break

        # Set sensor state to last selected sensor from list of sources
        self._state = state

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._state.state != STATE_UNAVAILABLE

    @property
    def state(self) -> StateType:
        """Return the state of the entity."""
        return self._state.state

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """
        Return entity specific state attributes.

        Implemented by platform classes. Convention for attribute names
        is lowercase snake_case.
        """
        attributes = self._state.attributes.copy()
        attributes[ATTR_SOURCE] = self._state.entity_id
        return attributes

    @property
    def unit_of_measurement(self) -> str | None:
        """Return the unit of measurement of this entity, if any."""
        return self._state.attributes.get(ATTR_UNIT_OF_MEASUREMENT)

    @property
    def assumed_state(self) -> bool:
        """Return True if unable to access real state of the entity."""
        return self._state.attributes.get(ATTR_ASSUMED_STATE, False)

    @property
    def attribution(self) -> str | None:
        """Return the attribution."""
        return self._state.attributes.get(ATTR_ATTRIBUTION)

    @property
    def device_class(self) -> str | None:
        """Return the class of this device, from component DEVICE_CLASSES."""
        return self._state.attributes.get(ATTR_DEVICE_CLASS)

    @property
    def entity_picture(self) -> str | None:
        """Return the entity picture to use in the frontend, if any."""
        return self._state.attributes.get(ATTR_ENTITY_PICTURE)

    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend, if any."""
        return self._state.attributes.get(ATTR_ICON)

    @property
    def supported_features(self) -> int | None:
        """Flag supported features."""
        return self._state.attributes.get(ATTR_SUPPORTED_FEATURES)
