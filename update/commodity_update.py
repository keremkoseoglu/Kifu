""" Commodity update module
This module is deprecated. sahibinden.com detects and prevents such bots.
A manual asset value update was developed instead.
You can access it via the menu Assets - Update Commodities.
"""
import time
import random
from sahibinden.quick_median import QuickMedian
from sahibinden.toolkit import SearchInput
from incubus import IncubusFactory
import config
from model import asset as imp_asset
from model.currency import OldCurrencyConverter, CurrencyConverter
from util import backup
from util.date_time import parse_json_date

_FOREIGN_CURR = "USD"

def execute():
    """ Stock update for all assets """
    _execute()

def execute_single(asset_guid: str):
    """ Stock update for single asset """
    _execute(asset_guid=asset_guid)

def _execute(asset_guid: str = None):
    """ Stock update """
    backup.execute()

    assets = imp_asset.get_assets()
    random.shuffle(assets["assets"])
    first_asset = True

    for asset in assets["assets"]:
        if asset["type"] != "COMMODITY":
            continue
        if "url_suffix" not in asset:
            continue
        if asset["url_suffix"] == "":
            continue
        if asset_guid is not None and asset["guid"] != asset_guid:
            continue

        if first_asset:
            first_asset = False
        else:
            time.sleep(config.CONSTANTS["COMMODITY_SEARCH_SLEEP"])
            IncubusFactory.get_instance().user_event()

        try:
            url = config.CONSTANTS["COMMODITY_URL"] + asset["url_suffix"]
            search_input = SearchInput(url=url, post_sleep=config.CONSTANTS["COMMODITY_PAGE_SLEEP"])
            quick_median = QuickMedian(search_input)

            asset["sales_value"] = \
                conv_last_usd_val_to_home_curr(asset) \
                if quick_median.median == 0 \
                else quick_median.median

        except Exception as update_error:
            print(f"Commodity search error: { str(update_error) } ")

    imp_asset.set_assets(assets)

def conv_last_usd_val_to_home_curr(asset_guid: str) -> int:
    """ Convert last known value to USD then project as TRY """
    result = 0
    assets = imp_asset.get_assets()["assets"]

    for asset in assets:
        if asset["guid"] != asset_guid:
            continue
        if "value_history" not in asset:
            break
        values = asset["value_history"]
        last_val = values[len(values)-1]
        last_date = parse_json_date(last_val["date"])

        historic_curr_conv = OldCurrencyConverter(last_date)
        today_curr_conv = CurrencyConverter()

        last_val_usd = \
            historic_curr_conv.convert_to_foreign_currency(
                last_val["value"],
                foreign_currency=_FOREIGN_CURR)

        result = \
            today_curr_conv.convert_to_local_currency(
                foreign_amount=last_val_usd,
                foreign_currency=_FOREIGN_CURR)

        break

    return int(result)
