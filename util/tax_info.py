""" Tax info """
import os
from model.company import Company
from model.bank_account import get_home_bank_acc_str
import config

class TaxInfo:
    """ Tax info generation """
    def __init__(self):
        self._html = ""
        self._company = Company(config.CONSTANTS["HOME_COMPANY"])

    def generate_for_home(self):
        """ Generate for home company """
        self._company = Company(config.CONSTANTS["HOME_COMPANY"])
        self._generate_html()
        self._save_html()

    def _generate_html(self):
        tax_no, tax_off = self._company.tax_info

        self._html = "<html><head/><body>"
        self._html += self._company.contact_person + "<br>"
        self._html += "Adres: " + self._company.address + "<br>"
        self._html += "Telefon: " + self._company.phone + "<br>"
        self._html += "E-Mail: " + self._company.email + "<br>"
        self._html += "Vergi dairesi: " + tax_off + "<br>"
        self._html += "Vergi no: " + tax_no + "<br>"
        self._html += "IBAN: " + get_home_bank_acc_str()
        self._html += "</body></html>"

    def _save_html(self):
        file_path = config.CONSTANTS["DOWNLOAD_DIR"] + "kifu_tax.html"
        with open(file_path, "w", encoding="utf-8") as company_file:
            company_file.write(self._html)
        os.system("open \"" + file_path + "\"")
        self._html = ""
