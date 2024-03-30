""" Income tax rates API """
from datetime import date
from model.timesheet.income_tax import IncomeTaxCalculatorFactory

class IncomeTaxRatesAPI():
    """ Income tax rates API """

    @property
    def result(self) -> dict:
        """ Returns result """
        inc_tax_calc = IncomeTaxCalculatorFactory.get_instance()
        out = {"default_rate": int(inc_tax_calc.default_tax_rate),
               "safety_rate": int(inc_tax_calc.safety_tax_rate),
               "temp_rate": int(inc_tax_calc.temp_tax_rate),
               "annual_rate": int(inc_tax_calc.calc_invoice_tax_rate(date.today().year, 0)),
               "forecast_rate": int(inc_tax_calc.forecast_tax_rate)}
        return out
