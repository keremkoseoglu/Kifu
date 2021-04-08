""" Currency account distribution report """
from report.html_report import HtmlReport
from util import amount
from model import bank_account, asset as imp_asset
from model.currency import CurrencyConverter
import config


class CurrencyAccountDistribution(HtmlReport):
    """ Currency account distribution report """

    _REPORT_NAME = "Currency Account Distribution"

    def __init__(self):
        self._chart_list = []
        self._output = ""

    def _append_banks(self):
        currency_conv = CurrencyConverter()
        currencies = bank_account.get_currencies()

        for currency in currencies:
            self._output += "<tr><td>" + currency + "</td>"
            accounts = bank_account.get_accounts_with_currency(currency)
            currency_sum = 0
            home_sum = 0
            bank_sum = 0
            home_perc = 0
            bank_perc = 0

            for account in accounts:
                account_balance = currency_conv.convert_to_local_currency(
                    account["balance"],
                    account["currency"])

                currency_sum += account_balance

                if account["bank_name"] == config.CONSTANTS["HOME_COMPANY"]:
                    home_sum += account_balance
                else:
                    bank_sum += account_balance

            if currency_sum != 0:
                home_perc = int((home_sum / currency_sum) * 100)
                bank_perc = 100 - home_perc

            self._output += "<td align=right>" + amount.get_formatted_amount(currency_sum) + " " + config.CONSTANTS["HOME_CURRENCY_SYMBOL"] + "</td>" # pylint: disable=C0301
            self._output += "<td align=right>" + amount.get_formatted_amount(bank_sum) + " " + config.CONSTANTS["HOME_CURRENCY_SYMBOL"] + "</td>" # pylint: disable=C0301
            self._output += "<td align=right>" + amount.get_formatted_amount(home_sum) + " " + config.CONSTANTS["HOME_CURRENCY_SYMBOL"] + "</td>" # pylint: disable=C0301
            self._output += "<td align=right>" + str(bank_perc) + " %</td>"
            self._output += "<td align=right>" + str(home_perc) + " %</td>"
            self._output += "</tr>"

            chart_item = {"currency": currency, "sum": currency_sum}
            self._chart_list.append(chart_item)

    def _append_assets(self):
        assets = imp_asset.get_asset_type_resale_value_sum(only_liquid=True)

        for asset in assets:
            html = "<tr>"
            html += "<td>" + asset["type"] + "</td>"
            html += "<td align=right>" + amount.get_formatted_amount(asset["sales_value"]) + " " + config.CONSTANTS["HOME_CURRENCY_SYMBOL"] + "</td>" # pylint: disable=C0301
            html += "<td align=right>" + amount.get_formatted_amount(asset["sales_value"]) + " " + config.CONSTANTS["HOME_CURRENCY_SYMBOL"] + "</td>" # pylint: disable=C0301
            html += "<td align=right>" + amount.get_formatted_amount(0) + " " + config.CONSTANTS["HOME_CURRENCY_SYMBOL"] + "</td>" # pylint: disable=C0301
            html += "<td align=right>100 %</td>"
            html += "<td align=right>0 %</td>"
            html += "</tr>"
            self._output += html

            chart_item = {"currency": asset["type"], "sum": asset["sales_value"]}
            self._chart_list.append(chart_item)

    def _append_chart(self):
        ##############################
        # Chart
        ##############################

        self._chart_list.sort(key=lambda x: x["sum"], reverse=True)

        self._output += "<div id='canvas-holder' style='width:100%'>"
        self._output += "<canvas id='chart-area'></canvas>"
        self._output += "</div>"
        self._output += "<script>"
        self._output += "var config = {"
        self._output += "type: 'pie',"
        self._output += "data: {"
        self._output += "datasets: [{"
        self._output += "data: ["

        first_balance = True
        for chart_item in self._chart_list:
            if not first_balance:
                self._output += ", "
            self._output += str(round(chart_item["sum"]))
            first_balance = False
        self._output += "],"

        self._output += "backgroundColor: ["
        first_balance = True
        balance_pos = 0
        for chart_item in self._chart_list:
            if not first_balance:
                self._output += ", "
            if balance_pos == 0:
                color = "006600"
            elif balance_pos == 1:
                color = "008800"
            elif balance_pos == 2:
                color = "00AA00"
            elif balance_pos == 3:
                color = "00CC00"
            elif balance_pos == 4:
                color = "00EE00"
            else:
                color = "AAAAAA"

            self._output += "'#" + color + "'"
            first_balance = False
            balance_pos += 1
        self._output += "],"
        self._output += "label: 'Currencies'"
        self._output += "}],"

        self._output += "labels: ["
        first_balance = True
        for chart_item in self._chart_list:
            if not first_balance:
                self._output += ", "
            self._output += "'" + chart_item["currency"] + "'"
            first_balance = False
        self._output += "]}, options: {responsive: true} };"

        self._output += "window.onload = function() {"
        self._output += "var ctx = document.getElementById('chart-area').getContext('2d');"
        self._output += "window.myPie = new Chart(ctx, config); };"
        self._output += "</script>"

    def _get_html_content(self) -> str:
        self._chart_list = []

        self._output = "<table cellspacing=0 cellpadding=10>"
        self._output += "<tr><td>Currency</td><td>Total</td><td>Bank</td><td>Home</td><td>Bank</td><td> Home</td></tr>" # pylint: disable=C0301
        self._append_banks()
        self._append_assets()
        self._output += "</table><hr>"

        self._append_chart()
        return self._output

    def _get_report_name(self) -> str:
        return self._REPORT_NAME
