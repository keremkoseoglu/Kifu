from report.html_report import HtmlReport
from util import amount, date_time
from model.payment import Payment


class PaymentStatus(HtmlReport):

    _REPORT_NAME = "Payment Status"

    def __init__(self):
        self._payment = None

    @staticmethod
    def get_html_for_payment(p: Payment,
                             with_title: bool = True,
                             with_description: bool = True,
                             subtitle_tag: str = "h2"):
        output = ""

        total_amount, curr = p.total_amount
        total_open_amount, curr = p.open_amount

        if with_title:
            output += "<h1>Payment Status</h1>"
        output += "<" + subtitle_tag + ">Summary</" + subtitle_tag + ">"
        if with_description:
            output += p.company.name + " - " + p.description + "<br><br>"
        output += "Total amount: " + amount.get_formatted_amount(total_amount) + " " + curr + "<br>"
        output += "Open amount: " + amount.get_formatted_amount(total_open_amount) + " " + curr + "<br>"

        amt, curr = p.amount
        scheme = p.scheme
        freq, per = scheme.frequency

        output += "Payment plan: " + amount.get_formatted_amount(amt) + " " + curr + " every " + str(
            freq) + " " + per + " x" + str(scheme.repeat) + "; starting " + date_time.get_formatted_date(
            scheme.start_date)

        recurrences = scheme.recurrences

        if len(recurrences) > 0:

            output += "<" + subtitle_tag + ">Recurrence</" + subtitle_tag + ">"
            output += "<table border=0 cellspacing=4 cellpadding=4>"
            output += "<tr>"
            output += "<td>Recurrence date</td>"
            output += "<td align=right>Amount</td>"
            output += "<td align=right>Paid</td>"
            output += "<td align=right>Open</td>"
            output += "<td>Collections</td>"
            output += "</tr>"

            for rec in recurrences:
                amt, curr = rec.amount
                paid, curr = rec.paid_amount
                open_amt, curr = rec.open_amount

                output += "<tr>"
                output += "<td valign=top>" + date_time.get_formatted_date(rec.recurrence_date) + "</td>"
                output += "<td align=right valign=top>" + amount.get_formatted_amount(amt) + " " + curr + "</td>"
                output += "<td align=right valign=top>" + amount.get_formatted_amount(paid) + " " + curr + "</td>"
                output += "<td align=right valign=top>" + amount.get_formatted_amount(open_amt) + " " + curr + "</td>"

                output += "<td>"
                collections = rec.collections
                if len(collections) > 0:
                    output += "<table cellspacing=0 cellpadding=4 style='border-bottom: 1px solid #ddd;'>"
                    for coll in collections:
                        coll_amo, coll_curr = coll.amount
                        output += "<tr>"
                        output += "<td><small>" + date_time.get_formatted_date(coll.date) + "</small></td>"
                        output += "<td align=right><small>" + amount.get_formatted_amount(
                            coll_amo) + " " + coll_curr + "</small></td>"
                        output += "<td><small>" + coll.description + "</small></td>"
                        output += "</tr>"
                    output += "</table>"
                output += "</td>"

                output += "</tr>"

            output += "</table>"

        return output

    @staticmethod
    def get_payment_description(p: Payment) -> str:
        return p.company.name + " - " + p.description

    def set_payment(self, p: Payment):
        self._payment = p

    def _get_html_content(self) -> str:
        return PaymentStatus.get_html_for_payment(self._payment)

    def _get_report_name(self) -> str:
        return self._REPORT_NAME