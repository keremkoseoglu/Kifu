""" Currency account distribution report """
from report.html_report import HtmlReport
from util import amount
from model import bank_account
from model.currency import CurrencyConverter
import config


class CurrencyAccountDistribution(HtmlReport):
    """ Currency account distribution report """

    _REPORT_NAME = "Currency Account Distribution"

    def _get_html_content(self) -> str:
        chart_list = []

        ##############################
        # HTML table (also prepares chart data)
        ##############################

        output = "<table cellspacing=0 cellpadding=10>"
        output += "<tr><td>Currency</td><td>Total</td><td>Bank</td><td>Home</td><td>Bank</td><td> Home</td></tr>" # pylint: disable=C0301

        currency_conv = CurrencyConverter()

        currencies = bank_account.get_currencies()
        for currency in currencies:
            output += "<tr><td>" + currency + "</td>"
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

            output += "<td align=right>" + amount.get_formatted_amount(currency_sum) + " " + config.CONSTANTS["HOME_CURRENCY_SYMBOL"] + "</td>" # pylint: disable=C0301
            output += "<td align=right>" + amount.get_formatted_amount(bank_sum) + " " + config.CONSTANTS["HOME_CURRENCY_SYMBOL"] + "</td>" # pylint: disable=C0301
            output += "<td align=right>" + amount.get_formatted_amount(home_sum) + " " + config.CONSTANTS["HOME_CURRENCY_SYMBOL"] + "</td>" # pylint: disable=C0301
            output += "<td align=right>" + str(bank_perc) + " %</td>"
            output += "<td align=right>" + str(home_perc) + " %</td>"
            output += "</tr>"

            chart_item = {"currency": currency, "sum": currency_sum}
            chart_list.append(chart_item)

        output += "</table><hr>"

        ##############################
        # Chart
        ##############################

        chart_list.sort(key=lambda x: x["sum"], reverse=True)

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
        for chart_item in chart_list:
            if not first_balance:
                output += ", "
            output += str(round(chart_item["sum"]))
            first_balance = False
        output += "],"

        output += "backgroundColor: ["
        first_balance = True
        balance_pos = 0
        for chart_item in chart_list:
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
        output += "label: 'Currencies'"
        output += "}],"

        output += "labels: ["
        first_balance = True
        for chart_item in chart_list:
            if not first_balance:
                output += ", "
            output += "'" + chart_item["currency"] + "'"
            first_balance = False
        output += "]}, options: {responsive: true} };"

        output += "window.onload = function() {"
        output += "var ctx = document.getElementById('chart-area').getContext('2d');"
        output += "window.myPie = new Chart(ctx, config); };"
        output += "</script>"

        ##############################
        # Flush
        ##############################

        return output

    def _get_report_name(self) -> str:
        return self._REPORT_NAME
