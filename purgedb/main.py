import sys
import json


def _get_config(filepath: str) -> dict:
    with open(filepath) as config_file:
        return json.load(config_file)


def run_app():
    if len(sys.argv) == 1:
        print('Error: config file is missed!')
        exit(1)

    config_file = _get_config(sys.argv[1])

    return True

