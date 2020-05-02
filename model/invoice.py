import datetime
from enum import Enum
import json
import os
from util import identifier, date_time
from config.constants import *
from model.company import Company
from model.currency import CurrencyConverter


class MultiValueError(Exception):
    class ErrorCode(Enum):
        multiple_payers = 1
        multiple_currencies = 2
        multiple_vat_rates = 3
        multiple_income_tax_rates = 4

    def __init__(self, error_code: ErrorCode):
        self.error_code = error_code

    @property
    def message(self) -> str:
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
    _INVOICE_FILE = "invoice.json"

    @staticmethod
    def delete_invoices(invoice_guids: []):
        all_invoices = Invoice.get_invoices()
        new_invoices = {"invoices": []}
        for i in range(len(all_invoices["invoices"])):
            invoice_i = all_invoices["invoices"][i]
            if invoice_i["guid"] not in invoice_guids:
                new_invoices["invoices"].append(invoice_i)
        Invoice._write_invoices_to_disk(new_invoices)

    @staticmethod
    def get_due_date_suggestion(invoice_date: datetime) -> datetime:
        output = date_time.get_next_month(date=invoice_date)
        output = date_time.get_first_day_of_next_month(output)
        while True:
            while output.weekday() != 2:  # Wednesday
                output = date_time.get_next_day(output)
            if date_time.is_working_day(output):
                return output
            else:
                output = date_time.get_next_day(output)

    @staticmethod
    def get_invoice_date_suggestion() -> datetime:
        output = datetime.datetime.now()
        if output.day > 15:
            output = date_time.get_last_day_of_month(output)
        else:
            output = date_time.get_last_day_of_prev_month(output)
        return output

    @staticmethod
    def get_invoices():
        with open(Invoice._get_file_path()) as f:
            json_data = json.load(f)
        return json_data

    @staticmethod
    def _get_file_path():
        return os.path.join(DATA_DIR_PATH + Invoice._INVOICE_FILE)

    @staticmethod
    def _write_invoices_to_disk(invoices: []):
        with open(Invoice._get_file_path(), "w") as f:
            json.dump(invoices, f, indent=3)

    def __init__(self, invoice: {}):
        self._invoice = invoice
        self._amount = float(self._invoice["amount"])
        self._vat_rate = float(self._invoice["vat_rate"])
        self._income_tax_rate = float(self._invoice["income_tax_rate"])
        self._currency_converter = CurrencyConverter()

    @property
    def alms_amount(self) -> float:
        return (self.amount - self.income_tax_amount) * DEFAULT_ALMS_RATE / 100

    @property
    def alms_payment_date(self) -> datetime:
        return self.due_date + datetime.timedelta(days=1)

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def amount_plus_vat(self) -> float:
        return self.amount + self.vat_amount

    @property
    def currency(self) -> str:
        return self._invoice["currency"]

    @property
    def due_date(self) -> datetime:
        return date_time.parse_json_date(self._invoice["due_date"])

    @property
    def file_path(self) -> str:
        if "file_path" in self._invoice:
            return self._invoice["file_path"]
        else:
            return ""

    @file_path.setter
    def file_path(self, file_path: str):
        self._invoice["file_path"] = file_path

    @property
    def guid(self) -> str:
        return self._invoice["guid"]

    @property
    def income_tax_amount(self) -> float:
        return self.amount * self.income_tax_rate / 100

    @property
    def income_tax_payment_date(self) -> datetime:
        return datetime.date(self.invoice_date.year + 1, 3, 15)

    @property
    def income_tax_rate(self) -> float:
        return self._income_tax_rate

    @property
    def income_tax_transfer_date(self) -> datetime:
        return self.due_date + datetime.timedelta(days=1)

    @property
    def invoice_date(self) -> datetime:
        return date_time.parse_json_date(self._invoice["invoice_date"])

    @property
    def payer(self) -> Company:
        return Company(self._invoice["payer"])

    @property
    def serial(self) -> str:
        return self._invoice["serial"]

    @property
    def vat_amount(self) -> float:
        return self._amount * self._vat_rate / 100

    @property
    def vat_amount_in_local_currency(self) -> float:
        return self._currency_converter.convert_to_local_currency(self.vat_amount, self.currency)

    @property
    def vat_payment_date(self) -> datetime:
        invoice_date = self.invoice_date
        invoice_day = invoice_date.day

        if invoice_day < VAT_DECLARATION_LAST_DAY:
            output = datetime.date(invoice_date.year, invoice_date.month, VAT_DECLARATION_LAST_DAY)
        else:
            output = datetime.date(invoice_date.year, invoice_date.month, VAT_DECLARATION_LAST_DAY)
            output = output + datetime.timedelta(days=30)

        return output

    @property
    def vat_rate(self) -> float:
        return self._vat_rate

    @property
    def vat_transfer_date(self) -> datetime:
        return self.vat_payment_date - datetime.timedelta(days=15)

    @property
    def is_vat_liable(self) -> bool:
        return not self.payer.is_foreign

    def save(self):
        if "guid" not in self._invoice:
            self._invoice["guid"] = identifier.get_guid()
        elif self._invoice["guid"] == "":
            self._invoice["guid"] = identifier.get_guid()

        current_invoices = Invoice.get_invoices()
        new_invoices = { "invoices": [] }

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
    income_tax_rate_set = False
    payer_set = False
    currency_set = False

    for act in activities:
        proj = act.project
        payer_name = proj.payer.name
        earned_amount, earned_curr = proj.get_earned_amount(act.hours)
        vat_rate = proj.vat_rate
        income_tax_rate = proj.income_tax_rate

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

        if not income_tax_rate_set:
            inv_json["income_tax_rate"] = income_tax_rate
            income_tax_rate_set = True
        elif inv_json["income_tax_rate"] != income_tax_rate:
            raise MultiValueError(MultiValueError.ErrorCode.multiple_income_tax_rates)

        inv_json["amount"] += earned_amount

    return Invoice(inv_json)