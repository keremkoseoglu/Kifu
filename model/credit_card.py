from config.constants import *
import json, os
from model.currency import CurrencyConverter

_CREDIT_CARD_FILE = "credit_card.json"


def get_credit_cards():
    with open(_get_file_path()) as f:
        json_data = json.load(f)
    return json_data


def get_current_credit_card_debt_sum() -> float:
    amount = 0
    credit_cards = get_credit_cards()
    currency_converter = CurrencyConverter()

    for cc in credit_cards["credit_cards"]:
        debt = cc["credit_limit"] - cc["usable_limit"]
        amount += currency_converter.convert_to_local_currency(debt, cc["currency"])

    return amount


def _get_file_path():
    return os.path.join(DATA_DIR_PATH + _CREDIT_CARD_FILE)