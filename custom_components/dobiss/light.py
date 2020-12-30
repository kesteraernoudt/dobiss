"""Support for dobiss lights."""
from datetime import timedelta

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    DOMAIN,
    SUPPORT_BRIGHTNESS,
    LightEntity,
)

from .const import DOMAIN, KEY_API

import logging

from dobissapi import DobissLight, DobissAnalogOutput, DobissOutput

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up dobisslights."""

    _LOGGER.debug(f"Setting up light component of {DOMAIN}")

    dobiss = hass.data[DOMAIN][config_entry.entry_id][KEY_API].api
    # _LOGGER.warn("set up dobiss lights on {}".format(dobiss.url))

    light_entities = dobiss.get_devices_by_type(DobissLight)
    entities = []
    for d in light_entities:
        # _LOGGER.warn("set up dobiss lights on {}".format(dobiss.url))
        entities.append(HADobissLight(d))
    # wrap analog output in lights for now...
    analog_entities = dobiss.get_devices_by_type(DobissAnalogOutput)
    for d in analog_entities:
        # _LOGGER.warn("set up dobiss lights on {}".format(dobiss.url))
        entities.append(HADobissLight(d))
    if entities:
        async_add_entities(entities)


class HADobissLight(LightEntity):
    """Dobiss light device."""

    should_poll = False

    def __init__(self, dobisslight: DobissOutput):
        """Init dobiss light device."""
        super().__init__()
        self._dobisslight = dobisslight

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._dobisslight.object_id)},
            "name": self.name,
            "manufacturer": "dobiss",
        }

    @property
    def device_state_attributes(self):
        """Return supported attributes."""
        return self._dobisslight.attributes

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._dobisslight.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        self._dobisslight.remove_callback(self.async_write_ha_state)

    @property
    def brightness(self):
        """Return the brightness of the light."""
        if not self._dobisslight.dimmable:
            return None
        # dobiss works from 0-100, ha from 0-255
        return (self._dobisslight.value / 100) * 255

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._dobisslight.is_on

    async def async_turn_on(self, **kwargs):
        """Turn on or control the light."""
        # dobiss works from 0-100, ha from 0-255
        if ATTR_BRIGHTNESS in kwargs:
            kwargs[ATTR_BRIGHTNESS] = int((kwargs.get(ATTR_BRIGHTNESS) / 255) * 100)
        await self._dobisslight.turn_on(**kwargs)

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        await self._dobisslight.turn_off()

    @property
    def icon(self):
        """Return the icon to use in the frontend"""
        if isinstance(self._dobisslight, DobissAnalogOutput):
            return "mdi:hvac"
        return super().icon

    @property
    def supported_features(self):
        """Flag supported features."""
        supports = 0
        if self._dobisslight.dimmable:
            supports = SUPPORT_BRIGHTNESS
        return supports

    @property
    def name(self):
        """Return the display name of this light."""
        return self._dobisslight.name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._dobisslight.object_id