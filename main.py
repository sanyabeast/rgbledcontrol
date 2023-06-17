import time
import argparse
from core import init_ledcontrol, update_rule
from things import Rule
from tools import get_gpu_usage, read_yaml_file


def main(config_path):
    config = read_yaml_file(config_path)
    update_interval = config["update_interval"]
    rules = Rule.parse_rules(config["rules"])

    print(f"rules count: {len(rules)}")

    init_ledcontrol(rules, config)

    time.sleep(config["update_delay"])

    while True:
        for r in rules:
            update_rule(r)
        time.sleep(update_interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LED Control Script")
    parser.add_argument("config_path", help="Path to the config file")
    args = parser.parse_args()

    main(args.config_path)
