from config.constants import DATA_DIR_PATH, HOME_COMPANY, HOME_CURRENCY
import json, os
from model.currency import CurrencyConverter

_BANK_ACCOUNT_FILE = "bank_account.json"


def get_accounts_with_currency(currency: str) -> []:
    output = []

    for bank_account in get_bank_accounts()["bank_accounts"]:
        if bank_account["currency"] == currency:
            output.append(bank_account)

    return output


def get_account_balances_in_both_currencies() -> []:
    output = []
    accounts = get_bank_accounts()
    currency_converter = CurrencyConverter()

    for account in accounts["bank_accounts"]:
        amount = currency_converter.convert_to_local_currency(account["balance"], account["currency"])
        output_dict = {
            "name": account["bank_name"] + " - " + account["account_name"],
            "home_balance": amount,
            "original_balance": account["balance"],
            "original_currency": account["currency"]
        }
        output.append(output_dict)

    return output


def get_bank_accounts():
    with open(_get_file_path()) as f:
        json_data = json.load(f)
    return json_data


def get_currencies() -> []:
    output = []

    for bank_account in get_bank_accounts()["bank_accounts"]:
        if bank_account["currency"] not in output:
            output.append(bank_account["currency"])

    return output


def get_current_account_balance_sum() -> float:
    amount = 0
    accounts = get_bank_accounts()
    currency_converter = CurrencyConverter()

    for account in accounts["bank_accounts"]:
        amount += currency_converter.convert_to_local_currency(account["balance"], account["currency"])

    return amount


def get_home_account_of_bank(bank: str) -> str:
    for bank_account in get_bank_accounts()["bank_accounts"]:
        if bank_account["bank_name"] == bank and bank_account["currency"] == HOME_CURRENCY:
            return bank_account["account_name"]
    raise Exception(HOME_CURRENCY + " account of " + bank + " not found")


def get_next_investment_account() -> tuple:
    accs = get_account_balances_in_both_currencies()
    inv_accs = []
    for acc in accs:
        if acc["original_currency"] != HOME_CURRENCY and acc["name"].find(HOME_COMPANY) == -1:
            inv_accs.append(acc)

    next_acc = inv_accs[0]

    for acc in inv_accs:
        if acc["home_balance"] < next_acc["home_balance"]:
            next_acc = acc

    ba = next_acc["name"].split()
    acc = ""
    for b in ba:
        if b == "-":
            break
        if acc != "":
            acc += " "
        acc += b
    return acc, ba[len(ba)-1]


def get_vat_account() -> dict:
    for bank_account in get_bank_accounts()["bank_accounts"]:
        if bank_account["is_vat"]:
            return bank_account
    raise Exception("VAT account not found")


def _get_file_path():
    return os.path.join(DATA_DIR_PATH + _BANK_ACCOUNT_FILE)