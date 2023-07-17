import os
import time
import argparse
from core import init_ledcontrol, update_rule
from things import Rule
from tools import get_gpu_usage, load_script_function, log_message, read_yaml_file

log_message('ledcontrol launched')

stutter_timeout = 15


def run_script(script_base, script_name, rules, config):
    print(
        f'[ledcontrol] (i): prepare to run script "{script_name}"')
    if "scripts" in config and script_name in config["scripts"]:
        sc = load_script_function(os.path.join(
            script_base, config["scripts"][script_name]))
        if sc != None:
            try:
                sc(rules, config)
            except Exception as e:
                log_message(str(e))

    print(
        f'[ledcontrol] (i): script execution finished "{script_name}"')


def main(config_path):
    config = read_yaml_file(config_path)
    config_dir = os.path.dirname(config_path)
    update_interval = config["update_interval"]
    rules = Rule.parse_rules(config["rules"])
    print(
        f"[ledcontrol] (i): preparing ledcontrol, rules count: {len(rules)}")

    run_script(config_dir, 'preinit', rules, config)

    init_ledcontrol(rules, config)

    time.sleep(config["update_delay"])

    prev_date = time.time()
    while True:
        for r in rules:
            update_rule(r)

        # stutter check
        curr_date = time.time()
        stutter_detected = curr_date - prev_date >= update_interval + stutter_timeout
        if stutter_detected:
            log_message('stutter detected')
            run_script(config_dir, 'stutter', rules, config)

        prev_date = curr_date
        time.sleep(update_interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LED Control Script")
    parser.add_argument("config_path", help="Path to the config file")
    args = parser.parse_args()

    main(args.config_path)
