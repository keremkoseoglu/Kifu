""" Net worth API """

from model import asset
from model.timesheet.activity import Activity
from model.bank import bank_account, credit_card
from model.timesheet.income_tax import IncomeTaxCalculatorFactory
from model.payment import payment


class NetWorthAPI:
    """Net worth API"""

    def __init__(self):
        self._result = {}
        self._sum_val = {"own": 0, "partner": 0, "joint": 0}

    @property
    def result(self) -> dict:
        """Returns net worth"""
        self._result = {"NetWorth": []}
        self._sum_val = {"own": 0, "partner": 0, "joint": 0}

        # Bank account balance
        bank_account_balance = bank_account.get_current_account_balance_sum()
        self._append_result(
            "Bank account balance",
            bank_account_balance["own"],
            bank_account_balance["partner"],
            bank_account_balance["joint"],
        )

        # Reserved balance
        reserved_balance = bank_account.get_reserved_balance()
        self._append_result(
            "Reserved balance",
            reserved_balance["own"] * -1,
            reserved_balance["partner"] * -1,
            reserved_balance["joint"] * -1,
        )

        # Credit card debt
        credit_card_debt = credit_card.get_current_credit_card_debt_sum() * -1
        self._append_result("Credit card debt", credit_card_debt, 0, credit_card_debt)

        # SUM: Liquid cash
        self._append_sum("Cash")

        # Activity earnings
        activity_earning = Activity.get_total_activity_earnings()
        self._append_result("Activity earning", activity_earning, 0, activity_earning)

        # Activity income tax
        inc_tax_rate = IncomeTaxCalculatorFactory.get_instance().default_tax_rate
        activity_tax = activity_earning * inc_tax_rate / 100 * -1
        self._append_result("Activity tax", activity_tax, 0, activity_tax)

        # Payment balance
        payment_balance = payment.get_payment_balance()
        self._append_result("Payment balance", payment_balance, 0, payment_balance)

        # SUM: Short term money
        self._append_sum("Short term money")

        # Reserved balance again
        self._append_result(
            "Reserved balance",
            reserved_balance["own"],
            reserved_balance["partner"],
            reserved_balance["joint"],
        )

        # SUM: Total money
        self._append_sum("Total money")

        # Asset resale
        asset_resales = asset.get_asset_type_resale_value_sum(deduct_income_tax=True)
        for asset_resale in asset_resales:
            self._append_result(
                asset_resale["type"] + " resale",
                asset_resale["own_sales_value"],
                asset_resale["partner_sales_value"],
                asset_resale["joint_sales_value"],
            )

        # SUM: Net worth
        self._append_sum("Net worth")

        # Return
        return self._result

    def _append_result(
        self, title, own_value, partner_value, joint_value, icon: str = ""
    ):
        self._sum_val["own"] += own_value
        self._sum_val["partner"] += partner_value
        self._sum_val["joint"] += joint_value

        entry = {
            "icon": icon,
            "title": title,
            "own_content": own_value,
            "partner_content": partner_value,
            "joint_content": joint_value,
            "own_result": self._sum_val["own"],
            "partner_result": self._sum_val["partner"],
            "joint_result": self._sum_val["joint"],
        }

        self._result["NetWorth"].append(entry)

    def _append_sum(self, title):
        entry = {
            "icon": "∑",
            "title": title,
            "own_content": 0,
            "partner_content": 0,
            "joint_content": 0,
            "own_result": self._sum_val["own"],
            "partner_result": self._sum_val["partner"],
            "joint_result": self._sum_val["joint"],
        }

        self._result["NetWorth"].append(entry)
