from model.company import Company
from config.constants import *
from util.company_label import CompanyLabel


class InvoiceLabel:

    def generate(self, invoices: []):

        companies = []

        for s in range(2):
            companies.append(Company(COMPANY_NAME_ACCOUNTING))

        for invoice in invoices:
            companies.append(invoice.payer)

        CompanyLabel().generate(companies)
