"""Support for dobiss climate control."""
from datetime import timedelta

from homeassistant.helpers.entity import Entity
from homeassistant.const import (
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_ILLUMINANCE,
    TEMP_CELSIUS,
    ATTR_TEMPERATURE,
)

from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.components.climate.const import (
    CURRENT_HVAC_COOL,
    CURRENT_HVAC_DRY,
    CURRENT_HVAC_FAN,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    CURRENT_HVAC_OFF,
    HVAC_MODE_AUTO,
    HVAC_MODE_OFF,
)
from homeassistant.components.climate import (
    ClimateEntity,
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    HVAC_MODE_HEAT,
)
import voluptuous as vol

from homeassistant.helpers.config_validation import entity_id, time
from homeassistant.const import ATTR_ENTITY_ID, ATTR_TEMPERATURE, ATTR_TIME

from .const import DOMAIN, KEY_API

import logging

from dobissapi import (
    DobissAPI,
    DobissTempSensor,
    ICON_FROM_DOBISS,
)

_LOGGER = logging.getLogger(__name__)

SERVICE_SET_HVAC_TEMP_TIMER = "set_hvac_temp_timer"

SET_HVAC_TEMP_TIMER_SCHEMA = vol.Schema(
    vol.All(
        {
            vol.Required(ATTR_ENTITY_ID): vol.Coerce(entity_id),
            vol.Optional(ATTR_TIME): vol.Coerce(int),
            vol.Optional(ATTR_TEMPERATURE): vol.Coerce(float),
        }
    )
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up dobisssensor."""

    dobiss = hass.data[DOMAIN][config_entry.entry_id][KEY_API].api

    # only add HVAC objects for temperature sensors when there is at least a schedule entry
    if len(dobiss.calendars) == 0:
        return

    entities = []
    d_entities = dobiss.get_devices_by_type(DobissTempSensor)
    for d in d_entities:
        entities.append(HADobissClimateControl(d))
    if entities:
        async_add_entities(entities)

    async def handle_set_hvac_temp_timer(call):
        """Handle set_hvac_timer service."""
        entity_id = call.data.get(ATTR_ENTITY_ID)
        entity = next(
            (dev for dev in entities if dev.entity_id == entity_id),
            None,
        )
        if entity == None:
            raise ValueError(f"no entity found in {DOMAIN} that matches {entity_id}")
        time = call.data.get(ATTR_TIME, None)
        if time == None:
            if entity._dobisssensor.manual_mode:
                time = entity._dobisssensor.time
            else:
                time = 30  # default to 30 minutes
        temp = call.data.get(ATTR_TEMPERATURE, entity._dobisssensor.asked)
        await entity._dobisssensor.set_temp_timer(temp, time)

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_HVAC_TEMP_TIMER,
        handle_set_hvac_temp_timer,
        schema=SET_HVAC_TEMP_TIMER_SCHEMA,
    )


class HADobissClimateControl(ClimateEntity):
    """Dobiss ssensor device."""

    should_poll = False

    temperature_unit = TEMP_CELSIUS

    supported_features = SUPPORT_TARGET_TEMPERATURE | SUPPORT_PRESET_MODE

    def __init__(self, dobisssensor: DobissTempSensor):
        """Init dobiss ClimateControl device."""
        super().__init__()
        self._dobisssensor = dobisssensor

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, f"climatecontrol_{self._dobisssensor.object_id}")},
            "name": f"climatecontrol_{self.name}",
            "manufacturer": "dobiss",
        }

    @property
    def device_state_attributes(self):
        """Return supported attributes."""
        return self._dobisssensor.attributes

    @property
    def available(self) -> bool:
        """Return True."""
        return True

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
        return f"climatecontrol_{self._dobisssensor.object_id}"

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._dobisssensor.value

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._dobisssensor.asked

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return 0.1

    async def async_set_temperature(self, **kwargs):
        value = kwargs.get(ATTR_TEMPERATURE, self.target_temperature)
        await self._dobisssensor.set_temperature(value)

    async def async_set_hvac_mode(self, hvac_mode: str):
        await self._dobisssensor.set_manual_mode(hvac_mode == HVAC_MODE_HEAT)

    async def async_set_preset_mode(self, preset_mode: str):
        await self._dobisssensor.set_preset_mode(preset_mode)

    @property
    def preset_modes(self):
        return self._dobisssensor._dobiss.calendars

    @property
    def preset_mode(self):
        """Return the current preset mode, e.g., home, away, temp.
        Requires SUPPORT_PRESET_MODE.
        """
        return self._dobisssensor.calendar

    @property
    def hvac_mode(self):
        """Return hvac operation ie. heat, cool mode.
        Need to be one of HVAC_MODE_*.
        """
        if self._dobisssensor.time != None and self._dobisssensor.time >= 0:
            return HVAC_MODE_HEAT
        return HVAC_MODE_AUTO

    @property
    def hvac_modes(self):
        """Return the list of available hvac operation modes.
        Need to be a subset of HVAC_MODES.
        """
        modes = []
        modes.append(HVAC_MODE_HEAT)
        modes.append(HVAC_MODE_AUTO)
        return modes

    @property
    def hvac_action(self):
        """Return the current running hvac operation if supported.

        Need to be one of CURRENT_HVAC_*.
        """
        if self._dobisssensor.status == 1:
            return CURRENT_HVAC_HEAT
        return CURRENT_HVAC_IDLE
