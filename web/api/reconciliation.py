""" Reconciliation module """
from typing import List
from model.payment import payment
from model.currency import CurrencyConverter
from web.api.payment_status import PaymentStatusAPI

class ReconciliationAPI():
    """ Reconciliation API """
    def __init__(self):
        self._out = {}
        self._company_dict = {}
        self._pay_stat_api = PaymentStatusAPI()
        self._curr = CurrencyConverter()

    def get_result(self, company_names: List[str]) -> dict:
        """ Returns payment status """
        payment.generate_high_time_recurrences()

        self._out = {"reconciliations": []}

        for company_name in company_names:
            self._company_dict = {"header": {"company": company_name,
                                             "inc_sum": 0,
                                             "out_sum": 0,
                                             "balance": 0},
                                  "incoming": [],
                                  "outgoing": []}

            self._process_open_payments(company_name)
            self._out["reconciliations"].append(self._company_dict)

        return self._out

    def _process_open_payments(self, company_name):
        open_payments = payment.get_open_payments_of_company(company_name)

        for open_payment in open_payments:
            open_payment_dict = self._pay_stat_api.get_result(open_payment.guid)
            open_amt = self._curr.convert_to_local_currency(
                open_payment_dict["summary"]["open_amount"],
                open_payment_dict["summary"]["currency"])

            if open_payment.direction == payment.DIRECTION_IN:
                self._company_dict["incoming"].append(open_payment_dict)
                self._company_dict["header"]["inc_sum"] += open_amt
                self._company_dict["header"]["balance"] += open_amt
            elif open_payment.direction == payment.DIRECTION_OUT:
                self._company_dict["outgoing"].append(open_payment_dict)
                self._company_dict["header"]["out_sum"] += open_amt
                self._company_dict["header"]["balance"] -= open_amt
