""" Assets """
from copy import deepcopy
from datetime import datetime
import json
import os
from typing import List
from util.date_time import get_formatted_date
from util import identifier
from model.currency import CurrencyConverter
from model.income_tax import IncomeTaxCalculatorFactory
import config

_ASSET_FILE = "asset.json"

def is_liquid(asset_type: str) -> bool:
    """ Returns true if asset is liquid """
    return asset_type in ("STOCK", "CRYPTO")


def get_assets(deduct_income_tax: bool = False):
    """ Returns all assets """
    with open(_get_file_path()) as asset_file:
        json_data = json.load(asset_file)

    if deduct_income_tax:
        inc_tax_rate = IncomeTaxCalculatorFactory.get_instance().default_tax_rate
        rate = 1 - (inc_tax_rate / 100)
        for asset in json_data["assets"]:
            if "income_tax" in asset and asset["income_tax"]:
                asset["sales_value"] = asset["sales_value"] * rate
                if "value_history" in asset:
                    for hist in asset["value_history"]:
                        hist["value"] = hist["value"] * rate

    return json_data


def set_assets(assets: dict):
    """ Saves assets to disk """
    assets_with_history = _generate_asset_value_history(assets)
    with open(_get_file_path(), "w") as ass_file:
        json.dump(assets_with_history, ass_file, indent=3)

def set_asset(asset: dict):
    """ Sets a single asset to disk """
    all_assets = get_assets()
    asset_updated = False

    for old_asset in all_assets["assets"]:
        if old_asset["guid"] != asset["guid"]:
            continue
        for asset_field in asset:
            old_asset[asset_field] = asset[asset_field]
        asset_updated = True
        break

    if not asset_updated:
        if asset["guid"] == "":
            asset["guid"] = identifier.get_guid()
        all_assets["assets"].append(asset)

    set_assets(all_assets)

def get_asset_type_resale_value_sum(only_liquid: bool = False,
                                    deduct_income_tax: bool = False) -> List:
    """ Asset type resale value sum
    Used when calculating net worth
    """
    result = []

    assets = get_assets(deduct_income_tax=deduct_income_tax)
    currency_converter = CurrencyConverter()

    for asset in assets["assets"]:
        if only_liquid and not is_liquid(asset["type"]):
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


def get_liquid_assets_in_both_currencies(deduct_income_tax: bool = False) -> List:
    """ Asset balances in original and home currencies """
    output = []
    assets = get_assets(deduct_income_tax=deduct_income_tax)
    currency_converter = CurrencyConverter()

    for asset in assets["assets"]:
        if not is_liquid(asset["type"]):
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

def delete_assets(asset_guids: List):
    """ Deletes given assets """
    all_assets = get_assets()
    new_assets = {"assets": []}
    for i in range(len(all_assets["assets"])):
        asset_i = all_assets["assets"][i]
        if asset_i["guid"] not in asset_guids:
            new_assets["assets"].append(asset_i)
    set_assets(new_assets)

def get_asset_types() -> List:
    """ Returns asset types """
    return ["COMMODITY", "STOCK"]

def _get_file_path():
    return os.path.join(config.CONSTANTS["DATA_DIR_PATH"] + _ASSET_FILE)

def _generate_asset_value_history(assets: dict) -> dict:
    """ Adds value history to asset dict """
    max_val_hist_size = config.CONSTANTS["ASSET_HISTORY_SIZE"]
    result = deepcopy(assets)

    for asset in result["assets"]:
        if "value_history" in asset:
            last_hist_idx = len(asset["value_history"]) - 1
            if last_hist_idx >= 0:
                last_hist_val = asset["value_history"][last_hist_idx]

                if last_hist_val["value"] == asset["sales_value"]:
                    continue

        new_hist_val = {
            "date": get_formatted_date(datetime.now()),
            "value": asset["sales_value"]
        }

        asset["value_history"].append(new_hist_val)

        if len(asset["value_history"]) > max_val_hist_size:
            len_diff = len(asset["value_history"]) - max_val_hist_size
            del asset["value_history"][0 : len_diff]

    return result
