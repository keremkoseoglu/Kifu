""" Address book report module """
from model.company import Company
from report.html_report import HtmlReport

class AddressBook(HtmlReport): # pylint: disable=R0903
    """ Address book report generator """
    _REPORT_NAME = "Address book"

    def _get_html_content(self) -> str: # pylint: disable=R0912, R0903
        output = ""
        first_company = True
        companies_json = Company.get_companies()
        for company_json in companies_json["companies"]:
            if not first_company:
                output += "<hr>"
            company = Company(company_json["name"])
            output += "<h1>" + company.name + "</h1>"
            if company.contact_person != "":
                output += company.contact_person + "<br>"
            if company.email != "":
                output += "<a href=mailto:" + company.email + ">" + company.email + "</a><br>"
            if company.phone != "":
                output += company.phone + "<br>"
            if company.address != "":
                output += company.address + "<br>"
            if company.country != "":
                output += company.country + "<br>"

            tax_number, tax_office = company.tax_info
            if tax_number != "" or tax_office != "":
                output += tax_office + " VD - " + tax_number + "<br>"

            if len(company.locations) > 0:
                output += "<br><b>Locations: </b>"
                first_location = True
                for location in company.locations:
                    if not first_location:
                        output += ", "
                    output += location
                    first_location = False
                output += "<br>"

            if len(company.ibans) > 0:
                output += "<br><b>Ibans: </b><ul>"
                for iban in company.ibans:
                    output += "<li>" + iban["name"] + " - " + iban["number"] + "</li>"
                output += "</ul><br>"

        return output

    def _get_report_name(self) -> str:
        return AddressBook._REPORT_NAME
