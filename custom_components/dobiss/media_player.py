"""Support for dobiss media players."""
import logging

from dobissapi import DobissAudioZone

from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.const import ATTR_ENTITY_ID, ENTITY_MATCH_ALL, ENTITY_MATCH_NONE
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, KEY_API

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up dobiss media players."""
    _LOGGER.debug(f"Setting up media_player component of {DOMAIN}")

    dobiss = hass.data[DOMAIN][config_entry.entry_id][KEY_API].api
    entities = [HADobissMediaPlayer(d) for d in dobiss.get_devices_by_type(DobissAudioZone)]
    if entities:
        async_add_entities(entities)


class HADobissMediaPlayer(MediaPlayerEntity):
    """Dobiss media player device."""

    should_poll = False

    def __init__(self, dobiss_audio_zone: DobissAudioZone):
        """Init dobiss media player device."""
        super().__init__()
        self._dobiss_audio_zone = dobiss_audio_zone
        self._attr_supported_features = self._calculate_supported_features()

    def _calculate_supported_features(self):
        features = MediaPlayerEntityFeature.TURN_ON | MediaPlayerEntityFeature.TURN_OFF
        if hasattr(self._dobiss_audio_zone, "set_volume") or hasattr(
            self._dobiss_audio_zone, "volume"
        ):
            features |= MediaPlayerEntityFeature.VOLUME_SET
        if hasattr(self._dobiss_audio_zone, "set_mute") or hasattr(
            self._dobiss_audio_zone, "is_muted"
        ):
            features |= MediaPlayerEntityFeature.VOLUME_MUTE
        if hasattr(self._dobiss_audio_zone, "set_source") or hasattr(
            self._dobiss_audio_zone, "sources"
        ):
            features |= MediaPlayerEntityFeature.SELECT_SOURCE
        return features

    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._dobiss_audio_zone.object_id)},
            "name": self.name,
            "manufacturer": "dobiss",
        }

    @property
    def extra_state_attributes(self):
        """Return supported attributes."""
        return self._dobiss_audio_zone.attributes

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        self._dobiss_audio_zone.register_callback(self.async_write_ha_state)
        self.async_on_remove(
            async_dispatcher_connect(self.hass, DOMAIN, self.signal_handler)
        )

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        self._dobiss_audio_zone.remove_callback(self.async_write_ha_state)

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

    @property
    def state(self):
        """Return the state of the media player."""
        is_on = getattr(self._dobiss_audio_zone, "is_on", None)
        if is_on is None:
            return None
        return MediaPlayerState.PLAYING if is_on else MediaPlayerState.OFF

    @property
    def volume_level(self):
        """Return volume level as 0..1."""
        volume = None
        if hasattr(self._dobiss_audio_zone, "volume"):
            volume = self._dobiss_audio_zone.volume
        elif hasattr(self._dobiss_audio_zone, "value"):
            volume = self._dobiss_audio_zone.value
        else:
            volume = self._dobiss_audio_zone.attributes.get("volume")
        if volume is None:
            return None
        return max(0, min(volume, 100)) / 100

    @property
    def is_volume_muted(self):
        """Return if the media player is muted."""
        if hasattr(self._dobiss_audio_zone, "is_muted"):
            return self._dobiss_audio_zone.is_muted
        if hasattr(self._dobiss_audio_zone, "muted"):
            return self._dobiss_audio_zone.muted
        return self._dobiss_audio_zone.attributes.get("muted")

    @property
    def source(self):
        """Return the current input source."""
        if hasattr(self._dobiss_audio_zone, "source"):
            return self._dobiss_audio_zone.source
        return self._dobiss_audio_zone.attributes.get("source")

    @property
    def source_list(self):
        """Return a list of available sources."""
        if hasattr(self._dobiss_audio_zone, "sources"):
            return self._dobiss_audio_zone.sources
        if hasattr(self._dobiss_audio_zone, "source_list"):
            return self._dobiss_audio_zone.source_list
        return self._dobiss_audio_zone.attributes.get("sources")

    async def async_turn_on(self):
        """Turn the media player on."""
        if hasattr(self._dobiss_audio_zone, "turn_on"):
            await self._dobiss_audio_zone.turn_on()

    async def async_turn_off(self):
        """Turn the media player off."""
        if hasattr(self._dobiss_audio_zone, "turn_off"):
            await self._dobiss_audio_zone.turn_off()

    async def async_set_volume_level(self, volume):
        """Set volume level."""
        level = int(volume * 100)
        if hasattr(self._dobiss_audio_zone, "set_volume"):
            await self._dobiss_audio_zone.set_volume(level)
        elif hasattr(self._dobiss_audio_zone, "set_value"):
            await self._dobiss_audio_zone.set_value(level)
        else:
            _LOGGER.warning("Dobiss audio zone does not support volume control")

    async def async_mute_volume(self, mute):
        """Mute or unmute the media player."""
        if hasattr(self._dobiss_audio_zone, "set_mute"):
            await self._dobiss_audio_zone.set_mute(mute)
        else:
            _LOGGER.warning("Dobiss audio zone does not support muting")

    async def async_select_source(self, source):
        """Select input source."""
        if hasattr(self._dobiss_audio_zone, "set_source"):
            await self._dobiss_audio_zone.set_source(source)
        else:
            _LOGGER.warning("Dobiss audio zone does not support source selection")

    @property
    def name(self):
        """Return the display name of this media player."""
        return self._dobiss_audio_zone.name

    @property
    def unique_id(self):
        """Return a unique ID."""
        return self._dobiss_audio_zone.object_id
