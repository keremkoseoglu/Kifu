""" Net worth API """
from model import asset, bank_account, credit_card, payment
from model.activity import Activity
from model.income_tax import IncomeTaxCalculatorFactory


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

        # Credit card debt
        credit_card_debt = credit_card.get_current_credit_card_debt_sum() * -1
        self._append_result("Credit card debt", credit_card_debt)

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

        # Asset resale
        asset_resales = asset.get_asset_type_resale_value_sum(deduct_income_tax=True)
        for asset_resale in asset_resales:
            self._append_result(asset_resale["type"] + " resale", asset_resale["sales_value"])

        # Return
        return self._result

    def _append_result(self, title, value):
        self._sum_val += value

        entry = {"title": title,
                 "content": value,
                 "result": self._sum_val}

        self._result["NetWorth"].append(entry)
