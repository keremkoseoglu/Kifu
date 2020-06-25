""" Company label printing """
import os
from model.company import Company
import config


class CompanyLabel:
    """ Company label printing """

    def __init__(self):
        self._html = ""
        self._html_count = 0
        self._company_count = 0
        self._company = Company(config.CONSTANTS["HOME_COMPANY"])

    def generate(self, companies: []):
        """ Generate labels """
        self._html = ""
        self._html_count = 0
        self._company_count = 0

        for company in companies:
            self._add_label(company)

        if self._html != "":
            if self._company_count == 1:
                self._html += "<td width=50%>&nbsp;</td></tr><tr><td width=50%>&nbsp;</td><td width=50%>&nbsp;</td></tr>" # pylint: disable=C0301
            if self._company_count == 2:
                self._html += "<tr><td width=50%>&nbsp;</td><td width=50%>&nbsp;</td></tr>"
            if self._company_count == 3:
                self._html += "<td width=50%>&nbsp;</td></tr>"
            self._end_html()
            self._save_html()

    def _add_label(self, comp: Company):
        self._company_count += 1
        if self._company_count > 4:
            self._end_html()
            self._save_html()

        if self._html == "":
            self._begin_html()

        if self._company_count == 1 or self._company_count == 3:
            self._html += "<tr height=50%>"

        self._html += "<td width=50% align=center>"
        self._html += "<h1>" + comp.name + "</h1>"
        self._html += "<h2>" + comp.contact_person + "</h2>"
        self._html += "<big><big>" + comp.address + "<br>"
        self._html += comp.phone + "<br>"
        self._html += "</big></big>"

        shipping_note = comp.shipping_note
        if shipping_note != "":
            self._html += "<br><b>(" + shipping_note + ")</b>"
        #self._html += "<br><hr>"
        #self._html += "<b>Gönderen: </b>"
        #self._html += self._config.CONSTANTS["HOME_COMPANY"].contact_person + ", "
        #self._html += self._config.CONSTANTS["HOME_COMPANY"].sender_address
        self._html += "</td>"

        if self._company_count == 2 or self._company_count == 4:
            self._html += "</tr>"

    def _begin_html(self):
        self._html = "<html><head></head><body>"
        self._html += "<table width=100% height=100%>"

    def _end_html(self):
        self._html_count += 1
        self._html += "</table>"
        self._html += "</body></html>"

    def _save_html(self):
        file_path = config.CONSTANTS["DOWNLOAD_DIR"] + "labels " + str(self._html_count) + ".html"
        with open(file_path, "w") as company_file:
            company_file.write(self._html)
        os.system("open \"" + file_path + "\"")
        self._html = ""
