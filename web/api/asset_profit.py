""" Asset profit API module """
from model import asset as imp_asset
from model.currency import CurrencyConverter, OldCurrencyConverter
from util import date_time

class AssetProfitAPI():
    """ Asset profit API class """

    @property
    def result(self) -> dict:
        """ Returns result """
        out = {"Profits": []}

        assets = imp_asset.get_assets(deduct_income_tax=True)
        currency_converter = CurrencyConverter()

        for asset in assets["assets"]:
            purchase_date = date_time.parse_json_date(asset["purchase_date"])
            old_currency_converter = OldCurrencyConverter(purchase_date)

            purchase_value = currency_converter.convert_to_local_currency(asset["purchase_value"],
                                                                          asset["currency"])

            purchase_total = asset["quantity"] * purchase_value

            purchase_usd_total = old_currency_converter.convert_to_foreign_currency(purchase_total,
                                                                                    "USD")

            sales_value = currency_converter.convert_to_local_currency(asset["sales_value"],
                                                                       asset["currency"])

            sales_total = asset["quantity"] * sales_value

            actual_usd_price = currency_converter.convert_to_foreign_currency(sales_value,
                                                                              "USD")

            actual_usd_total = asset["quantity"] * actual_usd_price

            usd_profit = actual_usd_total - purchase_usd_total
            if purchase_usd_total == 0:
                perc_profit = 0
            else:
                perc_profit = (usd_profit / purchase_usd_total) * 100

            asset_dict = {"name": asset["name"],
                          "purchase_date": date_time.get_formatted_date(purchase_date),
                          "quantity": asset["quantity"],
                          "purchase_value": purchase_value,
                          "purchase_total": purchase_total,
                          "purchase_usd_total": purchase_usd_total,
                          "sales_value": sales_value,
                          "sales_total": sales_total,
                          "actual_usd_total": actual_usd_total,
                          "usd_profit": usd_profit,
                          "perc_profit": perc_profit}

            out["Profits"].append(asset_dict)

        return out
