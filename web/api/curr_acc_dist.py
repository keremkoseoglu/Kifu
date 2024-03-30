""" Currency account distribution API """

from model import asset as imp_asset
from model.bank import bank_account
from model.currency import CurrencyConverter
import config
from web.api.chart import get_pie_dict


class CurrAccDistAPI:
    """Currency account distribution API"""

    def __init__(self):
        self._out = {}
        self._built = False

    @property
    def result(self) -> dict:
        """Returns distribution"""
        if not self._built:
            self._out = {"Currencies": [], "PieChart": {}}
            self._read_bank_accounts()
            self._read_assets()
            self._build_pie()
            self._built = True

        return self._out

    def _read_bank_accounts(self):
        currency_conv = CurrencyConverter()
        currencies = bank_account.get_currencies()

        for currency in currencies:
            accounts = bank_account.get_accounts_with_currency(currency)
            currency_sum = 0
            home_sum = 0
            bank_sum = 0
            home_perc = 0
            bank_perc = 0

            for account in accounts:
                account_balance = currency_conv.convert_to_local_currency(
                    account["balance"], account["currency"]
                )

                currency_sum += account_balance

                if account["bank_name"] == config.CONSTANTS["HOME_COMPANY"]:
                    home_sum += account_balance
                else:
                    bank_sum += account_balance

            if currency_sum != 0:
                home_perc = int((home_sum / currency_sum) * 100)
                bank_perc = 100 - home_perc

            curr_dict = {
                "currency": currency,
                "currency_sum": currency_sum,
                "bank_sum": bank_sum,
                "home_sum": home_sum,
                "bank_perc": bank_perc,
                "home_perc": home_perc,
            }

            self._out["Currencies"].append(curr_dict)

    def _read_assets(self):
        assets = imp_asset.get_asset_type_resale_value_sum(
            only_liquid=True, deduct_income_tax=True
        )

        for asset in assets:
            curr_dict = {
                "currency": asset["type"],
                "currency_sum": asset["own_sales_value"],
                "bank_sum": asset["own_sales_value"],
                "home_sum": 0,
                "bank_perc": 100,
                "home_perc": 0,
            }

            self._out["Currencies"].append(curr_dict)

    def _build_pie(self):
        self._out["PieChart"] = get_pie_dict(
            entries=self._out["Currencies"],
            label_fld="currency",
            val_fld="currency_sum",
        )
