from report.html_report import HtmlReport
from model import asset, bank_account, credit_card, payment
from model.activity import Activity
from util import amount


class NetWorth(HtmlReport):

    _REPORT_NAME = "Net Worth"

    def _get_table_line(self, title: str, content: str, result: str):
        return "<tr><td>" + title + "</td><td align=right>" + content + "</td><td align=right>" + result + "</td>"

    def _get_html_content(self) -> str:

        # Initialize
        sum = 0
        output = "<table cellspacing=20 cellpadding=20>"

        # Titles
        output += self._get_table_line("<b>Item</b>", "<b>Value</b>", "<b>Sum</b>")

        # Bank account balance
        bank_account_balance = bank_account.get_current_account_balance_sum()
        sum += bank_account_balance
        output += self._get_table_line("Bank account balance", amount.get_formatted_amount(bank_account_balance), amount.get_formatted_amount(sum))

        # Credit card debt
        credit_card_debt = credit_card.get_current_credit_card_debt_sum()
        sum -= credit_card_debt
        output += self._get_table_line("Credit card debt", "-" + amount.get_formatted_amount(credit_card_debt), amount.get_formatted_amount(sum))

        # Activity earnings
        activity_earning = Activity.get_total_activity_earnings()
        sum += activity_earning
        output += self._get_table_line("Activity earning", amount.get_formatted_amount(activity_earning), amount.get_formatted_amount(sum))

        # Payment balance
        payment_balance = payment.get_payment_balance()
        sum += payment_balance
        output += self._get_table_line("Payment balance", amount.get_formatted_amount(payment_balance), amount.get_formatted_amount(sum))

        # Asset resale
        asset_resale = asset.get_asset_resale_value_sum()
        sum += asset_resale
        output += self._get_table_line("Asset resale", amount.get_formatted_amount(asset_resale), amount.get_formatted_amount(sum))

        # Flush

        output += "</table>"
        return output

    def _get_report_name(self) -> str:
        return self._REPORT_NAME