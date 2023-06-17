import time
import psutil
import yaml
from openrgb.utils import RGBColor, DeviceType
import py3nvml

_timer_gates = {}

def timer_gate(alias, timeout):
    global _timer_gates
    current_time = time.time()
    last_time = _timer_gates.get(alias, 0)
    if current_time - last_time >= timeout:
        _timer_gates[alias] = current_time
        return True
    else:
        return False


def read_yaml_file(file_path):
    with open(file_path, 'r') as file:
        try:
            yaml_data = yaml.safe_load(file)
            return yaml_data
        except yaml.YAMLError as e:
            print(f"Error reading YAML file: {e}")
            return {}


def ease_value(input_value, exp):
    return pow(input_value, exp)


def get_cpu_usage():
    # Get CPU usage as a percentage
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_usage = cpu_percent / 100  # Convert percentage to a float between 0 and 1
    return cpu_usage

def get_ram_usage():
    ram = psutil.virtual_memory()
    ram_percent = ram.used / ram.total
    return ram_percent

def get_gpu_usage():
    py3nvml.py3nvml.nvmlInit()
    handle = py3nvml.py3nvml.nvmlDeviceGetHandleByIndex(0)  # Assuming a single GPU is installed

    utilization = py3nvml.py3nvml.nvmlDeviceGetUtilizationRates(handle)
    gpu_usage = utilization.gpu

    py3nvml.py3nvml.nvmlShutdown()
    return gpu_usage

def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def lerp(start, end, t):
    return start + (end - start) * t

def lerp_color(color_from, color_to, t):
    return RGBColor(
        int(lerp(color_from.red, color_to.red, t)),
        int(lerp(color_from.green, color_to.green, t)),
        int(lerp(color_from.blue, color_to.blue, t)),
    )

def apply_color_brightness(brightness, rgb_color):
    return get_color_with_brightness(brightness, rgb_color.red, rgb_color.green, rgb_color.blue)


def get_color_with_brightness(brightness, r, g, b):
    r = int(clamp(r * brightness, 0, 255))
    g = int(clamp(g * brightness, 0, 255))
    b = int(clamp(b * brightness, 0, 255))
    return RGBColor(r, g, b)
