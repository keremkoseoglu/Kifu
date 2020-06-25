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

        output += "</table>"
        return output

    def _get_report_name(self) -> str:
        return self._REPORT_NAME
