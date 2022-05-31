""" Net worth API """
from model import asset
from model.timesheet.activity import Activity
from model.bank import bank_account, credit_card
from model.timesheet.income_tax import IncomeTaxCalculatorFactory
from model.payment import payment


class NetWorthAPI():
    """ Net worth API """
    def __init__(self):
        self._result = {}
        self._sum_val = 0

    @property
    def result(self) -> dict:
        """ Returns net worth """
        self._result = {"NetWorth": []}
        self._sum_val = 0

        # Bank account balance
        bank_account_balance = bank_account.get_current_account_balance_sum()
        self._append_result("Bank account balance", bank_account_balance)

        # Reserved balance
        reserved_balance = bank_account.get_reserved_balance() * -1
        self._append_result("Reserved balance", reserved_balance)

        # Credit card debt
        credit_card_debt = credit_card.get_current_credit_card_debt_sum() * -1
        self._append_result("Credit card debt", credit_card_debt)

        # SUM: Liquid cash
        self._append_sum("Cash")

        # Activity earnings
        activity_earning = Activity.get_total_activity_earnings()
        self._append_result("Activity earning", activity_earning)

        # Activity income tax
        inc_tax_rate = IncomeTaxCalculatorFactory.get_instance().default_tax_rate
        activity_tax = activity_earning * inc_tax_rate / 100 * -1
        self._append_result("Activity tax", activity_tax)

        # Payment balance
        payment_balance = payment.get_payment_balance()
        self._append_result("Payment balance", payment_balance)

        # SUM: Short term cash
        self._append_sum("Money")

        # Asset resale
        asset_resales = asset.get_asset_type_resale_value_sum(deduct_income_tax=True,
                                                              own_percentage_only=True)
        for asset_resale in asset_resales:
            self._append_result(asset_resale["type"] + " resale", asset_resale["sales_value"])

        # Reserved balance again
        reserved_balance *= -1
        self._append_result("Reserved balance", reserved_balance)

        # SUM: Net worth
        self._append_sum("Net worth")

        # Return
        return self._result

    def _append_result(self, title, value, icon: str = ""):
        self._sum_val += value

        entry = {"icon": icon,
                 "title": title,
                 "content": value,
                 "result": self._sum_val}

        self._result["NetWorth"].append(entry)

    def _append_sum(self, title):
        entry = {"icon": "∑",
                 "title": title,
                 "content": 0,
                 "result": self._sum_val}

        self._result["NetWorth"].append(entry)
