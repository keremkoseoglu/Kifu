""" Reconciliation report """
from typing import List
from model.company import Company
from model import payment
from report.html_report import HtmlReport
from report.payment_status import PaymentStatus, PaymentStatusHtml
from util.amount import get_formatted_amount
import config


class ReconciliationCursor:
    """ Reconciliation cursor """
    def __init__(self, company: Company = None):
        self._company = company
        self.output = ""
        self._open_payments = []
        self._open_payments_read = False

    @property
    def balance(self) -> float:
        """ Reconciliation balance """
        return self.open_incoming_amount - self.open_outgoing_amount

    @property
    def company(self) -> Company:
        """ Reconciliation company """
        return self._company

    @company.setter
    def company(self, company: Company):
        """ Reconciliation company """
        self._company = company
        self._open_payments = []
        self._open_payments_read = False

    @property
    def open_payments(self) -> List[payment.Payment]:
        """ Open payments """
        if not self._open_payments_read:
            if self._company is not None:
                self._open_payments = payment.get_open_payments_of_company(self.company.name)
            self._open_payments_read = True
        return self._open_payments

    @property
    def open_incoming_amount(self) -> float:
        """ Open incoming amount """
        return ReconciliationCursor._get_amount_sum_of_payments(self.open_incoming_payments)

    @property
    def open_incoming_payments(self) -> List[payment.Payment]:
        """ Open incoming payments """
        return self._get_open_payments_with_direction(payment.DIRECTION_IN)

    @property
    def open_outgoing_amount(self) -> float:
        """ Open outgoing amount """
        return ReconciliationCursor._get_amount_sum_of_payments(self.open_outgoing_payments)

    @property
    def open_outgoing_payments(self) -> List[payment.Payment]:
        """ Open outgoing payments """
        return self._get_open_payments_with_direction(payment.DIRECTION_OUT)

    @staticmethod
    def _get_amount_sum_of_payments(payments: List[payment.Payment]) -> float:
        output = 0
        for pay in payments:
            output += pay.open_amount_in_local_currency
        return output

    def _get_open_payments_with_direction(self, direction: str) -> List[payment.Payment]:
        output = []
        for open_payment in self.open_payments:
            if open_payment.direction == direction:
                output.append(open_payment)
        return output


class Reconciliation(HtmlReport):
    """ Reconciliation report """
    _REPORT_NAME = "Reconciliation"

    def __init__(self, companies: List[Company]):
        self._companies = companies
        self._cursor = ReconciliationCursor()
        self._output = ""

    def _append_amount_in_home_currency(self, value: float):
        self._cursor.output += get_formatted_amount(value)
        self._cursor.output += " " + config.CONSTANTS["HOME_CURRENCY_SYMBOL"]

    def _append_separator_cell(self):
        self._cursor.output += "<td bgcolor=#cc0000>&nbsp;</td>"

    def _append_sum_cell(self, value: float):
        self._cursor.output += "<td><b>∑ "
        self._append_amount_in_home_currency(value)
        self._cursor.output += "</b></td>"

    def _generate_html_for_cursor(self):
        self._cursor.output = "<h1>" + self._cursor.company.name + " - Reconciliation</h1>"

        self._cursor.output += "<h2>Balance: "
        self._append_amount_in_home_currency(self._cursor.balance)
        self._cursor.output += "</h2>"

        self._cursor.output += "<table border=0 cellspacing=10>"
        self._cursor.output += "<tr>"
        self._generate_html_for_cursor_payments(self._cursor.open_incoming_payments, "Incoming")
        self._append_separator_cell()
        self._generate_html_for_cursor_payments(self._cursor.open_outgoing_payments, "Outgoing")
        self._cursor.output += "</tr>"

        self._cursor.output += "<tr>"
        self._append_sum_cell(self._cursor.open_incoming_amount)
        self._append_separator_cell()
        self._append_sum_cell(self._cursor.open_outgoing_amount)
        self._cursor.output += "</tr>"

        self._cursor.output += "</table>"

    def _generate_html_for_cursor_payments(self,
                                           payments: List[payment.Payment],
                                           title: str):
        self._cursor.output += "<td align=left valign=top>"
        self._cursor.output += "<h2>" + title + "</h2>"

        if len(payments) <= 0:
            self._cursor.output += "(None)"
            return

        first_payment = True
        for pay in payments:
            if not first_payment:
                self._cursor.output += "<hr>"
            self._cursor.output += "<h3>" + pay.description + "</h3>"
            self._cursor.output += PaymentStatus.get_html_for_payment(
                pay,
                with_title=False,
                with_description=False,
                subtitle_tag="h4").body
            first_payment = False

        self._cursor.output += "</td>"

    def _get_html_content(self) -> str:
        self._output = ""
        PaymentStatusHtml.reset()
        payment.generate_high_time_recurrences()
        for company in self._companies:
            self._cursor = ReconciliationCursor(company=company)
            self._generate_html_for_cursor()
            if self._output != "":
                self._output += "<br><hr>"
            self._output += self._cursor.output
        self._output += PaymentStatusHtml.footer_script()
        return self._output

    def _get_report_name(self) -> str:
        return self._REPORT_NAME
