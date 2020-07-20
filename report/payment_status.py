""" Payment status report """
from report.html_report import HtmlReport
from util import amount, date_time
from model.payment import Payment


class PaymentStatusHtml:
    """ Payment status output """

    configs = {}
    on_loads = []

    def __init__(self):
        self.body = ""

    @staticmethod
    def footer_script() -> str:
        """ Builds and returns footer """
        output = ""
        output += "<script>"
        for config in PaymentStatusHtml.configs:
            output += "var " + config + " = " + PaymentStatusHtml.configs[config]
        output += "window.onload = function () { "
        for on_load in PaymentStatusHtml.on_loads:
            output += on_load
        output += "};"
        output += "</script>"
        return output

    @staticmethod
    def reset():
        """ Resets variables """
        PaymentStatusHtml.config = {}
        PaymentStatusHtml.on_loads = []

class PaymentStatus(HtmlReport):
    """ Payment status report """

    _REPORT_NAME = "Payment Status"
    _CHART_INDEX = 0

    def __init__(self):
        self._payment = None

    @staticmethod
    def get_html_for_payment(payment_obj: Payment,
                             with_title: bool = True,
                             with_description: bool = True,
                             subtitle_tag: str = "h2") -> PaymentStatusHtml:
        """ Generates HTML out of payment """
        output = PaymentStatusHtml()

        total_amount, curr = payment_obj.total_amount
        total_open_amount, curr = payment_obj.open_amount

        ##############################
        # HTML table
        ##############################

        if with_title:
            output.body += "<h1>Payment Status</h1>"
        output.body += "<" + subtitle_tag + ">Summary</" + subtitle_tag + ">"
        if with_description:
            output.body += payment_obj.company.name + " - " + payment_obj.description + "<br><br>"
        output.body += "Total amount: " + amount.get_formatted_amount(total_amount) + " " + curr + "<br>" # pylint: disable=C0301
        output.body += "Open amount: " + amount.get_formatted_amount(total_open_amount) + " " + curr + "<br>" # pylint: disable=C0301

        amt, curr = payment_obj.amount
        scheme = payment_obj.scheme
        freq, per = scheme.frequency

        output.body += "Payment plan: "
        output.body += amount.get_formatted_amount(amt) + " "
        output.body += curr + " every " + str(freq) + " "
        output.body += per + " x" + str(scheme.repeat)
        output.body += "; starting " + date_time.get_formatted_date(scheme.start_date)

        recurrences = scheme.recurrences

        if len(recurrences) > 0:
            output.body += "<" + subtitle_tag + ">Recurrence</" + subtitle_tag + ">"
            output.body += "<table border=0 cellspacing=4 cellpadding=4>"
            output.body += "<tr>"
            output.body += "<td>Recurrence date</td>"
            output.body += "<td align=right>Amount</td>"
            output.body += "<td align=right>Paid</td>"
            output.body += "<td align=right>Open</td>"
            output.body += "<td>Collections</td>"
            output.body += "</tr>"

            for rec in recurrences:
                amt, curr = rec.amount
                paid, curr = rec.paid_amount
                open_amt, curr = rec.open_amount

                output.body += "<tr>"
                output.body += "<td valign=top>" + date_time.get_formatted_date(rec.recurrence_date) + "</td>" # pylint: disable=C0301
                output.body += "<td align=right valign=top>" + amount.get_formatted_amount(amt) + " " + curr + "</td>" # pylint: disable=C0301
                output.body += "<td align=right valign=top>" + amount.get_formatted_amount(paid) + " " + curr + "</td>" # pylint: disable=C0301
                output.body += "<td align=right valign=top>" + amount.get_formatted_amount(open_amt) + " " + curr + "</td>" # pylint: disable=C0301

                output.body += "<td>"
                collections = rec.collections
                if len(collections) > 0:
                    output.body += "<table cellspacing=0 cellpadding=4 style='border-bottom: 1px solid #ddd;'>" # pylint: disable=C0301
                    for coll in collections:
                        coll_amo, coll_curr = coll.amount
                        output.body += "<tr>"
                        output.body += "<td><small>" + date_time.get_formatted_date(coll.date) + "</small></td>" # pylint: disable=C0301
                        output.body += "<td align=right><small>" + amount.get_formatted_amount(
                            coll_amo) + " " + coll_curr + "</small></td>"
                        output.body += "<td><small>" + coll.description + "</small></td>"
                        output.body += "</tr>"
                    output.body += "</table>"
                output.body += "</td>"

                output.body += "</tr>"

            output.body += "</table><hr>"

        ##############################
        # Chart
        ##############################

        PaymentStatus._CHART_INDEX += 1
        chart_area = "chart-area_" + str(PaymentStatus._CHART_INDEX)

        chart_paid = str(round(total_amount - total_open_amount))
        chart_open = str(round(total_open_amount))

        output.body += "<div id='canvas-holder-" + str(PaymentStatus._CHART_INDEX) + "'>"
        output.body += "<canvas id='" + chart_area + "'></canvas>"
        output.body += "</div>"

        config_var = "config_" + str(PaymentStatus._CHART_INDEX)
        config = "{"
        config += "type: 'pie',"
        config += "data: {"
        config += "datasets: [{"
        config += "data: ["
        config += chart_paid + ", "
        config += chart_open + "],"
        config += "backgroundColor: ['#00FF00', '#FF0000'],"
        config += "label: 'Status'"
        config += "}],"
        config += "labels: ['Paid: " + chart_paid + "', 'Open: " + chart_open + "']"
        config += "}, options: {responsive: true} };"
        PaymentStatusHtml.configs[config_var] = config

        ctx = "ctx_" + str(PaymentStatus._CHART_INDEX)
        on_load = "var " + ctx + " = document.getElementById('" + chart_area + "').getContext('2d');" # pylint: disable=C0301
        on_load += "window.myPie_" + str(PaymentStatus._CHART_INDEX) + " = new Chart(" + ctx + ", " + config_var + "); " # pylint: disable=C0301
        PaymentStatusHtml.on_loads.append(on_load)

        ##############################
        # Flush
        ##############################

        return output

    @staticmethod
    def get_payment_description(payment_obj: Payment) -> str:
        """ Payment description """
        return payment_obj.company.name + " - " + payment_obj.description

    def set_payment(self, payment_obj: Payment):
        """ Set payment """
        self._payment = payment_obj

    def _get_html_content(self) -> str:
        PaymentStatusHtml.reset()
        output = PaymentStatus.get_html_for_payment(self._payment)
        return output.body + " " + PaymentStatusHtml.footer_script()

    def _get_report_name(self) -> str:
        return self._REPORT_NAME
