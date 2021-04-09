""" Stock update module """
import requests
import config
from model import asset as imp_asset

def _find_between(doc, first, last):
    try:
        start = doc.index(first) + len(first)
        end = doc.index(last, start)
        return doc[start:end]
    except ValueError:
        return ""

def execute():
    """ Stock update """
    assets = imp_asset.get_assets()

    for asset in assets["assets"]:
        if asset["type"] != "STOCK":
            continue
        if "url_suffix" not in asset:
            continue
        if asset["url_suffix"] == "":
            continue

        url = config.CONSTANTS["STOCK_URL"] + asset["url_suffix"]
        resp = requests.get(url, verify=False)
        str_val = _find_between(resp.text, '<span class="value">', '</span>')
        str_val = str_val.replace(".", "").replace(",", ".")
        asset["sales_value"] = float(str_val)

    imp_asset.set_assets(assets)
