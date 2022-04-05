""" Notifications in main window """
import datetime
from typing import List
from model import payment
from model.payment import Payment
from model.activity import Activity
from util import amount as util_amount
from util import date_time


ICON_GREEN = "   "
ICON_YELLOW = " ~ "
ICON_RED = " ! "


def get_notifications() -> List:
    """ Builds and returns a notification list """
    output = []

    if not Activity.has_activity_for_today():
        output.append(ICON_YELLOW + "No activity entered for today")

    # Completed payments
    for pay in payment.get_completed_payments():
        line = ICON_GREEN + "Completed Payment"
        line += _get_payment_suffix(pay)
        output.append(line) # pylint: disable=C0301

    # Approaching or late payments
    for pay in get_raw_recurrence_list():
        output.append(pay[1])

    # Flush
    return output


def get_raw_recurrence_list() -> List:
    """ Returns the raw recurrence list """
    output = []
    today = datetime.date.today()

    payment.generate_high_time_recurrences()
    for pay, sch, recs in payment.get_approaching_or_late_recurrences(): # pylint: disable=W0612
        for rec in recs:
            amount, currency = rec.open_amount
            rec_date = rec.realistic_payment_date

            if rec_date.date() > today:
                icon = ICON_GREEN
            elif rec_date.date() == today:
                icon = ICON_YELLOW
            else:
                icon = ICON_RED

            output_text = icon + "Payment"
            output_text += _get_payment_suffix(
                pay=pay,
                rec_date=rec_date,
                amount=amount,
                currency=currency)

            output_line = (rec_date, output_text)
            output.append(output_line)

    output.sort(key=lambda x: x[0])
    return output

def _get_payment_suffix(pay: Payment,
                        rec_date: datetime.datetime = None,
                        amount: float = None,
                        currency: str = None) -> str:
    output = " (" + pay.direction + "):"
    if rec_date is not None:
        output += " " + date_time.get_formatted_date(rec_date)
    if amount is not None and currency is not None:
        output += " - "
        output += util_amount.get_formatted_amount(amount) + " " + currency
    output += " (" + pay.description + ") {" + pay.guid + "}"
    return output
