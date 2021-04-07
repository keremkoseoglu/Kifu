""" Assets """
import json
import os
from model.currency import CurrencyConverter
import config


_ASSET_FILE = "asset.json"


def get_assets():
    """ Returns all assets """
    with open(_get_file_path()) as asset_file:
        json_data = json.load(asset_file)
    return json_data


def get_asset_type_resale_value_sum() -> []:
    """ Asset type resale value sum
    Used when calculating net worth
    """
    result = []

    assets = get_assets()
    currency_converter = CurrencyConverter()

    for asset in assets["assets"]:
        asset_unit_value = currency_converter.convert_to_local_currency(
            asset["sales_value"],
            asset["currency"])
        asset_value = asset_unit_value * asset["quantity"]

        found = False
        for res in result:
            if res["type"] == asset["type"]:
                res["sales_value"] = res["sales_value"] + asset_value
                found = True

        if not found:
            res = {"type": asset["type"], "sales_value": asset_value}
            result.append(res)

    return result


def get_asset_resale_value_sum() -> float:
    """ Asset resale value sum
    Used when calculating net worth
    """
    result = 0
    type_sum = get_asset_type_resale_value_sum()

    for entry in type_sum:
        result = result + entry["sales_value"]

    return result


def _get_file_path():
    return os.path.join(config.CONSTANTS["DATA_DIR_PATH"] + _ASSET_FILE)
