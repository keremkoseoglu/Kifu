""" Configuration module """
import os
from os import path
import json
from sagkutana.switcher import Switcher
from util import backup


CONSTANTS = {}
TEST_MODE = False
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
    _read_kutapada()


def test_mode():
    """ Activates test mode """
    global CONSTANTS, TEST_MODE
    TEST_MODE = True
    backup_dir = backup.execute()
    CONSTANTS["DATA_DIR_PATH"] = backup_dir + "/"


def _read_config():
    global _CONFIG
    if _CONFIG != {}:
        return
    config_path = path.join(os.getcwd(), _CONFIG_FILE)
    with open(config_path) as config_file:
        _CONFIG = json.load(config_file)

def _read_kutapada():
    global CONSTANTS
    if "KUTAPADA_PATH" not in CONSTANTS:
        return
    with open(CONSTANTS["KUTAPADA_PATH"]) as kutapada_file:
        kutapada_json = json.load(kutapada_file)
    for system in kutapada_json["systems"]:
        if system["name"] == CONSTANTS["ECZ_DAHA_KUTAPADA"]:
            account = system["accounts"][0]
            CONSTANTS["ECZ_DAHA_USER"] = account["name"]
            CONSTANTS["ECZ_DAHA_PASS"] = Switcher().decrypt_text(account["credential"])
            return
