""" Currency update """
import datetime
import requests
import xmltodict
from model import currency
import config
from util import date_time

def get_old_currencies(date: datetime) -> dict:
    """ Returns the currencies in a former date
    https://www.tcmb.gov.tr/kurlar/202001/15012020.xml
    """
    year = str(date.year)
    month = date_time.get_two_digit_month(date.month)
    day = date_time.get_two_digit_month(date.day)

    url = config.CONSTANTS["OLD_CURRENCY_CONV_URL"]
    url += year + month + "/"
    url += day + month + year + ".xml"

    resp = requests.get(url, verify=False)
    resp_as_dict = xmltodict.parse(resp.text)

    return resp_as_dict

def get_old_currency(date: datetime, curr: str) -> float:
    """ Returns an old currency """
    result = 0
    old_currencies = get_old_currencies(date)

    for old_curr in old_currencies["Tarih_Date"]["Currency"]:
        if old_curr["@Kod"] == curr:
            result = float(old_curr["BanknoteBuying"])

    return result

def execute():
    """ Runs currency update """

    # Currencies from TCMB
    resp = requests.get(config.CONSTANTS["CURRENCY_CONV_URL"], verify=False)
    resp_as_dict = xmltodict.parse(resp.text)

    # Gold conversion
    gold_resp = requests.get(config.CONSTANTS["CURRENY_GOLD_URL"])
    pos1 = gold_resp.text.find('<table class="table table-striped">') + 113
    gold_price_txt = gold_resp.text[pos1:pos1+7].replace("<", "").replace(",", ".")
    gold_price = float(gold_price_txt)
    dgc_dict = {
        "@CrossOrder": "0",
        "@Kod": "DGC",
        "@CurrencyCode": "DGC",
        "Unit": "1",
        "Isim": "Gold",
        "CurrencyName": "Gold",
        "ForexBuying": gold_price,
        "ForexSelling": gold_price,
        "BanknoteBuying": gold_price,
        "BanknoteSelling": gold_price
    }
    resp_as_dict["Tarih_Date"]["Currency"].append(dgc_dict)

    # Save
    currency.save_currency_conv(resp_as_dict)
