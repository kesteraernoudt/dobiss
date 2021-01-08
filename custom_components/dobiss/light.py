"""Support for dobiss lights."""
import logging

from dobissapi import DobissAnalogOutput
from dobissapi import DobissLight
from dobissapi import DobissOutput
from homeassistant.components.light import ATTR_BRIGHTNESS
from homeassistant.components.light import LightEntity
from homeassistant.components.light import SUPPORT_BRIGHTNESS
from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.const import ENTITY_MATCH_ALL
from homeassistant.const import ENTITY_MATCH_NONE
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN
from .const import KEY_API

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
        self.async_on_remove(
            async_dispatcher_connect(self.hass, DOMAIN, self.signal_handler)
        )

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        self._dobisslight.remove_callback(self.async_write_ha_state)

    async def signal_handler(self, data):
        """Handle domain-specific signal by calling appropriate method."""
        entity_ids = data[ATTR_ENTITY_ID]

        if entity_ids == ENTITY_MATCH_NONE:
            return

        if entity_ids == ENTITY_MATCH_ALL or self.entity_id in entity_ids:
            params = {
                key: value
                for key, value in data.items()
                if key not in ["entity_id", "method"]
            }
            await getattr(self, data["method"])(**params)

    async def turn_on_service(self, brightness=None, delayon=None, delayoff=None):
        await self._dobisslight.turn_on(
            brightness=brightness, delayon=delayon, delayoff=delayoff
        )

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
        brightness = 100
        if ATTR_BRIGHTNESS in kwargs:
            brightness = int((kwargs.get(ATTR_BRIGHTNESS) / 255) * 100)
        await self._dobisslight.turn_on(brightness)

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
