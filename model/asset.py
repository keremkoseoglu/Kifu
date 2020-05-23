""" Assets """
import json
import os
from config.constants import DATA_DIR_PATH
from model.currency import CurrencyConverter

_ASSET_FILE = "asset.json"


def get_assets():
    """ Returns all assets """
    with open(_get_file_path()) as asset_file:
        json_data = json.load(asset_file)
    return json_data


def get_asset_resale_value_sum() -> float:
    """ Asset resale value sum
    Used when calculating net worth
    """
    amount = 0
    assets = get_assets()
    currency_converter = CurrencyConverter()

    for asset in assets["assets"]:
        asset_value = currency_converter.convert_to_local_currency(
            asset["sales_value"],
            asset["currency"])
        amount += asset_value

    return amount


def _get_file_path():
    return os.path.join(DATA_DIR_PATH + _ASSET_FILE)
