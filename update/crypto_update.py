""" Crypto update module """
import json
import requests
import config
from model import asset as imp_asset
from util import backup

def execute(run_backup: bool = True):
    """ Crypto update """
    if run_backup:
        backup.execute()
    btc_dict = json.loads(requests.get(config.CONSTANTS["BTC_URL"], verify=False, timeout=5).text)

    assets = imp_asset.get_assets()

    for asset in assets["assets"]:
        if asset["name"] == "BTC":
            asset["sales_value"] = btc_dict["bpi"]["USD"]["rate_float"]
            asset["currency"] = "USD"

    imp_asset.set_assets(assets)
