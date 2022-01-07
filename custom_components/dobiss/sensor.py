"""Support for dobiss switchs."""
import logging

from dobissapi import DobissLightSensor
from dobissapi import DobissSensor
from dobissapi import DobissTempSensor
from homeassistant.const import DEVICE_CLASS_ILLUMINANCE
from homeassistant.const import DEVICE_CLASS_TEMPERATURE
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity

from .const import CONF_IGNORE_ZIGBEE_DEVICES
from .const import DOMAIN
from .const import KEY_API

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up dobisssensor."""

    _LOGGER.debug(f"Setting up sensor component of {DOMAIN}")
    dobiss = hass.data[DOMAIN][config_entry.entry_id][KEY_API].api
    # _LOGGER.warn("set up dobiss switch on {}".format(dobiss.url))

    entities = []
    d_entities = dobiss.get_devices_by_type(DobissTempSensor)
    for d in d_entities:
        if (
            config_entry.options.get(CONF_IGNORE_ZIGBEE_DEVICES) is not None
            and config_entry.options.get(CONF_IGNORE_ZIGBEE_DEVICES)
            and (d.address == 210 or d.address == 211)
        ):
            continue
        # _LOGGER.warn("set up dobiss temp sensor on {}".format(dobiss.host))
        entities.append(HADobissTempSensor(d))
    d_entities = dobiss.get_devices_by_type(DobissLightSensor)
    for d in d_entities:
        # _LOGGER.warn("set up dobiss light sensor on {}".format(dobiss.host))
        entities.append(HADobissLightSensor(d))
    if entities:
        async_add_entities(entities)


class HADobissSensor(Entity):
    """Dobiss ssensor device."""

    should_poll = False

    def __init__(self, dobisssensor: DobissSensor):
        """Init dobiss Switch device."""
        super().__init__()
        self._dobisssensor = dobisssensor

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._dobisssensor.object_id)},
            "name": self.name,
            "manufacturer": "dobiss",
        }

    @property
    def extra_state_attributes(self):
        """Return supported attributes."""
        return self._dobisssensor.attributes

    @property
    def available(self) -> bool:
        """Return True."""
        return True

    # leave the icon up to the device class
    #    @property
    #    def icon(self):
    #        """Return the icon to use in the frontend"""
    #        return ICON_FROM_DOBISS[self._dobisssensor.icons_id]

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._dobisssensor.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        self._dobisssensor.remove_callback(self.async_write_ha_state)

    @property
    def name(self):
        """Return the display name of this sensor."""
        return self._dobisssensor.name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._dobisssensor.object_id


class HADobissLightSensor(HADobissSensor):
    """Dobiss Light Sensor."""

    device_class = DEVICE_CLASS_ILLUMINANCE

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "lm"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._dobisssensor.value


class HADobissTempSensor(HADobissSensor):
    """Dobiss Light Sensor."""

    device_class = DEVICE_CLASS_TEMPERATURE

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return TEMP_CELSIUS

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._dobisssensor.value
