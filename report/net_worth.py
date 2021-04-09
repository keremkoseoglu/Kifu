""" Net worth """
from report.html_report import HtmlReport
from model import asset, bank_account, credit_card, payment
from model.activity import Activity
from util import amount


class NetWorth(HtmlReport):
    """ Net worth """

    _REPORT_NAME = "Net Worth"

    @staticmethod
    def _get_table_line(title: str, content: str, result: str):
        return "<tr><td>" + title + "</td><td align=right>" + content + "</td><td align=right>" + result + "</td>" # pylint: disable=C0301

    def _get_html_content(self) -> str:

        # Initialize
        sum_val = 0
        output = "<table cellspacing=20 cellpadding=20>"

        # Titles
        output += NetWorth._get_table_line("<b>Item</b>", "<b>Value</b>", "<b>Sum</b>")

        # Bank account balance
        bank_account_balance = bank_account.get_current_account_balance_sum()
        sum_val += bank_account_balance
        output += NetWorth._get_table_line(
            "Bank account balance",
            amount.get_formatted_amount(bank_account_balance),
            amount.get_formatted_amount(sum_val))

        # Credit card debt
        credit_card_debt = credit_card.get_current_credit_card_debt_sum()
        sum_val -= credit_card_debt
        output += NetWorth._get_table_line(
            "Credit card debt",
            "-" + amount.get_formatted_amount(credit_card_debt),
            amount.get_formatted_amount(sum_val))

        # Activity earnings
        activity_earning = Activity.get_total_activity_earnings()
        sum_val += activity_earning
        output += NetWorth._get_table_line(
            "Activity earning",
            amount.get_formatted_amount(activity_earning),
            amount.get_formatted_amount(sum_val))

        # Payment balance
        payment_balance = payment.get_payment_balance()
        sum_val += payment_balance
        output += NetWorth._get_table_line(
            "Payment balance",
            amount.get_formatted_amount(payment_balance),
            amount.get_formatted_amount(sum_val))

        # Asset resale
        asset_resales = asset.get_asset_type_resale_value_sum(deduct_income_tax=True)
        for asset_resale in asset_resales:
            sum_val += asset_resale["sales_value"]
            output += NetWorth._get_table_line(
                asset_resale["type"] + " resale",
                amount.get_formatted_amount(asset_resale["sales_value"]),
                amount.get_formatted_amount(sum_val))

        # Flush
        output += "</table>"
        return output

    def _get_report_name(self) -> str:
        return self._REPORT_NAME
