""" Asset profit API module """
from copy import deepcopy
from model import asset as imp_asset
from model.currency import CurrencyConverter, OldCurrencyConverter
from util import date_time

class AssetProfitAPI():
    """ Asset profit API class """

    def __init__(self) -> None:
        self._curr_conv = CurrencyConverter()

    @property
    def result(self) -> dict:
        """ Returns result """
        out = {"Profits": [],
               "Sums": {"liquid_sales": 0,
                        "liquid_profit": 0,
                        "sales": 0,
                        "liquid_sales_home": 0,
                        "liquid_profit_home": 0,
                        "sales_home": 0}}

        assets = imp_asset.get_assets(deduct_income_tax=True)
        assets["assets"].sort(key=lambda x: imp_asset.is_liquid(x["type"]), reverse=True)

        for asset in assets["assets"]:
            asset_profit = self._calc_asset_profit(asset)

            history = ""
            prev_hist_val = 0
            if "value_history" in asset:
                for history_entry in asset["value_history"]:
                    hist_asset = deepcopy(asset)
                    hist_asset["sales_value"] = history_entry["value"]
                    hist_profit = self._calc_asset_profit(hist_asset)

                    if history != "":
                        if hist_profit["usd_profit"] > prev_hist_val:
                            history += " ↑ "
                        else:
                            history += " ↓ "
                    history += str(round(hist_profit["usd_profit"]))
                    prev_hist_val = hist_profit["usd_profit"]

            asset_dict = deepcopy(asset_profit)
            asset_dict["name"] = asset["name"]
            asset_dict["purchase_date"] = date_time.get_formatted_date(asset_profit["purchase_date"]) # pylint: disable=C0301
            asset_dict["quantity"] = asset["quantity"]
            asset_dict["history"] = history

            out["Profits"].append(asset_dict)

            if imp_asset.is_liquid(asset["type"]):
                out["Sums"]["liquid_sales"] += int(asset_dict["actual_usd_total"])
                out["Sums"]["liquid_profit"] += int(asset_dict["usd_profit"])
            out["Sums"]["sales"] += int(asset_dict["actual_usd_total"])

        out["Sums"]["liquid_sales_home"] = int(self._curr_conv.convert_to_local_currency(
            out["Sums"]["liquid_sales"],
            "USD"))

        out["Sums"]["liquid_profit_home"] = int(self._curr_conv.convert_to_local_currency(
            out["Sums"]["liquid_profit"],
            "USD"))

        out["Sums"]["sales_home"] = int(self._curr_conv.convert_to_local_currency(
            out["Sums"]["sales"],
            "USD"))

        return out

    def _calc_asset_profit(self, asset: dict) -> dict:
        purchase_date = date_time.parse_json_date(asset["purchase_date"])
        old_currency_converter = OldCurrencyConverter(purchase_date)

        purchase_value = self._curr_conv.convert_to_local_currency(asset["purchase_value"],
                                                                   asset["currency"])

        purchase_total = asset["quantity"] * purchase_value

        purchase_usd_total = old_currency_converter.convert_to_foreign_currency(purchase_total,
                                                                                "USD")

        sales_value = self._curr_conv.convert_to_local_currency(asset["sales_value"],
                                                                asset["currency"])

        sales_total = asset["quantity"] * sales_value

        actual_usd_price = self._curr_conv.convert_to_foreign_currency(sales_value,
                                                                       "USD")

        actual_usd_total = asset["quantity"] * actual_usd_price

        usd_profit = actual_usd_total - purchase_usd_total
        if purchase_usd_total == 0:
            perc_profit = 0
        else:
            perc_profit = (usd_profit / purchase_usd_total) * 100

        result = {
            "purchase_date": purchase_date,
            "purchase_value": purchase_value,
            "purchase_total": purchase_total,
            "purchase_usd_total": purchase_usd_total,
            "sales_value": sales_value,
            "sales_total": sales_total,
            "actual_usd_price": actual_usd_price,
            "actual_usd_total": actual_usd_total,
            "usd_profit": usd_profit,
            "perc_profit": perc_profit
        }

        return result
