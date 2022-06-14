""" Commodity update module """
import time
import random
from sahibinden.quick_median import QuickMedian
from sahibinden.toolkit import SearchInput
from incubus import IncubusFactory
import config
from model import asset as imp_asset
from util import backup

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

            if quick_median.median != 0:
                asset["sales_value"] = quick_median.median
        except Exception as update_error:
            print(f"Commodity search error: { str(update_error) } ")

    imp_asset.set_assets(assets)
