""" Configuration module """
import os
from os import path
import json


CONSTANTS = {}
_CONFIG_FILE = "config.json"
_CONFIG = {}



def read_constants():
    """ Loads all constants """
    global CONSTANTS, _CONFIG
    if CONSTANTS != {}:
        return
    _read_config()
    with open(_CONFIG["constants"]) as constants_file:
        CONSTANTS = json.load(constants_file)


def _read_config():
    global _CONFIG
    if _CONFIG != {}:
        return
    config_path = path.join(os.getcwd(), _CONFIG_FILE)
    with open(config_path) as config_file:
        _CONFIG = json.load(config_file)
