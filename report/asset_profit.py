""" Asset profit """
from typing import List
from time import sleep
from report.html_report import HtmlReport
from model import asset as imp_asset
from model.currency import CurrencyConverter
from util import amount, date_time, currency_update


class AssetProfit(HtmlReport):
    """ Asset profit """

    _REPORT_NAME = "Asset Profit"

    def __init__(self):
        self._result = ""

    def _append_line(self, cols: List[str]):
        line = "<tr>"
        for col in cols:
            line += "<td align=right>"
            line += col
            line += "</td>"
        line += "</tr>"
        self._result += line

    def _append_titles(self):
        cols = ["Name",
                "Pur date",
                "Quantity",
                "Pur - Price",
                "Pur - Value",
                "Pur - USD value",
                "Act - Price",
                "Act - Value",
                "Act - USD value",
                "Profit - USD",
                "Profit - %"]

        self._append_line(cols)

    def _append_assets(self):
        assets = imp_asset.get_assets()
        currency_converter = CurrencyConverter()
        actual_usd_curr = currency_converter.get_local_conversion_rate("USD")

        for asset in assets["assets"]:
            purchase_date = date_time.parse_json_date(asset["purchase_date"])
            old_usd = currency_update.get_old_currency(purchase_date, "USD")
            sleep(1)

            purchase_value = currency_converter.convert_to_local_currency(
                asset["purchase_value"],
                asset["currency"])

            purchase_total = asset["quantity"] * purchase_value
            purchase_usd_total = purchase_total / old_usd

            sales_value = currency_converter.convert_to_local_currency(
                asset["sales_value"],
                asset["currency"])

            sales_total = asset["quantity"] * sales_value
            actual_usd_price = sales_value / actual_usd_curr
            actual_usd_total = asset["quantity"] * actual_usd_price

            usd_profit = actual_usd_total - purchase_usd_total
            perc_profit = (usd_profit / purchase_usd_total) * 100

            cols = [asset["name"],
                    date_time.get_formatted_date(purchase_date),
                    str(asset["quantity"]),
                    amount.get_formatted_amount(purchase_value),
                    amount.get_formatted_amount(purchase_total),
                    amount.get_formatted_amount(purchase_usd_total),
                    amount.get_formatted_amount(sales_value),
                    amount.get_formatted_amount(sales_total),
                    amount.get_formatted_amount(actual_usd_total),
                    amount.get_formatted_amount(usd_profit),
                    amount.get_formatted_amount(perc_profit)]

            self._append_line(cols)

    def _get_html_content(self) -> str:
        self._result = "<table border=1 cellpadding=3>"
        self._append_titles()
        self._append_assets()
        self._result += "</table>"
        return self._result

    def _get_report_name(self) -> str:
        return self._REPORT_NAME
