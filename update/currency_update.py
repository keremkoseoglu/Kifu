""" Currency update """
import requests
import xmltodict
from model import currency
import config

_EXECUTED_TODAY = False

def execute():
    """ Runs currency update """
    global _EXECUTED_TODAY

    if _EXECUTED_TODAY:
        return

    _EXECUTED_TODAY = True

    try:
        # Currencies from TCMB
        resp = requests.get(config.CONSTANTS["CURRENCY_CONV_URL"], verify=False, timeout=5)
        resp_as_dict = xmltodict.parse(resp.text)

        # Gold conversion
        gold_resp = requests.get(config.CONSTANTS["CURRENY_GOLD_URL"], verify=False, timeout=5)
        pos1 = gold_resp.text.find('<table class="table table-striped">') + 113
        gold_price_txt = gold_resp.text[pos1:pos1+7].replace("<", "").replace(",", ".")
        gold_price = float(gold_price_txt.replace("/", ""))
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

    except Exception as error:
        print("Currency update error: " + str(error))
