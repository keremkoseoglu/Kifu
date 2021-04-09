""" Module to fetch old / historic currency values """
import datetime
import requests
import xmltodict
from util import date_time
import config

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
