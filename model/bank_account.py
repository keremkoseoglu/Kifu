""" Bank account """
import json
from locale import ABDAY_1
import os
from model.currency import CurrencyConverter
import config


_BANK_ACCOUNT_FILE = "bank.json"


def get_accounts_with_currency(currency: str) -> []:
    """ Returns all bank accounts having the given currency """
    output = []

    for bank_account in get_bank_accounts()["bank_accounts"]:
        if bank_account["currency"] == currency:
            output.append(bank_account)

    return output


def get_account_balances_in_both_currencies() -> []:
    """ Account balances in original and home currencies """
    output = []
    accounts = get_bank_accounts()
    currency_converter = CurrencyConverter()

    for account in accounts["bank_accounts"]:
        amount = currency_converter.convert_to_local_currency(
            account["balance"],
            account["currency"])
        output_dict = {
            "name": account["bank_name"] + " - " + account["account_name"],
            "home_balance": amount,
            "original_balance": account["balance"],
            "original_currency": account["currency"],
            "is_investment": account["is_investment"]
        }
        output.append(output_dict)

    return output


def get_bank_accounts():
    """ Returns all bank accounts """
    with open(_get_file_path()) as acc_file:
        json_data = json.load(acc_file)
    return json_data


def get_currencies() -> []:
    """ Returns all currencies in bank accounts """
    output = []

    for bank_account in get_bank_accounts()["bank_accounts"]:
        if bank_account["currency"] not in output:
            output.append(bank_account["currency"])

    return output


def get_current_account_balance_sum() -> float:
    """ Returns money in banks in home currency """
    amount = 0
    accounts = get_bank_accounts()
    currency_converter = CurrencyConverter()

    for account in accounts["bank_accounts"]:
        amount += currency_converter.convert_to_local_currency(
            account["balance"],
            account["currency"])

    return amount


def get_home_account_of_bank(bank: str) -> str:
    """ Returns bank account in home currency """
    for bank_account in get_bank_accounts()["bank_accounts"]:
        if bank_account["bank_name"] == bank and \
            bank_account["currency"] == config.CONSTANTS["HOME_CURRENCY"]:
            return bank_account["account_name"]
    raise Exception(config.CONSTANTS["HOME_CURRENCY"] + " account of " + bank + " not found")


def get_next_investment_account() -> tuple:
    """ Selects and returns the most suitable investment account
    This is the account with the lowest amount
    """
    # Determine list of foreign currencies, sorted by amount ascending
    accs = get_account_balances_in_both_currencies()

    foreign_currency_balances = []
    for acc in accs:
        if acc["original_currency"] == config.CONSTANTS["HOME_CURRENCY"]:
            continue
        found = False
        for fcb in foreign_currency_balances:
            if fcb["original_currency"] == acc["original_currency"]:
                fcb["home_balance"] += acc["home_balance"]
                found = True
        if found:
            continue
        new_fcb = {
            "original_currency": acc["original_currency"],
            "home_balance": acc["home_balance"]
        }
        foreign_currency_balances.append(new_fcb)

    foreign_currency_balances = sorted(foreign_currency_balances, key=lambda x: x["home_balance"])

    # Find investment account with least amount
    next_acc = None
    for fcb in foreign_currency_balances:
        for acc in accs:
            if not acc["is_investment"]:
                continue
            if acc["original_currency"] == fcb["original_currency"]:
                next_acc = acc
                break
        if next_acc is not None:
            break

    # Format & return
    account_parts = next_acc["name"].split()
    acc = ""
    for account_part in account_parts:
        if account_part == "-":
            break
        if acc != "":
            acc += " "
        acc += account_part
    return acc, account_parts[len(account_parts)-1]


def get_vat_account() -> dict:
    """ Returns the default VAT account """
    for bank_account in get_bank_accounts()["bank_accounts"]:
        if bank_account["is_vat"]:
            return bank_account
    raise Exception("VAT account not found")

def get_home_bank_acc_str() -> str:
    """ Returns home bank account text """
    for bank_account in get_bank_accounts()["bank_accounts"]:
        if bank_account["bank_name"] != config.CONSTANTS["DEFAULT_BANK"]:
            continue
        if bank_account["account_name"] != config.CONSTANTS["HOME_CURRENCY"]:
            continue
        result = bank_account["iban"]
        break

    result += " (" + config.CONSTANTS["DEFAULT_BANK"] + " - " + config.CONSTANTS["HOME_CURRENCY"] + ")"

    return result

def _get_file_path():
    return os.path.join(config.CONSTANTS["DATA_DIR_PATH"] + _BANK_ACCOUNT_FILE)
