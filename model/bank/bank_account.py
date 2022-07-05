""" Bank account """
import json
import os
from typing import List
from model.currency import CurrencyConverter
import config

_BANK_ACCOUNT_FILE = "bank.json"

def get_accounts_with_currency(currency: str) -> List:
    """ Returns all bank accounts having the given currency """
    output = []

    for bank_account in get_bank_accounts()["bank_accounts"]:
        if bank_account["currency"] == currency:
            output.append(bank_account)

    return output


def get_account_balances_in_both_currencies() -> List:
    """ Account balances in original and home currencies """
    output = []
    accounts = get_bank_accounts()
    currency_converter = CurrencyConverter()

    for account in accounts["bank_accounts"]:
        amount_home = currency_converter.convert_to_local_currency(account["balance"],
                                                                   account["currency"])

        reserved = 0

        if "reserved" in account:
            for res_entry in account["reserved"]:
                reserved += res_entry["amount"]

        reserved_home = currency_converter.convert_to_local_currency(reserved,
                                                                     account["currency"])

        usable = account["balance"] - reserved
        usable_home = amount_home - reserved_home

        output_dict = {
            "name": account["bank_name"] + " - " + account["account_name"],
            "home_balance": amount_home,
            "original_balance": account["balance"],
            "original_currency": account["currency"],
            "is_investment": account["is_investment"],
            "original_reserved": reserved,
            "home_reserved": reserved_home,
            "original_usable": usable,
            "home_usable": usable_home
        }
        output.append(output_dict)

    return output


def get_bank_accounts():
    """ Returns all bank accounts """
    with open(_get_file_path(), encoding="utf-8") as acc_file:
        json_data = json.load(acc_file)
    return json_data


def get_currencies() -> List:
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
    raise Exception(f"{config.CONSTANTS['HOME_CURRENCY']} account of {bank} not found")


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

    result += " (" + config.CONSTANTS["DEFAULT_BANK"]
    result += " - " + config.CONSTANTS["HOME_CURRENCY"] + ")"

    return result

def get_reserved_balance() -> float:
    """ Returns the reserved bank account balance """
    output = 0
    home_curr = config.CONSTANTS["HOME_CURRENCY"]
    curr_conv = CurrencyConverter()

    for bank_account in get_bank_accounts()["bank_accounts"]:
        if not "reserved" in bank_account:
            continue
        for balance in bank_account["reserved"]:
            reserved_amt = balance["amount"] \
                            if bank_account["currency"] == home_curr \
                            else curr_conv.convert_to_local_currency( balance["amount"],
                                                                      bank_account["currency"])

            output += reserved_amt

    return output

def _get_file_path():
    return os.path.join(config.CONSTANTS["DATA_DIR_PATH"] + _BANK_ACCOUNT_FILE)