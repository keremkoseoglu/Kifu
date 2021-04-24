""" Invoice """
import datetime
from enum import Enum
import json
from util import identifier, date_time
from model.company import Company
from model.currency import CurrencyConverter
from model.invoice_file_reader import get_invoices, get_file_path
from model.income_tax import IncomeTaxCalculatorFactory
import config

class MultiValueError(Exception):
    """ Error regarding multiple values
    when single was expected
    """
    class ErrorCode(Enum):
        """ Error code enum """
        multiple_payers = 1
        multiple_currencies = 2
        multiple_vat_rates = 3
        multiple_income_tax_rates = 4

    def __init__(self, error_code: ErrorCode):
        super().__init__()
        self.error_code = error_code

    @property
    def message(self) -> str:
        """ Human readable error message """
        if self.error_code == MultiValueError.ErrorCode.multiple_currencies:
            return "Multiple currencies"
        if self.error_code == MultiValueError.ErrorCode.multiple_income_tax_rates:
            return "Multiple income tax rates"
        if self.error_code == MultiValueError.ErrorCode.multiple_payers:
            return "Multiple payers"
        if self.error_code == MultiValueError.ErrorCode.multiple_vat_rates:
            return "Multiple VAT rates"
        return "Invoice value error"


class Invoice:
    """ Invoice class """
    @staticmethod
    def delete_invoices(invoice_guids: []):
        """ Deletes the provided invoices """
        all_invoices = get_invoices()
        new_invoices = {"invoices": []}
        for i in range(len(all_invoices["invoices"])):
            invoice_i = all_invoices["invoices"][i]
            if invoice_i["guid"] not in invoice_guids:
                new_invoices["invoices"].append(invoice_i)
        Invoice._write_invoices_to_disk(new_invoices)

    @staticmethod
    def get_due_date_suggestion(invoice_date: datetime) -> datetime:
        """ Suggests a due date based on the invoice date """
        output = date_time.get_next_month(date=invoice_date)
        output = date_time.get_first_day_of_next_month(output)
        while True:
            while output.weekday() != 2:  # Wednesday
                output = date_time.get_next_day(output)
            if date_time.is_working_day(output):
                return output
            output = date_time.get_next_day(output)

    @staticmethod
    def get_invoice_date_suggestion() -> datetime:
        """ Suggests an invoice date """
        output = datetime.datetime.now()
        if output.day > 15:
            output = date_time.get_last_day_of_month(output)
        else:
            output = date_time.get_last_day_of_prev_month(output)
        return output

    @staticmethod
    def _write_invoices_to_disk(invoices: []):
        with open(get_file_path(), "w") as invoice_file:
            json.dump(invoices, invoice_file, indent=3)

    def __init__(self, invoice: {}):
        self._invoice = invoice
        self._amount = float(self._invoice["amount"])
        self._vat_rate = float(self._invoice["vat_rate"])
        self._income_tax_rate = float(self._invoice["income_tax_rate"])
        self._currency_converter = CurrencyConverter()

    @property
    def alms_amount(self) -> float:
        """ Amount of recommended alms """
        return (self.amount - self.income_tax_amount) * config.CONSTANTS["DEFAULT_ALMS_RATE"] / 100

    @property
    def alms_payment_date(self) -> datetime:
        """ Alms payment date """
        return self.due_date + datetime.timedelta(days=1)

    @property
    def amount(self) -> float:
        """ Invoice amount as float """
        return self._amount

    @property
    def amount_plus_vat(self) -> float:
        """ Invoice amount + vat as float """
        return self.amount + self.vat_amount

    @property
    def currency(self) -> str:
        """ Invoice currency """
        return self._invoice["currency"]

    @property
    def due_date(self) -> datetime:
        """ Invoice due date """
        return date_time.parse_json_date(self._invoice["due_date"])

    @property
    def file_path(self) -> str:
        """ File path of invoice
        This is usually the PDF file of the e-archive invoice
        """
        if "file_path" in self._invoice:
            return self._invoice["file_path"]
        return ""

    @file_path.setter
    def file_path(self, file_path: str):
        """ File path setter """
        self._invoice["file_path"] = file_path

    @property
    def guid(self) -> str:
        """ Invoice GUID
        Every invoice will have a unique immutable GUID.
        But if you really need to change it, you can edit
        JSON data files
        """
        return self._invoice["guid"]

    @property
    def income_tax_amount(self) -> float:
        """ Income tax amount """
        return self.amount * self.income_tax_rate / 100

    @property
    def income_tax_payment_date(self) -> datetime:
        """ Income tax payment date (suggestion) """
        return datetime.date(self.invoice_date.year + 1, 3, 15)

    @property
    def income_tax_rate(self) -> float:
        """ Income tax rate
        Usually ~30%
        """
        return self._income_tax_rate

    @property
    def income_tax_transfer_date(self) -> datetime:
        """ Suggested income tax transfer date """
        return self.due_date + datetime.timedelta(days=1)

    @property
    def invoice_date(self) -> datetime:
        """ Invoice date """
        return date_time.parse_json_date(self._invoice["invoice_date"])

    @property
    def payer(self) -> Company:
        """ Company which will pay the invoice """
        return Company(self._invoice["payer"])

    @property
    def serial(self) -> str:
        """ Invoice serial number
        Paper invoice: Preprinted
        E-Archive: Provided by GIB
        """
        return self._invoice["serial"]

    @property
    def vat_amount(self) -> float:
        """ Calculated VAT amount """
        return self._amount * self._vat_rate / 100

    @property
    def vat_amount_in_local_currency(self) -> float:
        """ Calculated VAT amount in local currency """
        return self._currency_converter.convert_to_local_currency(self.vat_amount, self.currency)

    @property
    def vat_payment_date(self) -> datetime:
        """ VAT payment date """
        invoice_date = self.invoice_date
        invoice_day = invoice_date.day

        if invoice_day < config.CONSTANTS["VAT_DECLARATION_LAST_DAY"]:
            output = datetime.date(
                invoice_date.year,
                invoice_date.month,
                config.CONSTANTS["VAT_DECLARATION_LAST_DAY"])
        else:
            output = datetime.date(
                invoice_date.year,
                invoice_date.month,
                config.CONSTANTS["VAT_DECLARATION_LAST_DAY"])
            output = output + datetime.timedelta(days=30)

        return output

    @property
    def vat_rate(self) -> float:
        """ VAT rate """
        return self._vat_rate

    @property
    def vat_transfer_date(self) -> datetime:
        """ VAT transfer date """
        return self.vat_payment_date - datetime.timedelta(days=15)

    @property
    def is_vat_liable(self) -> bool:
        """ Is VAT liable or not
        Usually; foreign invoices are not VAT liable """
        return not self.payer.is_foreign

    def save(self):
        """ Writes invoice data to disk """
        if "guid" not in self._invoice:
            self._invoice["guid"] = identifier.get_guid()
        elif self._invoice["guid"] == "":
            self._invoice["guid"] = identifier.get_guid()

        current_invoices = get_invoices()
        new_invoices = {"invoices": []}

        updated = False
        for inv in current_invoices["invoices"]:
            if inv["guid"] == self._invoice["guid"]:
                new_invoices["invoices"].append(self._invoice)
                updated = True
            else:
                new_invoices["invoices"].append(inv)

        if not updated:
            new_invoices["invoices"].append(self._invoice)

        Invoice._write_invoices_to_disk(new_invoices)


def get_invoice_obj_from_activities(activities: []) -> Invoice:
    """ Creates a new invoice from the given activities """
    invoice_date = Invoice.get_invoice_date_suggestion()
    due_date = Invoice.get_due_date_suggestion(invoice_date)

    inv_json = {
        "guid": identifier.get_guid(),
        "serial": "",
        "payer": "",
        "invoice_date": invoice_date.isoformat(),
        "due_date": due_date.isoformat(),
        "amount": 0,
        "currency": "",
        "vat_rate": 0,
        "income_tax_rate": 0
    }

    vat_rate_set = False
    payer_set = False
    currency_set = False

    for act in activities:
        proj = act.project
        payer_name = proj.payer.name
        earned_amount, earned_curr = proj.get_earned_amount(act.hours)
        vat_rate = proj.vat_rate

        if not payer_set:
            inv_json["payer"] = payer_name
            payer_set = True
        elif inv_json["payer"] != payer_name:
            raise MultiValueError(MultiValueError.ErrorCode.multiple_payers)

        if not currency_set:
            inv_json["currency"] = earned_curr
            currency_set = True
        elif inv_json["currency"] != earned_curr:
            raise MultiValueError(MultiValueError.ErrorCode.multiple_currencies)

        if not vat_rate_set:
            inv_json["vat_rate"] = vat_rate
            vat_rate_set = True
        elif inv_json["vat_rate"] != vat_rate:
            raise MultiValueError(MultiValueError.ErrorCode.multiple_vat_rates)

        inv_json["amount"] += earned_amount

    inc_tax_calc = IncomeTaxCalculatorFactory.get_instance()
    inv_json["income_tax_rate"] = inc_tax_calc.calc_invoice_tax_rate(
        invoice_date.year,
        inv_json["amount"])

    return Invoice(inv_json)
