""" Eczacıbaşı activity integration """
import json
from ssl import create_default_context, Purpose, CERT_NONE

# import requests
from requests import Session, adapters
from requests.auth import HTTPBasicAuth
from urllib3 import poolmanager
import config


class CustomHttpAdapter(adapters.HTTPAdapter):
    """Created to prevent some bug with SSL in Python"""

    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        """Created to prevent some bug with SSL in Python"""
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_context=self.ssl_context,
        )


def ssl_supressed_session():
    """Created to prevent some bug with SSL in Python"""
    ctx = create_default_context(Purpose.SERVER_AUTH)
    # to bypass verification after accepting Legacy connections
    ctx.check_hostname = False
    ctx.verify_mode = CERT_NONE
    # accepting legacy connections
    ctx.options |= 0x4
    session = Session()
    session.mount("https://", CustomHttpAdapter(ctx))
    return session


def get_daily_activity(p_sap_date: str) -> dict:
    """Returns activities on the given date"""
    fiori_url = config.CONSTANTS["ECZ_DAHA_DAILY_URL"] + "?date=" + p_sap_date

    # resp = requests.get(
    #     fiori_url,
    #     timeout=10,
    #     auth=HTTPBasicAuth(
    #         config.CONSTANTS["ECZ_DAHA_USER"], config.CONSTANTS["ECZ_DAHA_PASS"]
    #     ),
    # )

    resp = ssl_supressed_session().get(
        fiori_url,
        timeout=10,
        auth=HTTPBasicAuth(
            config.CONSTANTS["ECZ_DAHA_USER"], config.CONSTANTS["ECZ_DAHA_PASS"]
        ),
    )

    resp_as_dict = json.loads(resp.text)
    return resp_as_dict


def get_monthly_activity(p_sap_year: str, p_sap_month: str) -> dict:
    """Returns activities on the given month"""
    fiori_url = config.CONSTANTS["ECZ_DAHA_MONTHLY_URL"]
    fiori_url += "?gjahr=" + p_sap_year + "&monat=" + p_sap_month

    # resp = requests.get(
    #    fiori_url,
    #    timeout=10,
    #    auth=HTTPBasicAuth(
    #        config.CONSTANTS["ECZ_DAHA_USER"], config.CONSTANTS["ECZ_DAHA_PASS"]
    #    ),
    # )

    resp = ssl_supressed_session().get(
        fiori_url,
        timeout=10,
        auth=HTTPBasicAuth(
            config.CONSTANTS["ECZ_DAHA_USER"], config.CONSTANTS["ECZ_DAHA_PASS"]
        ),
    )

    resp_as_dict = json.loads(resp.text)
    return resp_as_dict
