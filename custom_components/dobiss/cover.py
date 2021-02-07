"""Support for dobiss covers."""
import logging
from asyncio import wait

from dobissapi import DOBISS_UP
from dobissapi import DobissSwitch
from homeassistant.components.cover import CoverEntity
from homeassistant.components.cover import DEVICE_CLASS_SHADE
from homeassistant.components.cover import DEVICE_CLASS_WINDOW
from homeassistant.components.cover import SUPPORT_CLOSE
from homeassistant.components.cover import SUPPORT_OPEN
from homeassistant.components.cover import SUPPORT_STOP
from homeassistant.helpers.restore_state import RestoreEntity

from .const import CONF_COVER_SET_END_POSITION
from .const import DOMAIN
from .const import KEY_API

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up dobissswitch."""

    _LOGGER.debug(f"Setting up cover component of {DOMAIN}")
    dobiss = hass.data[DOMAIN][config_entry.entry_id][KEY_API].api
    # _LOGGER.warn(f"set up dobiss switch on {dobiss.host}")

    d_entities = dobiss.get_devices_by_type(DobissSwitch)
    entities = []
    for d in d_entities:
        if d.buddy:
            # only add the up cover, and his buddy is down
            if d.icons_id == DOBISS_UP:
                # _LOGGER.warn(f"set up dobiss cover {d.name} and {d.buddy.name}")
                entities.append(HADobissCover(d, d.buddy, config_entry))
    if entities:
        async_add_entities(entities)


class HADobissCover(CoverEntity, RestoreEntity):
    """Dobiss Cover device."""

    should_poll = False

    supported_features = SUPPORT_STOP | SUPPORT_OPEN | SUPPORT_CLOSE

    def __init__(self, up: DobissSwitch, down: DobissSwitch, config_entry):
        """Init dobiss Switch device."""
        super().__init__()
        # do some hacky check to see which type it is --> todo: make this flexible!
        # from dobiss: if it is a shade, up and down have the same name
        # if it is a velux shade, up and down end in 'op' and 'neer'
        # if it is a velux window, up and down end in 'open' and 'dicht'
        self._device_class = DEVICE_CLASS_SHADE
        self._is_velux = False
        self._name = up.name
        self._config_entry = config_entry
        if up.name.endswith(" op"):
            self._device_class = DEVICE_CLASS_SHADE
            self._name = up.name[: -len(" op")]
            self._is_velux = True
        elif up.name.endswith(" open"):
            self._device_class = DEVICE_CLASS_WINDOW
            self._name = up.name[: -len(" open")]
            self._is_velux = True
        self._up = up
        self._down = down
        self._last_up = False

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._up.object_id)},
            "name": self.name,
            "manufacturer": "dobiss",
        }

    @property
    def device_class(self):
        """Return the class of this device, from component DEVICE_CLASSES."""
        return self._device_class

    @property
    def device_state_attributes(self):
        """Return supported attributes."""
        prefix = "up_"
        attr = {prefix + str(key): val for key, val in self._up.attributes.items()}
        prefix = "down_"
        attr.update(
            {prefix + str(key): val for key, val in self._down.attributes.items()}
        )
        attr["last_up"] = self._last_up
        return attr

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._up.register_callback(self.async_write_ha_state)
        self._down.register_callback(self.async_write_ha_state)
        self._up.register_callback(self.up_callback)
        self._down.register_callback(self.down_callback)
        # todo: set _last_up with info coming from dobiss (not yet available in api now)
        # so for now, just restore the previous known last state, and hope the cover didn't move
        last_state = await self.async_get_last_state()
        if last_state:
            self._last_up = last_state.attributes.get("last_up")

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        self._up.remove_callback(self.async_write_ha_state)
        self._down.remove_callback(self.async_write_ha_state)
        self._up.remove_callback(self.up_callback)
        self._down.remove_callback(self.down_callback)

    @property
    def name(self):
        """Return the display name of this cover."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return f"{self._up.object_id}-{self._down.object_id}"

    @property
    def available(self) -> bool:
        """Return True."""
        return True

    @property
    def is_closed(self):
        if self._down.value is None:
            return None
        if self._config_entry.options.get(CONF_COVER_SET_END_POSITION):
            return not self._last_up and self._down.value == 0
        """ Unknown """
        return None

    @property
    def is_closing(self):
        """Return if the cover is closing or not."""
        if self._is_velux:
            return None
        return self._down.value > 0 if self._down.value else None

    @property
    def is_opening(self):
        """Return if the cover is opening or not."""
        if self._is_velux:
            return None
        return self._up.value > 0 if self._up.value else None

    async def async_toggle(self, **kwargs):
        """Toggle the entity."""
        if self._last_up:
            await self.async_close_cover(**kwargs)
        else:
            await self.async_open_cover(**kwargs)

    # callbacks to remember last direction
    def up_callback(self):
        if self._up.is_on and not self._down.is_on:
            self._last_up = True

    def down_callback(self):
        if self._down.is_on and not self._up.is_on:
            self._last_up = False

    # These methods allow HA to tell the actual device what to do. In this case, move
    # the cover to the desired position, or open and close it all the way.
    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        await self._up.turn_on()

    async def async_close_cover(self, **kwargs):
        """Close the cover."""
        await self._down.turn_on()

    async def async_stop_cover(self, **kwargs):
        """Stop the cover."""
        if self._is_velux:
            await wait([self._up.turn_on(), self._down.turn_on()])
        else:
            await wait([self._up.turn_off(), self._down.turn_off()])
