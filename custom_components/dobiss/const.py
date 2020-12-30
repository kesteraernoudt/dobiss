"""Constants for the dobiss integration."""
from homeassistant.const import CONF_HOST  # noqa: F401 pylint: disable=unused-import

DOMAIN = "dobiss"
CONF_SECRET = "secret"
CONF_SECURE = "secure"

KEY_API = "dobiss_api"
DEVICES = "dobiss_devices"
DOBISS_CLIMATE_DEVICES = "dobiss_climate_devices"

# Options
CONF_INVERT_BINARY_SENSOR = "invert_binary_sensor"
DEFAULT_INVERT_BINARY_SENSOR = False
