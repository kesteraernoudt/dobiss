[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

[![dobiss][icon]][dobiss]

**This component will set up the following platforms coming from a [dobiss] NXT server.**

| Platform        | Description                                                      |
| --------------- | ---------------------------------------------------------------- |
| `binary_sensor` | Dobiss contacts - can be open or closed.                         |
| `sensor`        | Dobiss sensors: temperature and light sensors.                   |
| `switch`        | Dobiss switches - can be relais outputs, flags, scenario's, etc. |
| `light`         | Dobiss lights - dimmable or not.                                 |
| `climate`       | Dobiss climate control - if you have temperature zone's.         |
| `cover`         | Dobiss covers - screens etc.                                     |

{% if not installed %}

## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "dobiss".

{% endif %}

## Configuration is done in the UI

## Dependencies

This integration will use the [pydobiss] python library which uses the native [Dobiss NXT API][dobiss_api].

[![dobiss_api][logo]][dobiss_api]

<!---->

## Credits

This project was generated from [@oncleben31](https://github.com/oncleben31)'s [Home Assistant Custom Component Cookiecutter](https://github.com/oncleben31/cookiecutter-homeassistant-custom-component) template.

Code template was mainly taken from [@Ludeeus](https://github.com/ludeeus)'s [integration_blueprint][integration_blueprint] template

---

[integration_blueprint]: https://github.com/custom-components/integration_blueprint
[buymecoffee]: https://www.buymeacoffee.com/ludeeus
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/kesteraernoudt/dobiss.svg?style=for-the-badge
[commits]: https://github.com/kesteraernoudt/dobiss/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license]: https://github.com/kesteraernoudt/dobiss/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/kesteraernoudt/dobiss.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40kesteraernoudt-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/kesteraernoudt/dobiss.svg?style=for-the-badge
[releases]: https://github.com/kesteraernoudt/dobiss/releases
[user_profile]: https://github.com/kesteraernoudt
[dobiss]: https://www.dobiss.com/en
[pydobiss]: https://pypi.org/project/pydobiss/
[dobiss_api]: http://support.dobiss.com/books/nl-dobiss-nxt/page/developer-api
[icon]: https://brands.home-assistant.io/dobiss/icon.png
[logo]: https://brands.home-assistant.io/_/dobiss/logo.png
