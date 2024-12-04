""" Asset value update module """

from datetime import datetime
from typing import List
import config
from model.asset import get_assets, is_liquid, set_asset
from util.date_time import get_formatted_date


class AssetValueAPI:
    """Asset value API class"""

    @staticmethod
    def get_commodity_values() -> List:
        """Returns commodity values
        Exports: guid, name, sales_value, currency, url
        """
        output = []
        all_assets = get_assets()["assets"]
        all_assets.sort(key=lambda x: x["sales_value"] * x["quantity"], reverse=True)

        for asset in all_assets:
            if is_liquid(asset):
                continue

            url = config.CONSTANTS["COMMODITY_URL"]
            url += asset["url_suffix"]
            if "sorting" not in url:
                url += "&sorting=price_asc"

            out_dict = {
                "guid": asset["guid"],
                "name": asset["name"],
                "sales_value": asset["sales_value"],
                "currency": asset["currency"],
                "url": url,
            }

            output.append(out_dict)

        return output

    @staticmethod
    def set_commodity_values(new_values: List) -> List:
        """Saves asset values
        Needs to import: guid, sales_value, currency
        """
        if len(new_values) <= 0:
            return

        today = get_formatted_date(datetime.now())
        all_assets = get_assets()["assets"]

        for new_value in new_values:
            for asset in all_assets:
                if asset["guid"] != new_value["guid"]:
                    continue
                if (
                    asset["sales_value"] == new_value["sales_value"]
                    and asset["currency"] == new_value["currency"]
                ):
                    continue

                hist_dict = {"date": today, "value": new_value["sales_value"]}

                asset["sales_value"] = new_value["sales_value"]
                asset["currency"] = new_value["currency"]

                if "value_history" not in asset:
                    asset["value_history"] = []
                asset["value_history"].append(hist_dict)

                set_asset(asset)
