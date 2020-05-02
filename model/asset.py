from config.constants import *
import json, os
from model.currency import CurrencyConverter

_ASSET_FILE = "asset.json"


def get_assets():
    with open(_get_file_path()) as f:
        json_data = json.load(f)
    return json_data


def get_asset_resale_value_sum() -> float:
    amount = 0
    assets = get_assets()
    currency_converter = CurrencyConverter()

    for asset in assets["assets"]:
        amount += currency_converter.convert_to_local_currency(asset["sales_value"], asset["currency"])

    return amount


def _get_file_path():
    return os.path.join(DATA_DIR_PATH + _ASSET_FILE)