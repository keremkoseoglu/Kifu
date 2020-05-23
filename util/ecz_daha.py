""" Eczacıbaşı activity integration """
import json
import requests
from requests.auth import HTTPBasicAuth
from config.constants import ECZ_DAHA_USER, ECZ_DAHA_PASS, ECZ_DAHA_DAILY_URL, ECZ_DAHA_MONTHLY_URL


def get_daily_activity(p_sap_date: str) -> dict:
    """ Returns activities on the given date """
    fiori_url = ECZ_DAHA_DAILY_URL + "?date=" + p_sap_date
    resp = requests.get(fiori_url, auth=HTTPBasicAuth(ECZ_DAHA_USER, ECZ_DAHA_PASS))
    resp_as_dict = json.loads(resp.text)
    return resp_as_dict

def get_monthly_activity(p_sap_year: str, p_sap_month: str) -> dict:
    """ Returns activities on the given month """
    fiori_url = ECZ_DAHA_MONTHLY_URL + "?gjahr=" + p_sap_year + "&monat=" + p_sap_month
    resp = requests.get(fiori_url, auth=HTTPBasicAuth(ECZ_DAHA_USER, ECZ_DAHA_PASS))
    resp_as_dict = json.loads(resp.text)
    return resp_as_dict
