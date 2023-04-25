from homeassistant import config_entries
from .const import DOMAIN
from homeassistant.const import (CONF_URL)
from homeassistant.components import zeroconf
import voluptuous as vol
import logging
from typing import Any, Final
from homeassistant.data_entry_flow import FlowResult
from getmac import get_mac_address
import aiohttp
import re


_LOGGER = logging.getLogger(__name__)

session = aiohttp.ClientSession()

class SensorThingsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for a SensorThings endpoint."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1

    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""

        errors: dict[str, str] = {}
        if user_input is not None:
            url: str = user_input[CONF_URL]

            try:
                info = await self._async_get_info(url)

                await self.async_set_unique_id(info['url'])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=url, data={
                    "url": url,
                })

            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # TODO: Optionally add a numeric field asking for the polling interval
        # Right now this is hard-coded to 300 seconds (5 minutes) in sensor.py.

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_URL): str,
            }),
            errors=errors
        )


    async def _async_get_info(self, url):
        """Checks that the SensorThings endpoint implements required data and conformance classes"""

        resp = await session.get(url)

        if (resp.status == 401):
            return { 'error': 'invalid_auth' }
        elif (resp.status != 200):
            return { 'error': 'unknown' }

        json = await resp.json()

        values = json['value']

        conformances = json['serverSettings']['conformance']

        print (values, conformances);

        if not 'http://www.opengis.net/spec/iot_sensing/1.1/req/datamodel' in conformances:
            return {'error': 'not_conforming'}
        if not 'http://www.opengis.net/spec/iot_sensing/1.1/req/request-data' in conformances:
            return {'error': 'not_conforming'}

        if not any(x['name'] == 'Datastreams' for x in values):
            return {'error': 'not_conforming'}
        if not any(x['name'] == 'Things' for x in values):
            return {'error': 'not_conforming'}


        # TODO: Return conformance classes (and save them in the config entry)
        # In particular, store whether the endpoint sends updates via MQTT.
        return {'url': url}

