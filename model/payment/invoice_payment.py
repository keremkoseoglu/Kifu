""" Invoice payments """

import datetime
from typing import List
import config
from model.payment.payment import (
    DIRECTION_IN,
    DIRECTION_OUT,
    DIRECTION_TRANSFER,
    PERIOD_DAILY,
    Payment,
)
from model.payment.scheme import Scheme
from model.timesheet.income_tax import IncomeTaxCalculatorFactory
from model.timesheet.invoice import Invoice
from util import date_time, identifier


class InvoicePaymentSet:
    """Invoice payment set"""

    _invoice: Invoice
    _payment_list: List
    _description_prefix: str

    """ Invoice payments """

    def __init__(self, invoice: Invoice):
        self._invoice = invoice
        self._payment_list = None
        self._description_prefix = None

    @property
    def payment_list(self) -> List:
        """Payment list"""
        if self._payment_list is None:
            self._build_payment_list()
        return self._payment_list

    @property
    def description_prefix(self) -> str:
        """Description prefix"""
        if self._description_prefix is None:
            self._description_prefix = (
                self._invoice.payer.name
                + " - "
                + date_time.get_formatted_date(self._invoice.invoice_date)
                + "("
                + self._invoice.serial
                + ")"
            )

        return self._description_prefix

    def save_payments(self):
        """Save payments"""
        for payment in self.payment_list:
            payment.save()

    def _append_jsons_to_list(self, payment_json: dict, scheme_json: dict):
        scheme_obj = Scheme(scheme_json)
        payment_obj = Payment(payment_json)
        payment_obj.scheme = scheme_obj
        self._payment_list.append(payment_obj)

    def _append_incoming_payment_to_list(self):
        incoming_payment_json = {
            "guid": identifier.get_guid(),
            "creation_date": datetime.datetime.now().isoformat(),
            "company": self._invoice.payer.name,
            "description": self.description_prefix + " - Incoming payment",
            "invoice_guid": self._invoice.guid,
            "direction": DIRECTION_IN,
            "amount": self._invoice.amount_plus_vat,
            "currency": self._invoice.currency,
            "cleared": False,
        }

        incoming_scheme_json = {
            "frequency": 1,
            "period": PERIOD_DAILY,
            "start": self._invoice.due_date.isoformat(),
            "repeat": 1,
            "recurrence": [
                {
                    "recurrence_date": self._invoice.due_date.isoformat(),
                    "expected_payment_date": self._invoice.due_date.isoformat(),
                    "amount": self._invoice.amount_plus_vat,
                    "currency": self._invoice.currency,
                    "cleared": False,
                    "collections": [],
                }
            ],
        }

        self._append_jsons_to_list(incoming_payment_json, incoming_scheme_json)

    def _append_vat_transfer_to_list(self):
        vat_amount = self._invoice.vat_amount_in_local_currency

        vat_transfer_json = {
            "guid": identifier.get_guid(),
            "creation_date": datetime.datetime.now().isoformat(),
            "company": config.CONSTANTS["DEFAULT_BANK"],
            "description": self.description_prefix + " - VAT transfer",
            "invoice_guid": "",
            "direction": DIRECTION_TRANSFER,
            "amount": vat_amount,
            "currency": config.CONSTANTS["HOME_CURRENCY"],
            "cleared": False,
        }

        vat_transfer_date = self._invoice.vat_transfer_date

        vat_transfer_scheme_json = {
            "frequency": 1,
            "period": PERIOD_DAILY,
            "start": vat_transfer_date.isoformat(),
            "repeat": 1,
            "recurrence": [
                {
                    "recurrence_date": vat_transfer_date.isoformat(),
                    "expected_payment_date": vat_transfer_date.isoformat(),
                    "amount": vat_amount,
                    "currency": config.CONSTANTS["HOME_CURRENCY"],
                    "cleared": False,
                    "collections": [],
                }
            ],
        }

        self._append_jsons_to_list(vat_transfer_json, vat_transfer_scheme_json)

    def _append_vat_payment_to_list(self):
        vat_amount = self._invoice.vat_amount_in_local_currency

        vat_payment_json = {
            "guid": identifier.get_guid(),
            "creation_date": datetime.datetime.now().isoformat(),
            "company": config.CONSTANTS["HOME_GOVERNMENT"],
            "description": self.description_prefix + " - VAT payment",
            "invoice_guid": "",
            "direction": DIRECTION_OUT,
            "amount": vat_amount,
            "currency": config.CONSTANTS["HOME_CURRENCY"],
            "cleared": False,
            "is_vat": True,
        }

        vat_payment_date = self._invoice.vat_payment_date

        vat_payment_scheme_json = {
            "frequency": 1,
            "period": PERIOD_DAILY,
            "start": vat_payment_date.isoformat(),
            "repeat": 1,
            "recurrence": [
                {
                    "recurrence_date": vat_payment_date.isoformat(),
                    "expected_payment_date": vat_payment_date.isoformat(),
                    "amount": vat_amount,
                    "currency": config.CONSTANTS["HOME_CURRENCY"],
                    "cleared": False,
                    "collections": [],
                }
            ],
        }

        self._append_jsons_to_list(vat_payment_json, vat_payment_scheme_json)

    def _append_itax_investment_transfer_to_list(self, itax_investment_amount: float):
        itax_transfer_json = {
            "guid": identifier.get_guid(),
            "creation_date": datetime.datetime.now().isoformat(),
            "company": config.CONSTANTS["DEFAULT_BANK"],
            "description": self.description_prefix + " - income tax investment",
            "invoice_guid": "",
            "direction": DIRECTION_TRANSFER,
            "amount": itax_investment_amount,
            "currency": config.CONSTANTS["HOME_CURRENCY"],
            "cleared": False,
        }

        itax_transfer_date = self._invoice.income_tax_transfer_date

        itax_transfer_scheme_json = {
            "frequency": 1,
            "period": PERIOD_DAILY,
            "start": itax_transfer_date.isoformat(),
            "repeat": 1,
            "recurrence": [
                {
                    "recurrence_date": itax_transfer_date.isoformat(),
                    "expected_payment_date": itax_transfer_date.isoformat(),
                    "amount": itax_investment_amount,
                    "currency": config.CONSTANTS["HOME_CURRENCY"],
                    "cleared": False,
                    "collections": [],
                }
            ],
        }

        self._append_jsons_to_list(itax_transfer_json, itax_transfer_scheme_json)

    def _append_itax_cash_transfer_to_list(self, itax_cash_amount: float):
        itax_transfer_json = {
            "guid": identifier.get_guid(),
            "creation_date": datetime.datetime.now().isoformat(),
            "company": config.CONSTANTS["DEFAULT_BANK"],
            "description": self.description_prefix + " - income tax transfer",
            "invoice_guid": "",
            "direction": DIRECTION_TRANSFER,
            "amount": itax_cash_amount,
            "currency": config.CONSTANTS["HOME_CURRENCY"],
            "cleared": False,
        }

        itax_transfer_date = self._invoice.income_tax_transfer_date

        itax_transfer_scheme_json = {
            "frequency": 1,
            "period": PERIOD_DAILY,
            "start": itax_transfer_date.isoformat(),
            "repeat": 1,
            "recurrence": [
                {
                    "recurrence_date": itax_transfer_date.isoformat(),
                    "expected_payment_date": itax_transfer_date.isoformat(),
                    "amount": itax_cash_amount,
                    "currency": config.CONSTANTS["HOME_CURRENCY"],
                    "cleared": False,
                    "collections": [],
                }
            ],
        }

        self._append_jsons_to_list(itax_transfer_json, itax_transfer_scheme_json)

    def _append_itax_transfers_to_list(self):
        inc_tax_calc = IncomeTaxCalculatorFactory.get_instance()
        total_itax_amount = self._invoice.income_tax_amount_in_local_currency
        itax_investment_rate = 100
        itax_investment_rate -= inc_tax_calc.safety_tax_rate
        itax_investment_rate -= inc_tax_calc.temp_tax_rate
        itax_investment_amount = total_itax_amount * itax_investment_rate / 100
        itax_cash_amount = total_itax_amount - itax_investment_amount

        self._append_itax_investment_transfer_to_list(itax_investment_amount)
        self._append_itax_cash_transfer_to_list(itax_cash_amount)

    def _append_itax_payment_to_list(self):
        total_itax_amount = self._invoice.income_tax_amount_in_local_currency

        itax_payment_json = {
            "guid": identifier.get_guid(),
            "creation_date": datetime.datetime.now().isoformat(),
            "company": config.CONSTANTS["HOME_GOVERNMENT"],
            "description": self.description_prefix + " - income tax payment",
            "invoice_guid": "",
            "direction": DIRECTION_OUT,
            "amount": total_itax_amount,
            "currency": config.CONSTANTS["HOME_CURRENCY"],
            "cleared": False,
            "is_income_tax": True,
        }

        itax_payment_date = self._invoice.income_tax_payment_date

        itax_payment_scheme_json = {
            "frequency": 1,
            "period": PERIOD_DAILY,
            "start": itax_payment_date.isoformat(),
            "repeat": 1,
            "recurrence": [
                {
                    "recurrence_date": itax_payment_date.isoformat(),
                    "expected_payment_date": itax_payment_date.isoformat(),
                    "amount": total_itax_amount,
                    "currency": config.CONSTANTS["HOME_CURRENCY"],
                    "cleared": False,
                    "collections": [],
                }
            ],
        }

        self._append_jsons_to_list(itax_payment_json, itax_payment_scheme_json)

    def _append_alms_to_list(self):
        alms_amount = self._invoice.alms_amount_in_local_currency

        alms_payment_json = {
            "guid": identifier.get_guid(),
            "creation_date": datetime.datetime.now().isoformat(),
            "company": config.CONSTANTS["COMPANY_NAME_UNKNOWN"],
            "description": self.description_prefix + " - alms",
            "invoice_guid": "",
            "direction": DIRECTION_OUT,
            "amount": alms_amount,
            "currency": config.CONSTANTS["HOME_CURRENCY"],
            "cleared": False,
        }

        alms_payment_date = self._invoice.alms_payment_date

        alms_payment_scheme_json = {
            "frequency": 1,
            "period": PERIOD_DAILY,
            "start": alms_payment_date.isoformat(),
            "repeat": 1,
            "recurrence": [
                {
                    "recurrence_date": alms_payment_date.isoformat(),
                    "expected_payment_date": alms_payment_date.isoformat(),
                    "amount": alms_amount,
                    "currency": config.CONSTANTS["HOME_CURRENCY"],
                    "cleared": False,
                    "collections": [],
                }
            ],
        }

        self._append_jsons_to_list(alms_payment_json, alms_payment_scheme_json)

    def _build_payment_list(self):
        self._payment_list = []

        # Incoming payment
        self._append_incoming_payment_to_list()

        # VAT
        if (
            self._invoice.is_vat_liable
            and self._invoice.vat_amount_in_local_currency > 0
        ):
            self._append_vat_transfer_to_list()
            self._append_vat_payment_to_list()

        # Income tax
        if self._invoice.income_tax_amount_in_local_currency > 0:
            self._append_itax_transfers_to_list()
            self._append_itax_payment_to_list()

        # Alms
        if self._invoice.alms_amount_in_local_currency > 0:
            self._append_alms_to_list()
