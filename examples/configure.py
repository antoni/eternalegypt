#!/usr/bin/env python3

"""Example file for eternalegypt library."""

import sys
import asyncio
import aiohttp

import eternalegypt

import logging
logging.basicConfig(level=logging.DEBUG)


async def reconnect():
    """Example of configuring fresh router"""
    jar = aiohttp.CookieJar(unsafe=True)
    websession = aiohttp.ClientSession(cookie_jar=jar)

    modem = eternalegypt.Modem(hostname=sys.argv[1], websession=websession)
    await modem.login(password=sys.argv[2])

    # Doesn't require reboot
    await modem.turn_off_wifi_when_tethering()
    await modem.set_led_enabled(False)

    # await modem.login(password=sys.argv[2])

    await modem.set_network_settings()

    print("Closing down")
    await modem.logout()

    await websession.close()

if len(sys.argv) != 3:
    print("{}: <netgear ip> <netgear password>".format(sys.argv[0]))
else:
    asyncio.run(reconnect())
