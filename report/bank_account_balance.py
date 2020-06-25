""" Bank account balance report """
from report.html_report import HtmlReport
from model import bank_account
from util import amount
import config


class BankAccountBalance(HtmlReport):
    """ Bank account balance report """

    _REPORT_NAME = "Bank Account Balance"

    def _get_html_content(self) -> str:
        output = "<table border=0 cellspacing=0 cellpadding=10>"

        for balance in bank_account.get_account_balances_in_both_currencies():
            output += "<tr>"
            output += "<td>" + balance["name"] + "</td>"
            output += "<td align=right>" + amount.get_formatted_amount(balance["original_balance"]) + " " + balance["original_currency"] + "</td>" # pylint: disable=C0301
            output += "<td align=right>" + amount.get_formatted_amount(balance["home_balance"]) + " " + config.CONSTANTS["HOME_CURRENCY_SYMBOL"] + "</td>" # pylint: disable=C0301
            output += "</tr>"

        output += "</table>"
        return output

    def _get_report_name(self) -> str:
        return self._REPORT_NAME
