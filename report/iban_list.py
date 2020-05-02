from report.html_report import HtmlReport
from model import bank_account
from model.company import Company
from config.constants import *


class IbanList(HtmlReport):

    _REPORT_NAME = "IBAN List"

    def __init__(self):
        self._home_company = Company(HOME_COMPANY)

    def _get_html_content(self) -> str:

        output = ""
        bank_accounts = bank_account.get_bank_accounts()

        for acc in bank_accounts["bank_accounts"]:
            if "iban" not in acc:
                continue
            output += "<b>" + acc["bank_name"] + "</b> (" + acc["account_name"] + ")<br>"
            output += self._home_company.contact_person + "<br>"
            output += acc["iban"] + "<br><hr>"

        return output

    def _get_report_name(self) -> str:
        return self._REPORT_NAME

