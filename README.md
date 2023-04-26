# homeassistant-sensorthings

`homeassistant-sensorthings` is a **prototype** [Home Assistant](https://www.home-assistant.io) integration for [OGC SensorThings](https://ogcapi.ogc.org/sensorthings/) services.

## Installation

#### Guided installation

- Enable the [HACS](https://hacs.xyz/) integration in your Home Assistant instance.
- Use the side menu to browse HACS.
- Navigate to "Integrations", then use the overflow menu (three dots at the top-right) to add a Custom Repository.
- Enter the URL `https://github.com/IvanSanchez/homeassistant-sensorthingss`, of type "Integration"
- You should see a new box labelled "OGC Sensorthings". Click on it and follow HACS' instructions to download and enable the integration.
- Restart Home Assistant when HACS tells you to.

#### Manual installation

Download the files from this repository. Copy the `custom_components/sensorthings/` directory into the `custom_components` directory of your Home Assistant instance.

e.g. if your configuration file is in `/home/homeassistant/.homeassistant/configuration.yaml`, then the files from this integration should be copied to `/home/homeassistant/.homeassistant/custom_components/sensorthings/`.

Restart Home Assistant to ensure the integration can be detected.


## Usage

Use the Home Assistant GUI to add a new integration (settings → devices & services → add new integration). You should find the OGC SensorThings integration in the list.

Configuration only requires the base URL of the OGC SensorThings endpoint (including its version). e.g. `https://ogc-demo.k8s.ilt-dmz.iosb.fraunhofer.de/v1.1` or `https://sensors.bgs.ac.uk/FROST-Server/v1.1`.

## OGC compliance

Even though this integration implements a OGC SensorThings client, and has been tested with several SensorThings endpoints, it has **not** undergone any OGC compliance tests.


## License

Licensed under GPLv3. See the `LICENSE` file for details.
