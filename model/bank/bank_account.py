""" Bank account """

import json
import os
from typing import List
from model.currency import CurrencyConverter
import config


_BANK_ACCOUNT_FILE = "bank.json"


def get_accounts_with_currency(currency: str, own: bool = True) -> List:
    """Returns all bank accounts having the given currency"""
    output = []

    for bank_account in get_bank_accounts()["bank_accounts"]:
        if bank_account["currency"] == currency:
            if not own or (own and bank_account["own_percentage"] > 0):
                output.append(bank_account)

    return output


def get_account_balances_in_both_currencies() -> List:
    """Account balances in original and home currencies"""
    output = []
    accounts = get_bank_accounts()
    currency_converter = CurrencyConverter()

    for account in accounts["bank_accounts"]:
        own = account["balance"] * account["own_percentage"] / 100
        partner = account["balance"] - own

        amount_home = currency_converter.convert_to_local_currency(
            own, account["currency"]
        )

        partner_amount_home = currency_converter.convert_to_local_currency(
            partner, account["currency"]
        )

        joint_amount_home = amount_home + partner_amount_home

        reserved = 0

        if "reserved" in account:
            for res_entry in account["reserved"]:
                reserved += res_entry["amount"]

        reserved_home = currency_converter.convert_to_local_currency(
            reserved, account["currency"]
        )

        usable = account["balance"] - reserved
        usable_home = joint_amount_home - reserved_home

        output_dict = {
            "name": account["bank_name"] + " - " + account["account_name"],
            "home_balance": amount_home,
            "partner_home_balance": partner_amount_home,
            "joint_home_balance": joint_amount_home,
            "original_balance": own,
            "partner_original_balance": partner,
            "joint_original_balance": account["balance"],
            "original_currency": account["currency"],
            "is_investment": account["is_investment"],
            "original_reserved": reserved,
            "home_reserved": reserved_home,
            "original_usable": usable,
            "home_usable": usable_home,
        }
        output.append(output_dict)

    return output


def get_bank_accounts():
    """Returns all bank accounts"""
    with open(_get_file_path(), encoding="utf-8") as acc_file:
        json_data = json.load(acc_file)
    return json_data


def get_currencies() -> List:
    """Returns all currencies in bank accounts"""
    output = []

    for bank_account in get_bank_accounts()["bank_accounts"]:
        if bank_account["currency"] not in output:
            output.append(bank_account["currency"])

    return output


def get_current_account_balance_sum() -> dict:
    """Returns money in banks in home currency"""
    result = {"own": 0, "partner": 0, "joint": 0}
    accounts = get_bank_accounts()
    currency_converter = CurrencyConverter()

    for account in accounts["bank_accounts"]:
        joint_amount = currency_converter.convert_to_local_currency(
            account["balance"], account["currency"]
        )

        own_amount = joint_amount * account["own_percentage"] / 100
        partner_amount = joint_amount - own_amount

        result["own"] += own_amount
        result["partner"] += partner_amount
        result["joint"] += joint_amount

    return result


def get_home_account_of_bank(bank: str) -> str:
    """Returns bank account in home currency"""
    for bank_account in get_bank_accounts()["bank_accounts"]:
        if (
            bank_account["bank_name"] == bank
            and bank_account["currency"] == config.CONSTANTS["HOME_CURRENCY"]
        ):
            return bank_account["account_name"]
    raise Exception(f"{config.CONSTANTS['HOME_CURRENCY']} account of {bank} not found")


def get_next_investment_account() -> tuple:
    """Selects and returns the most suitable investment account
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
            "home_balance": acc["home_balance"],
        }
        foreign_currency_balances.append(new_fcb)

    foreign_currency_balances = sorted(
        foreign_currency_balances, key=lambda x: x["home_balance"]
    )

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
    return acc, account_parts[len(account_parts) - 1]


def get_vat_account() -> dict:
    """Returns the default VAT account"""
    for bank_account in get_bank_accounts()["bank_accounts"]:
        if "is_vat" in bank_account and bank_account["is_vat"]:
            return bank_account
    raise Exception("VAT account not found")


def get_home_bank_acc_str() -> str:
    """Returns home bank account text"""
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


def get_reserved_balance() -> dict:
    """Returns the reserved bank account balance"""
    output = {"own": 0, "partner": 0, "joint": 0}
    home_curr = config.CONSTANTS["HOME_CURRENCY"]
    curr_conv = CurrencyConverter()

    for bank_account in get_bank_accounts()["bank_accounts"]:
        if not "reserved" in bank_account:
            continue
        for balance in bank_account["reserved"]:
            joint_reserved_amt = (
                balance["amount"]
                if bank_account["currency"] == home_curr
                else curr_conv.convert_to_local_currency(
                    balance["amount"], bank_account["currency"]
                )
            )

            own_reserved_amt = joint_reserved_amt * bank_account["own_percentage"] / 100
            partner_reserved_amt = joint_reserved_amt - own_reserved_amt

            output["own"] += own_reserved_amt
            output["partner"] += partner_reserved_amt
            output["joint"] += joint_reserved_amt

    return output


def add_amount_to_vat_account(delta: float, currency: str):
    """Updates VAT account"""
    add_amount_to_account_with_property("is_vat", True, delta, currency)


def add_amount_to_income_tax_account(delta: float, currency: str):
    """Updates income tax account"""
    add_amount_to_account_with_property("is_income_tax", True, delta, currency)


def add_amount_to_account_with_property(
    prop_key: str, prop_val, delta: float, currency: str
):
    """Updates any account"""
    curr_conv = CurrencyConverter()
    accounts = get_bank_accounts()

    for account in accounts["bank_accounts"]:
        if prop_key in account and account[prop_key] == prop_val:
            converted_delta = curr_conv.convert_to_currency(
                delta, currency, account["currency"]
            )
            account["balance"] += converted_delta
            _save_bank_accounts(accounts)
            return


def _get_file_path():
    return os.path.join(config.CONSTANTS["DATA_DIR_PATH"] + _BANK_ACCOUNT_FILE)


def _save_bank_accounts(accounts: dict):
    with open(_get_file_path(), "w", encoding="utf-8") as ba_file:
        json.dump(accounts, ba_file, indent=3)
