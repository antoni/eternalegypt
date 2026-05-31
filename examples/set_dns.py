#!/usr/bin/env python3

"""Example file for eternalegypt library."""

import sys
import asyncio
import aiohttp
import logging
import pprint
import json

import eternalegypt

logging.basicConfig(level=logging.DEBUG)

async def get_information():
    """Example of printing the inbox."""
    jar = aiohttp.CookieJar(unsafe=True)
    websession = aiohttp.ClientSession(cookie_jar=jar)

    modem = eternalegypt.Modem(hostname=sys.argv[1], websession=websession)
    await modem.login(password=sys.argv[2])

    result = await modem.set_dns()
    print(json.dumps(result, default=lambda o: o.__dict__))
    print("Device will be restarted now")

if len(sys.argv) != 3:
    print("{}: <netgear ip> <netgear password>".format(sys.argv[0]))
else:
    asyncio.run(get_information())
