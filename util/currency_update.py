import requests, xmltodict
from model import currency
from config.constants import *


def execute():

    # Currencies from TCMB
    resp = requests.get(CURRENCY_CONV_URL)
    resp_as_dict = xmltodict.parse(resp.text)

    # Gold conversion
    gold_resp = requests.get(CURRENY_GOLD_URL)
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