"""Sensors from OGC Sensorthings DataStreams"""
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import (
    HomeAssistant,
    callback
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN
# from .coordinator import DGTInfoCarCoordinator

import traceback

import asyncio
import aiohttp

from datetime import timedelta

SCAN_INTERVAL = timedelta(seconds=60)


session = aiohttp.ClientSession()

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add cameras for passed config_entry."""

    url = config_entry.data['url']

    # Fetch URL of DataStreams endpoint
    resp = await session.get(url)
    json = await resp.json()
    values = json['value']

    datastreams_url = [i['url'] for i in values if i['name']=='Datastreams'][0]

    # print(f"Datastreams url: {datastreams_url}")

    # Fetch available DataStreams
    # Ask the Thing for each datastream to be expanded, in order to build the
    # HASS DeviceInfo structure easier
    # FIXME: Right now this only requests the first 10 datastreams to ease debugging
    # TODO: URL handling should be more robust, request parameter(s) should be
    # added via https://docs.python.org/3/library/urllib.parse.html
    resp = await session.get(f"{datastreams_url}?$top=10&$expand=Thing")
    json = await resp.json()

    sensors = []

    for datastream in json['value']:
        # print (datastream)

        sensors.append(
            OGCSTSensor(datastream)
        )

    async_add_entities(sensors)


class OGCSTSensor(SensorEntity):
    """A SensorThings DataStream, mapped to a HASS Sensor entity."""

    def __init__ (self, datastream = None ):

        # Instance attributes built into Entity:
        self._attr_name = datastream['description']
        self._attr_should_poll = True
        # self._attr_icon = icon
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, datastream['Thing']['@iot.id'])},
            name=datastream['Thing']['name']
        )
        self._attr_unique_id = datastream['@iot.id']

        # Instance attributes built into SensorEntity:
        # self._attr_state_class = state_class
        # self._attr_native_value = None
        self._attr_native_unit_of_measurement = datastream['unitOfMeasurement']['symbol']


        self.last_observation_url = f"{datastream['Observations@iot.navigationLink']}?$top=1&$orderby=phenomenonTime desc"

        # TODO: Store other datastream data into the `extra_state_attributes`
        # property of this class.

    async def async_update(self):
        """Requests the last observation"""
        print("Polling", self.name)

        # Note this is automatically called by HASS every SCAN_INTERVAL.
        resp = await session.get(self.last_observation_url)
        json = await resp.json()

        print(self.name, json)

        if len(json['value']) == 0:
            return None
        else:
            self._attr_native_value = json['value'][0]['result']
            return self.async_write_ha_state()


