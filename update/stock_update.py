""" Stock update module """
import requests
import config
from model import asset as imp_asset
from util import backup

def _find_between(doc, first, last):
    try:
        start = doc.index(first) + len(first)
        end = doc.index(last, start)
        return doc[start:end]
    except ValueError:
        return ""

def execute(run_backup: bool = True):
    """ Stock update """
    if run_backup:
        backup.execute()
    assets = imp_asset.get_assets()

    for asset in assets["assets"]:
        if asset["type"] != "STOCK":
            continue
        if "url_suffix" not in asset:
            continue
        if asset["url_suffix"] == "":
            continue

        try:
            url = config.CONSTANTS["STOCK_URL"] + asset["url_suffix"]
            resp = requests.get(url, verify=False, timeout=5)
            str_val = _find_between(resp.text, '<span class="value">', '</span>')
            str_val = str_val.replace(".", "").replace(",", ".")
            asset["sales_value"] = float(str_val)
        except Exception as ex:
            print(str(ex))
            print(f"Can't update stock {asset['name']}")

    imp_asset.set_assets(assets)
