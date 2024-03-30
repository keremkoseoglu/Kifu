""" Credit card module """
from dataclasses import dataclass
import json
import os
from typing import List
from model.currency import CurrencyConverter
import config


_CREDIT_CARD_FILE = "bank.json"

@dataclass
class CreditCardDebt: # pylint: disable=R0903
    """ Credit card debt """
    bank_name: str
    card_name: str
    amount: int

@dataclass
class CreditCardDebtList: # pylint: disable=R0903
    """ Credit card debt list """
    currency: str
    debts: List[CreditCardDebt] = None

    def __post_init__(self):
        if self.debts is None:
            self.debts = []


def get_credit_cards():
    """ Returns a dict of credit cards """
    with open(_get_file_path(), encoding="utf-8") as cc_file:
        json_data = json.load(cc_file)
    return json_data


def get_credit_card_debts() -> CreditCardDebtList:
    """ Returns all credit card debts """
    output = CreditCardDebtList(config.CONSTANTS["HOME_CURRENCY"])
    credit_cards = get_credit_cards()
    currency_converter = CurrencyConverter()

    for credit_card in credit_cards["credit_cards"]:
        debt = credit_card["credit_limit"] - credit_card["usable_limit"]
        if debt <= 0:
            continue
        local_debt = currency_converter.convert_to_local_currency(debt, credit_card["currency"])
        cc_debt = CreditCardDebt(credit_card["bank_name"], credit_card["card_name"], local_debt)
        output.debts.append(cc_debt)

    return output


def get_current_credit_card_debt_sum() -> float:
    """ Returns the total sum of credit card debts """
    output = 0
    debts = get_credit_card_debts()
    for debt in debts.debts:
        output += debt.amount
    return output


def _get_file_path():
    return os.path.join(config.CONSTANTS["DATA_DIR_PATH"] + _CREDIT_CARD_FILE)
