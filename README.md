# dobiss

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![pre-commit][pre-commit-shield]][pre-commit]
[![Black][black-shield]][black]

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

## Installation

Preferred way to install is using HACS

Manual Install:

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `dobiss`.
4. Download _all_ the files from the `custom_components/dobiss/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "dobiss"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/dobiss/translations/en.json
custom_components/dobiss/__init__.py
custom_components/dobiss/binary_sensor.py
custom_components/dobiss/config_flow.py
custom_components/dobiss/const.py
custom_components/dobiss/manifest.json
custom_components/dobiss/sensor.py
custom_components/dobiss/switch.py
custom_components/dobiss/climate.py
custom_components/dobiss/cover.py
custom_components/dobiss/light.py
```

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
[black]: https://github.com/psf/black
[black-shield]: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
[buymecoffee]: https://www.buymeacoffee.com/kesteraernoudt
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/kesteraernoudt/dobiss.svg?style=for-the-badge
[commits]: https://github.com/kesteraernoudt/dobiss/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/kesteraernoudt/dobiss.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40kesteraernoudt-blue.svg?style=for-the-badge
[pre-commit]: https://github.com/pre-commit/pre-commit
[pre-commit-shield]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/kesteraernoudt/dobiss.svg?style=for-the-badge
[releases]: https://github.com/kesteraernoudt/dobiss/releases
[user_profile]: https://github.com/kesteraernoudt
[dobiss]: https://www.dobiss.com/en
[pydobiss]: https://pypi.org/project/pydobiss/
[dobiss_api]: http://support.dobiss.com/books/nl-dobiss-nxt/page/developer-api
[icon]: https://brands.home-assistant.io/dobiss/icon.png
[logo]: https://brands.home-assistant.io/_/dobiss/logo.png
