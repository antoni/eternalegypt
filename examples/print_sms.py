#!/usr/bin/env python3

"""Print all SMS messages to stdout and mark them as read."""

import asyncio
import pprint
import sys

import aiohttp

import eternalegypt


async def print_sms(hostname, password):
    """Print the modem's inbox and mark each message as read."""
    jar = aiohttp.CookieJar(unsafe=True)
    async with aiohttp.ClientSession(cookie_jar=jar) as websession:
        modem = eternalegypt.Modem(hostname=hostname, websession=websession)
        await modem.login(password=password)
        try:
            result = await modem.information()
            for sms in result.sms:
                pprint.pprint(sms, stream=sys.stdout)
                await modem.set_read_sms_message(sms.id)
        finally:
            await modem.logout()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("{}: <netgear ip> <netgear password>".format(sys.argv[0]))
    asyncio.run(print_sms(sys.argv[1], sys.argv[2]))
