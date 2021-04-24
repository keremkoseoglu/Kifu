""" Invoice JSON file reader """
from typing import List
from os import path
import json
from datetime import date
import config
from util.date_time import parse_json_date, get_months_between_dates

_INVOICE_FILE = "invoice.json"

def get_file_path():
    """ Returns invoice file path """
    return path.join(config.CONSTANTS["DATA_DIR_PATH"] + _INVOICE_FILE)

def get_invoices() -> dict:
    """ Returns current invoices """
    with open(get_file_path()) as invoice_file:
        json_data = json.load(invoice_file)
    return json_data

def get_invoices_of_last_year() -> List[dict]:
    """ Returns invoices of last 12 months """
    out = []
    today = date.today()
    invoices = get_invoices()
    for invoice in invoices["invoices"]:
        inv_date = parse_json_date(invoice["invoice_date"])
        month_diff = get_months_between_dates(inv_date, today)
        if month_diff <= 12:
            out.append(invoice)
    if len(out) < 12:
        raise Exception("Not enough invoices")
    return out

def get_invoices_of_fiscal_year(year: int) -> List[dict]:
    """ Returns invoices of given fiscal year """
    out = []
    invoices = get_invoices()
    for invoice in invoices["invoices"]:
        inv_date = parse_json_date(invoice["invoice_date"])
        if inv_date.year == year:
            out.append(invoice)
    return out
