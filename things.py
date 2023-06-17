from openrgb.utils import RGBColor, DeviceType

from tools import clamp


class Rule:
    def __init__(self, type, interval, source, color_min, color_max, mode, curve, led_mode, smooth):
        self.type = type
        self.interval = interval
        self.source = source
        self.curve = curve
        self.mode = mode
        self.color_min = RGBColor(color_min[0], color_min[1], color_min[2])
        self.color_max = RGBColor(color_max[0], color_max[1], color_max[2])
        self.led_mode = led_mode
        self.id = id(self)
        self.smooth = smooth
        self.values = []

    @classmethod
    def from_json(cls, data):
        type = data.get('type')
        interval = data.get('interval')
        source = data.get('source')
        curve = data.get('curve')
        color_min = data.get('color_min')
        color_max = data.get('color_max')
        mode = data.get('mode')
        led_mode = data.get('led_mode')
        smooth = clamp(data.get('smooth'), 1, 32)
        return cls(type=type, interval=interval, source=source, color_min=color_min, color_max=color_max, mode=mode, curve=curve, led_mode=led_mode, smooth=smooth)

    @classmethod
    def parse_rules(cls, data):
        rules = []
        for value in data:
            rules.append(Rule.from_json(value))
        return rules

    def to_string(self):
        return f"Rule(type={self.type}, source={self.source})"

    def commit_value(self, v):
        self.values = [v] + self.values
        
        if len(self.values) > self.smooth:
            self.values = self.values[:self.smooth]

        sum = 0
        for val in self.values:
            sum = sum + val

        return sum / len(self.values)
