""" Bank account balance report """
from report.html_report import HtmlReport
from model import asset, bank_account
from util import amount
import config


class BankAccountBalance(HtmlReport):
    """ Bank account balance report """

    _REPORT_NAME = "Bank Account Balance"

    @staticmethod
    def _get_balances() -> []:
        result = []
        bank_balances = bank_account.get_account_balances_in_both_currencies()
        asset_balances = asset.get_liquid_assets_in_both_currencies(deduct_income_tax=True)

        for bank_balance in bank_balances:
            result.append(bank_balance)
        for asset_balance in asset_balances:
            result.append(asset_balance)

        return result

    def _get_html_content(self) -> str:
        balances = BankAccountBalance._get_balances()

        output = "<table border=0 cellspacing=0 cellpadding=10>"

        for balance in balances:
            output += "<tr>"
            output += "<td>" + balance["name"] + "</td>"
            output += "<td align=right>" + amount.get_formatted_amount(balance["original_balance"]) + " " + balance["original_currency"] + "</td>" # pylint: disable=C0301
            output += "<td align=right>" + amount.get_formatted_amount(balance["home_balance"]) + " " + config.CONSTANTS["HOME_CURRENCY_SYMBOL"] + "</td>" # pylint: disable=C0301
            output += "</tr>"

        output += "</table><hr>"

        balances.sort(key=lambda x: x["home_balance"], reverse=True)

        output += "<div id='canvas-holder' style='width:100%'>"
        output += "<canvas id='chart-area'></canvas>"
        output += "</div>"
        output += "<script>"
        output += "var config = {"
        output += "type: 'pie',"
        output += "data: {"
        output += "datasets: [{"
        output += "data: ["

        first_balance = True
        for balance in balances:
            if not first_balance:
                output += ", "
            output += str(round(balance["home_balance"]))
            first_balance = False
        output += "],"

        output += "backgroundColor: ["
        first_balance = True
        balance_pos = 0
        for balance in balances:
            if not first_balance:
                output += ", "
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

            output += "'#" + color + "'"
            first_balance = False
            balance_pos += 1
        output += "],"
        output += "label: 'Balances'"
        output += "}],"

        output += "labels: ["
        first_balance = True
        for balance in balances:
            if not first_balance:
                output += ", "
            output += "'" + balance["name"] + "'"
            first_balance = False
        output += "]}, options: {responsive: true} };"

        output += "window.onload = function() {"
        output += "var ctx = document.getElementById('chart-area').getContext('2d');"
        output += "window.myPie = new Chart(ctx, config); };"
        output += "</script>"
        return output

    def _get_report_name(self) -> str:
        return self._REPORT_NAME
