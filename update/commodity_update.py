""" Commodity update module """
import time
import random
from sahibinden.search import Search
from incubus import IncubusFactory
import config
from model import asset as imp_asset
from util import backup

def execute():
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

        if first_asset:
            first_asset = False
        else:
            time.sleep(config.CONSTANTS["COMMODITY_SEARCH_SLEEP"])
            IncubusFactory.get_instance().user_event()

        url = config.CONSTANTS["COMMODITY_URL"] + asset["url_suffix"]
        search = Search(url, post_sleep=config.CONSTANTS["COMMODITY_PAGE_SLEEP"])
        if search.result.price_median != 0:
            asset["sales_value"] = search.result.price_median

    imp_asset.set_assets(assets)
