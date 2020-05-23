""" Invoice label printing """
from model.company import Company
from config.constants import COMPANY_NAME_ACCOUNTING
from util.company_label import CompanyLabel


class InvoiceLabel:
    """ Invoice label printing """

    @staticmethod
    def generate(invoices: []):
        """ Prints given invoices """

        companies = []

        for snumber in range(2): # pylint: disable=W0612
            companies.append(Company(COMPANY_NAME_ACCOUNTING))

        for invoice in invoices:
            companies.append(invoice.payer)

        CompanyLabel().generate(companies)
