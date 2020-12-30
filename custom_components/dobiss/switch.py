"""Support for dobiss switchs."""

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, KEY_API

import logging

from dobissapi import (
    DobissSwitch,
    ICON_FROM_DOBISS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up dobissswitch."""

    _LOGGER.debug(f"Setting up switch component of {DOMAIN}")
    dobiss = hass.data[DOMAIN][config_entry.entry_id][KEY_API].api
    # _LOGGER.warn(f"set up dobiss switch on {dobiss.host}")

    d_entities = dobiss.get_devices_by_type(DobissSwitch)
    entities = []
    for d in d_entities:
        # _LOGGER.warn(f"set up dobiss switch {d.name} on {dobiss.host}")
        if not d.buddy:
            entities.append(HADobissSwitch(d))
    if entities:
        async_add_entities(entities)


class HADobissSwitch(SwitchEntity):
    """Dobiss switch device."""

    should_poll = False

    def __init__(self, dobissswitch: DobissSwitch):
        """Init dobiss Switch device."""
        super().__init__()
        self._dobissswitch = dobissswitch

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._dobissswitch.object_id)},
            "name": self.name,
            "manufacturer": "dobiss",
        }

    @property
    def device_state_attributes(self):
        """Return supported attributes."""
        return self._dobissswitch.attributes

    @property
    def icon(self):
        """Return the icon to use in the frontend"""
        return ICON_FROM_DOBISS[self._dobissswitch.icons_id]

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._dobissswitch.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        self._dobissswitch.remove_callback(self.async_write_ha_state)

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._dobissswitch.is_on

    async def async_turn_on(self, **kwargs):
        """Turn on or control the switch."""
        await self._dobissswitch.turn_on(**kwargs)

    async def async_turn_off(self, **kwargs):
        """Instruct the switch to turn off."""
        await self._dobissswitch.turn_off()

    @property
    def name(self):
        """Return the display name of this switch."""
        return self._dobissswitch.name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._dobissswitch.object_id