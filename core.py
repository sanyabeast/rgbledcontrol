
import socket
import time
from openrgb import OpenRGBClient
from openrgb.utils import RGBColor, DeviceType
import sys

from tools import apply_color_brightness, clamp, ease_value, get_cpu_usage, get_gpu_usage, get_ram_usage, lerp_color, timer_gate

client = None

def init_ledcontrol(rules, config):
    global client

    client = 0
    x = 0
    while x <= config["retry_count"]:
        try:
            client = OpenRGBClient()
            break
        except socket.timeout:
            time.sleep(config["retry_timeout"])
            print(f'failed to connect: retry in {config["retry_timeout"]}s; ({x}/{config["retry_count"]})')
            x += 1

    if (client == 0):
        print('failed to connect')
        sys.exit()
        return 0

    print('connected')
    client.clear()

    for rule in rules:
        if rule.type == 'mb':
            devices = client.get_devices_by_type(DeviceType.MOTHERBOARD)
        elif rule.type == 'ram':
            devices = client.get_devices_by_type(DeviceType.DRAM)
        elif rule.type == 'gpu':
            devices = client.get_devices_by_type(DeviceType.GPU)

    for dv in devices:
        dv.set_mode(rule.led_mode)


def update_rule(rule):

    if (timer_gate(rule.id, rule.interval)):
        # print(f'updating rule: {rule.to_string()}')
        devices = None
        progress = 0
        curved_progress = 0
        new_color = rule.color_min

        # type
        if rule.type == 'mb':
            devices = client.get_devices_by_type(DeviceType.MOTHERBOARD)
        elif rule.type == 'ram':
            devices = client.get_devices_by_type(DeviceType.DRAM)
        elif rule.type == 'gpu':
            devices = client.get_devices_by_type(DeviceType.GPU)

        if len(devices) == 0:
            print(f'no devices for rule: {rule.to_string()}')
            return

        # source
        if rule.source == 'cpu':
            progress = get_cpu_usage()
        elif rule.source == 'ram':
            progress = get_ram_usage()
        elif rule.source == 'gpu':
            progress = get_gpu_usage()
        elif rule.source == 'always_max':
            progress = 1
        elif rule.source == 'always_min':
            progress = 0

        # progress = rule.commit_value(progress)    
        # print(progress)

        curved_progress = ease_value(progress, rule.curve)
        curved_progress = rule.commit_value(curved_progress)    

        new_color = lerp_color(
            rule.color_min, rule.color_max, curved_progress)

        # print(f"{rule.to_string()}: {'{:2.2f}'.format(progress * 100)}%, curved progress: {'{:2.2f}'.format(curved_progress * 100)}%")

        # applying
        if rule.mode == "zone_step":
            for dv in devices:
                zn_index = 0
                for zn in dv.zones:
                    if (zn_index / len(dv.zones) <= curved_progress):
                        zn.set_color(rule.color_max)
                    else:
                        zn.set_color(rule.color_min)
                    zn_index += 1
        if rule.mode == "zone_step_reverse":
            for dv in devices:
                zn_index = len(dv.zones) - 1
                for zn in dv.zones:
                    if (zn_index / len(dv.zones) >= curved_progress):
                        zn.set_color(rule.color_min)

                    else:
                        zn.set_color(rule.color_max)
                    zn_index -= 1
                    # zn.set_color(new_color)
        if rule.mode == "led_step":
            for dv in devices:
                total_leds = 0
                for zn in dv.zones:
                    total_leds += len(zn.leds)
                ld_index = 0
                for zn in dv.zones:
                    for ld in zn.leds:
                        if (ld_index / total_leds <= curved_progress):
                            ld.set_color(rule.color_max)
                        else:
                            ld.set_color(rule.color_min)
                        ld_index += 1
        if rule.mode == "led_step_reverse":
            for dv in devices:
                total_leds = 0
                for zn in dv.zones:
                    total_leds += len(zn.leds)
                ld_index = total_leds - 1
                for zn in dv.zones:
                    for ld in zn.leds:
                        if (ld_index / total_leds <= curved_progress):
                            ld.set_color(rule.color_max)
                        else:
                            ld.set_color(rule.color_min)
                        ld_index -= 1
        if rule.mode == "default":
            for dv in devices:
                for zn in dv.zones:
                    zn.set_color(new_color)
