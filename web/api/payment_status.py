""" Payment status API """
from util import amount, date_time
from model.payment import get_payment_with_guid
from web.api.chart import get_pie_dict

class PaymentStatusAPI():
    """ Payment status API """
    def __init__(self):
        self._out = {}
        self._payment = None

    def get_result(self, guid: str) -> dict:
        """ Returns payment status """
        self._out = {"summary": {}, "recurrences": [], "PieChart": {}}

        if guid is None:
            return self._out

        self._payment = get_payment_with_guid(guid)
        if self._payment is None:
            return self._out

        self._build_summary()
        self._build_recurrences()
        self._build_pie()

        return self._out

    def _build_summary(self):
        total_amount, curr = self._payment.total_amount
        total_open_amount, curr = self._payment.open_amount
        paid_amount = total_amount - total_open_amount

        if total_amount == 0:
            paid_perc = 0
        else:
            paid_perc = int(paid_amount * 100 / total_amount)

        amt, curr = self._payment.amount
        scheme = self._payment.scheme
        freq, per = scheme.frequency
        pay_plan = amount.get_formatted_amount(amt) + " "
        pay_plan += curr + " every " + str(freq) + " "
        pay_plan += per + " x" + str(scheme.repeat)
        pay_plan += "; starting " + date_time.get_formatted_date(scheme.start_date)

        self._out["summary"] = {"description": self._payment.description,
                                "company": self._payment.company.name,
                                "total_amount": total_amount,
                                "open_amount": total_open_amount,
                                "paid_amount": paid_amount,
                                "paid_perc": paid_perc,
                                "currency": curr,
                                "pay_plan": pay_plan}

    def _build_recurrences(self):
        recurrences = self._payment.scheme.recurrences

        for rec in recurrences:
            amt, curr = rec.amount # pylint: disable=W0612
            paid, curr = rec.paid_amount
            open_amt, curr = rec.open_amount
            date = date_time.get_formatted_date(rec.recurrence_date)

            rec_dict = {"date": date,
                        "amount": amt,
                        "paid": paid,
                        "open": open_amt,
                        "collections": []}

            collections = rec.collections

            for coll in collections:
                coll_amo, coll_curr = coll.amount
                coll_dict = {"date": date_time.get_formatted_date(coll.date),
                             "amount": coll_amo,
                             "currency": coll_curr,
                             "description": coll.description}
                rec_dict["collections"].append(coll_dict)

            self._out["recurrences"].append(rec_dict)

    def _build_pie(self):
        pie_list = [{"label": "paid",
                     "value": self._out["summary"]["paid_amount"]},
                    {"label": "open",
                     "value": self._out["summary"]["open_amount"]},
                    {"label": "total",
                     "value": self._out["summary"]["total_amount"]}]

        self._out["PieChart"] = get_pie_dict(entries=pie_list,
                                             label_fld="label",
                                             val_fld="value")
