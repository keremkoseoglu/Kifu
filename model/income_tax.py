""" Income tax module """
from os import path
import json
from datetime import date
import config
from model.invoice_file_reader import get_invoices_of_last_year, get_invoices_of_fiscal_year
from model.currency import CurrencyConverter
from util.date_time import parse_json_date

_INCOME_TAX_FILE = "income_tax.json"

class IncomeTaxCalculator():
    """ Income tax calculator class """
    def __init__(self):
        self._tax_rates = []

        self._default_tax_rate = 0
        self._default_tax_rate_calculated = False

        self._tmp_tax_rate = 0
        self._tmp_tax_rate_calculated = False

        self._forecast_tax_rate = 0
        self._forecast_tax_rate_calculated = False

        self._converter = CurrencyConverter()
        self._read_tax_rates()

    @property
    def default_tax_rate(self) -> float:
        """ Returns average tax rate from historic invoices """
        if not self._default_tax_rate_calculated:
            today = date.today()
            invoices = get_invoices_of_last_year()
            invoice_sum = 0
            for invoice in invoices:
                home_amount = self._converter.convert_to_local_currency(
                    invoice["amount"],
                    invoice["currency"])
                inv_date = parse_json_date(invoice["invoice_date"])
                if inv_date.year < today.year:
                    home_amount *= 1 + (config.CONSTANTS["TUFE_RATE"] / 100)
                invoice_sum += home_amount
            annual_tax = self._calc_annual_tax(invoice_sum)
            self._default_tax_rate = (annual_tax / invoice_sum) * 100
            self._default_tax_rate_calculated = True
        return self._default_tax_rate

    @property
    def temp_tax_rate(self) -> float:
        """ Returns temporay tax rate """
        if not self._tmp_tax_rate_calculated:
            self._tmp_tax_rate = self.default_tax_rate / 2
            self._tmp_tax_rate_calculated = True
        return self._tmp_tax_rate

    @property
    def safety_tax_rate(self) -> float:
        """ Returns safety tax rate """
        return self.temp_tax_rate

    @property
    def forecast_tax_rate(self) -> float:
        """ Returns forecast tax rate """
        if not self._forecast_tax_rate_calculated:
            # Last year (with inflation)
            last_year = date.today().year - 1
            last_year_invoices = get_invoices_of_fiscal_year(last_year)
            invoice_sum = 0
            for invoice in last_year_invoices:
                home_amount = self._converter.convert_to_local_currency(
                    invoice["amount"],
                    invoice["currency"])
                home_amount *= 1 + (config.CONSTANTS["TUFE_RATE"] / 100)
                invoice_sum += home_amount

            if invoice_sum == 0:
                last_year_rate = 0
            else:
                last_year_annual_tax = self._calc_annual_tax(invoice_sum)
                last_year_rate = last_year_annual_tax / invoice_sum

            # This year (projection)
            this_year_invoices = get_invoices_of_fiscal_year(date.today().year)
            invoice_sum = 0
            for invoice in this_year_invoices:
                home_amount = self._converter.convert_to_local_currency(
                    invoice["amount"],
                    invoice["currency"])
                home_amount *= 1 + (config.CONSTANTS["TUFE_RATE"] / 100)
                invoice_sum += home_amount
            invoice_sum = invoice_sum * (12 - (date.today().month) + 1)

            if invoice_sum == 0:
                this_year_rate = 0
            else:
                this_year_annual_tax = self._calc_annual_tax(invoice_sum)
                this_year_rate = this_year_annual_tax / invoice_sum

            # Average
            if this_year_rate == 0:
                self._forecast_tax_rate = last_year_rate
            elif last_year_rate == 0:
                self._forecast_tax_rate = this_year_rate
            else:
                if this_year_rate > last_year_rate:
                    self._forecast_tax_rate = this_year_rate
                else:
                    self._forecast_tax_rate = (this_year_rate + last_year_rate) / 2

            self._forecast_tax_rate *= 100
            self._forecast_tax_rate_calculated = True
        return self._forecast_tax_rate

    def calc_invoice_tax_rate(self, year: int, amount: float) -> float:
        """ Calculate tax rate for given invoice """
        fiscal_invoices = get_invoices_of_fiscal_year(year)
        invoice_sum = 0
        for invoice in fiscal_invoices:
            home_amount = self._converter.convert_to_local_currency(
                invoice["amount"],
                invoice["currency"])
            invoice_sum += home_amount
        invoice_sum += amount

        for tax_rate in self._tax_rates:
            if tax_rate["amount"] >= invoice_sum:
                return tax_rate["rate"]

        raise Exception("Couldn't calculate invoice tax rate")


    def calc_invoice_tax_amount(self, year: int, amount: float) -> float:
        """ Calculate tax for given invoice """
        tax_rate = self.calc_invoice_tax_rate(year, amount)
        return amount * tax_rate / 100


    def _read_tax_rates(self):
        with open(self._income_tax_file_path) as tax_file:
            json_data = json.load(tax_file)
        self._tax_rates = json_data["rates"]

    def _calc_annual_tax(self, amount: float) -> float:
        out = 0
        remain = amount

        for tax_rate in self._tax_rates:
            if remain > tax_rate["amount"]:
                tax_amount = tax_rate["amount"] * tax_rate["rate"] / 100
                out += tax_amount
                remain -= tax_rate["amount"]
            else:
                tax_amount = remain * tax_rate["rate"] / 100
                out += tax_amount
                remain = 0
                break
        return out

    @property
    def _income_tax_file_path(self) -> str:
        global _INCOME_TAX_FILE
        return path.join(config.CONSTANTS["DATA_DIR_PATH"] + _INCOME_TAX_FILE)

class IncomeTaxCalculatorFactory():
    """ Singleton """
    _SINGLETON: IncomeTaxCalculator = None

    @staticmethod
    def get_instance() -> IncomeTaxCalculator:
        """ Singleton """
        if IncomeTaxCalculatorFactory._SINGLETON is None:
            IncomeTaxCalculatorFactory._SINGLETON = IncomeTaxCalculator()
        return IncomeTaxCalculatorFactory._SINGLETON
