

import socket
import time
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType
import sys


def reset(mode="direct"):
    global client

    client = 0
    x = 0
    while x <= 32:
        try:
            client = OpenRGBClient()
            break
        except socket.timeout:
            time.sleep(1)
            x += 1

    if (client == 0):
        sys.exit()
        return 0

    client.clear()
    devices = client.get_devices_by_type(DeviceType.DRAM)
    for dv in devices:
        try:
            dv.set_mode(mode)
        except Exception as e:
            print(e)

    devices = client.get_devices_by_type(DeviceType.MOTHERBOARD)
    for dv in devices:
        try:
            dv.set_mode(mode)
        except Exception as e:
            print(e)

    devices = client.get_devices_by_type(DeviceType.GPU)
    for dv in devices:
        try:
            dv.set_mode(mode)
        except Exception as e:
            print(e)


def run_script(rules, config):
    reset("off")
    time.sleep(1)
    reset("direct")
    time.sleep(1)
    reset("off")
    time.sleep(2)


if __name__ == "__main__":
    run_script(None, None)
