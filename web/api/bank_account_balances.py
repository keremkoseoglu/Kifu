""" Bank account balance API """
from model import asset, bank_account
from web.api.chart import get_pie_dict

class BankAccountBalanceAPI():
    """ Bank account balance API """

    @property
    def result(self) -> dict:
        """ Bank account balances """
        out = {"Balances": [],
               "PieChart": {}}

        # Balances
        bank_balances = bank_account.get_account_balances_in_both_currencies()
        asset_balances = asset.get_liquid_assets_in_both_currencies(deduct_income_tax=True,
                                                                    own_percentage_only=True)

        for bank_balance in bank_balances:
            out["Balances"].append(bank_balance)
        for asset_balance in asset_balances:
            out["Balances"].append(asset_balance)

        # Pie Chart
        out["PieChart"] = get_pie_dict(entries=out["Balances"],
                                       label_fld="name",
                                       val_fld="home_balance")

        # Flush
        return out
