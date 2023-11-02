""" Currency update """
import json
import requests
import xmltodict
from model import currency
import config
from util import backup

_EXECUTED_TODAY = False


def execute(run_backup: bool = True):
    """Runs currency update"""
    global _EXECUTED_TODAY

    if _EXECUTED_TODAY:
        return

    _EXECUTED_TODAY = True

    try:
        # Backup
        if run_backup:
            backup.execute()

        # Currencies from TCMB
        resp = requests.get(
            config.CONSTANTS["CURRENCY_CONV_URL"], verify=False, timeout=5
        )
        resp_as_dict = xmltodict.parse(resp.text)

        # Gold conversion
        gold_resp = requests.get(
            config.CONSTANTS["CURRENY_GOLD_URL"], verify=False, timeout=5
        )
        pos1 = gold_resp.text.find(
            "altinData =",
        )
        pos2 = gold_resp.text.find(";", pos1)
        gold_price_txt = gold_resp.text[pos1:pos2].replace("altinData =", "")
        gold_price_json = json.loads(gold_price_txt)
        gold_price = -1

        for gold_entry in gold_price_json:
            if gold_entry["Adi"] == "ALTIN (TL/GR)":
                gold_price = gold_entry["Alis"]
                break

        if gold_price > 0:
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
                "BanknoteSelling": gold_price,
            }
            resp_as_dict["Tarih_Date"]["Currency"].append(dgc_dict)

        # Save
        currency.save_currency_conv(resp_as_dict)

    except Exception as error:
        print(f"Currency update error: {str(error)}")
