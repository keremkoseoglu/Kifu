""" Assets """
import json
import os
from model.currency import CurrencyConverter
import config


_ASSET_FILE = "asset.json"


def _is_liquid(asset_type: str) -> bool:
    return asset_type in ("STOCK", "CRYPTO")


def get_assets():
    """ Returns all assets """
    with open(_get_file_path()) as asset_file:
        json_data = json.load(asset_file)
    return json_data


def set_assets(assets: dict):
    """ Saves assets to disk """
    with open(_get_file_path(), "w") as ass_file:
        json.dump(assets, ass_file, indent=3)


def get_asset_type_resale_value_sum(only_liquid: bool = False) -> []:
    """ Asset type resale value sum
    Used when calculating net worth
    """
    result = []

    assets = get_assets()
    currency_converter = CurrencyConverter()

    for asset in assets["assets"]:
        if only_liquid and not _is_liquid(asset["type"]):
            continue

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


def get_liquid_assets_in_both_currencies() -> []:
    """ Asset balances in original and home currencies """
    output = []
    assets = get_assets()
    currency_converter = CurrencyConverter()

    for asset in assets["assets"]:
        if not _is_liquid(asset["type"]):
            continue

        org_amount = asset["sales_value"] * asset["quantity"]

        local_amount = currency_converter.convert_to_local_currency(
            org_amount,
            asset["currency"])

        name = asset["bank"] + " - " + asset["type"]
        found = False

        for out in output:
            if out["name"] == name and out["original_currency"] == asset["currency"]:
                found = True
                out["home_balance"] += local_amount
                out["original_balance"] += org_amount
                break

        if not found:
            output_dict = {
                "name": asset["bank"] + " - " + asset["type"],
                "home_balance": local_amount,
                "original_balance": org_amount,
                "original_currency": asset["currency"],
                "is_investment": True
            }
            output.append(output_dict)

    return output


def _get_file_path():
    return os.path.join(config.CONSTANTS["DATA_DIR_PATH"] + _ASSET_FILE)
