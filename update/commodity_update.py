""" Commodity update module """
import time
import random
from sahibinden.search import Search
import config
from model import asset as imp_asset

def execute():
    """ Stock update """
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

        if first_asset:
            first_asset = False
        else:
            time.sleep(config.CONSTANTS["COMMODITY_SEARCH_SLEEP"])

        url = config.CONSTANTS["COMMODITY_URL"] + asset["url_suffix"]
        search = Search(url, post_sleep=config.CONSTANTS["COMMODITY_PAGE_SLEEP"])
        if search.result.price_median != 0:
            asset["sales_value"] = search.result.price_median

    imp_asset.set_assets(assets)
