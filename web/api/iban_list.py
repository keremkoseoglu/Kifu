""" Iban list API """
from model import bank_account
from model.company import Company
import config

class IbanListAPI():
    """ Iban list API """

    def __init__(self):
        self._company = Company(config.CONSTANTS["HOME_COMPANY"])

    @property
    def result(self) -> dict:
        """ Returns net worth """
        result = {"Ibans": []}

        bank_accounts = bank_account.get_bank_accounts()

        for acc in bank_accounts["bank_accounts"]:
            if "iban" not in acc:
                continue
            entry = {"account": acc["bank_name"] + " (" + acc["account_name"] + ")",
                     "person": self._company.contact_person,
                     "iban": acc["iban"]}
            result["Ibans"].append(entry)

        return result
