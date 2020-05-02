from model import payment
from model.activity import Activity
from util import amount as util_amount
from util import date_time
import datetime


ICON_GREEN = "   "
ICON_YELLOW = " ~ "
ICON_RED = " ! "


def get_notifications() -> []:
    output = []

    if not Activity.has_activity_for_today():
        output.append(ICON_YELLOW + "No activity entered for today")

    # Approaching or late payments
    for pay in get_raw_recurrence_list():
        output.append(pay[1])

    # Completed payments
    for pay in payment.get_completed_payments():
        output.append(ICON_GREEN + "Completed payment: " + pay.company.name + " - " + pay.description)

    # Flush
    return output


def get_raw_recurrence_list() -> []:
    output = []
    today = datetime.date.today()

    payment.generate_high_time_recurrences()
    for pay, sch, recs in payment.get_approaching_or_late_recurrences():
        for rec in recs:
            amount, currency = rec.open_amount
            rec_date = rec.realistic_payment_date

            if rec_date.date() > today:
                icon = ICON_GREEN
            elif rec_date.date() == today:
                icon = ICON_YELLOW
            else:
                icon = ICON_RED

            output_text = icon + "Payment" +\
                " (" + pay.direction + "): " +\
                date_time.get_formatted_date(rec_date) + " - " + \
                util_amount.get_formatted_amount(amount) + " " + currency + \
                " (" + pay.description + ") {" + pay.guid + "}"

            output_line = (rec_date, output_text)
            output.append(output_line)

    output.sort(key=lambda x: x[0])
    return output
