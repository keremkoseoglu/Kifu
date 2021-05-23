""" Investment adviser module """
import os
import json
import config
from model.bank_account import get_next_investment_account

_INVEST_FILE = "invest.json"

def _get_file_path() -> str:
    return os.path.join(config.CONSTANTS["DATA_DIR_PATH"] + _INVEST_FILE)


class InvestmentAdviser:
    """ Investment adviser class """
    def __init__(self):
        file_path = _get_file_path()
        with open(file_path) as inv_file:
            self._invest = json.load(inv_file)

    def advise(self, amount: float) -> []:
        """ Advise investment """
        result = []

        for inv in self._invest:
            if inv["percentage"] <= 0:
                continue
            entry_amount = amount * inv["percentage"] / 100
            entry = {"bank": "", "account": "", "amount": entry_amount}

            if inv["type"] == "CURRENCY":
                inv_bank, inv_acc = get_next_investment_account()
                entry["bank"] = inv_bank
                entry["account"] = inv_acc
            elif inv["type"] == "STOCK":
                entry["bank"] = inv["company"]
                entry["account"] = inv["type"]
            elif inv["type"] == "CRYPTO":
                entry["bank"] = inv["company"]
                entry["account"] = inv["type"]
            else:
                raise Exception("Unknown investment type: " + inv["type"])

            result.append(entry)
        return result
