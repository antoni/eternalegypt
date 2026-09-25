#!/usr/bin/env python3

"""Example file for eternalegypt library."""

import sys
import asyncio
import aiohttp

import eternalegypt

import logging

logging.basicConfig(level=logging.DEBUG)


DNS1 = "94.140.14.14"  # AdGuard DNS
DNS2 = "94.140.15.15"
GATEWAY_IP = "192.168.86.1"
DHCP_RANGE_LOW = "192.168.86.20"
DHCP_RANGE_HIGH = "192.168.86.99"


def needs_update(items, wanted):
    """Return True if any wanted config value differs from the modem's.

    Keys are the lowercased model.json paths from Information.items.
    A key missing from the modem counts as different.
    """
    changed = {key: items.get(key) for key, value in wanted.items()
               if str(items.get(key)) != value}
    if changed:
        print("Needs update, current values: {}".format(changed))
    return bool(changed)


async def configure():
    """Example of configuring fresh router"""
    jar = aiohttp.CookieJar(unsafe=True)
    async with aiohttp.ClientSession(cookie_jar=jar) as websession:
        modem = eternalegypt.Modem(hostname=sys.argv[1], websession=websession)
        await modem.login(password=sys.argv[2])

        try:
            # Doesn't require reboot
            await modem.turn_off_wifi_when_tethering()
            await modem.set_led_enabled(False)

            # Mark all messages as read
            result = await modem.information()
            for sms in result.sms:
                await modem.set_read_sms_message(sms.id)

            # Requires reboot, so only when something changes
            if needs_update(result.items, {
                    "router.dhcp.dnsmode": "Manual",
                    "router.dhcp.dns1": DNS1,
                    "router.dhcp.dns2": DNS2}):
                await modem.set_dns(DNS1, DNS2)
                await modem.wait_for_reboot()
            else:
                print("DNS already set, skipping")

            # Requires reboot and may change the gateway IP, so keep it last
            if needs_update(result.items, {
                    "router.gatewayip": GATEWAY_IP,
                    "router.dhcp.range.low": DHCP_RANGE_LOW,
                    "router.dhcp.range.high": DHCP_RANGE_HIGH}):
                await modem.set_network_settings(GATEWAY_IP, DHCP_RANGE_LOW, DHCP_RANGE_HIGH)
            else:
                print("Network settings already set, skipping")
        finally:
            print("Closing down")
            await modem.logout()


if len(sys.argv) != 3:
    print("{}: <netgear ip> <netgear password>".format(sys.argv[0]))
else:
    asyncio.run(configure())
