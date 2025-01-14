""" Payment module """

import datetime
import json
import os
from typing import List
from model.company import Company
from model.bank.credit_card import get_credit_card_debts
from model.currency import CurrencyConverter
from model.investor import InvestmentAdviser
from model.payment.recurrence import Collection, Recurrence
from model.payment.scheme import Scheme
from model.budget import get_domain_dict, get_monthly_pyf_amount
from util import backup, date_time, identifier
import config

DIRECTION_IN = "I"
DIRECTION_OUT = "O"
DIRECTION_TRANSFER = "T"

PERIOD_DAILY = "D"
PERIOD_WEEKLY = "W"
PERIOD_MONTHLY = "M"
PERIOD_YEARLY = "Y"

_PAYMENT_FILE = "payment.json"


def get_payments():
    """All payments"""
    with open(_get_file_path(), encoding="utf-8") as payment_file:
        json_data = json.load(payment_file)
    return json_data


def delete_completed_payments():
    """Deletes completed payments"""
    completed_guids = []
    for completed_payment in get_completed_payments():
        completed_guids.append(completed_payment.guid)
    delete_payments(completed_guids)


def delete_payments(payment_guids: List):
    """Deletes given payments"""
    if payment_guids is None or len(payment_guids) <= 0:
        return
    all_payments = get_payments()
    new_payments = {"payments": []}
    for i in range(len(all_payments["payments"])):
        payment_i = all_payments["payments"][i]
        if payment_i["guid"] not in payment_guids:
            new_payments["payments"].append(payment_i)
    write_payments_to_disk(new_payments)


def generate_high_time_recurrences():
    """Generates approaching / due recurrences"""
    for payment_json in get_payments()["payments"]:
        payment_obj = Payment(payment_json)
        payment_obj.generate_high_time_recurrences()
        payment_obj.save()


def get_approaching_or_late_recurrences() -> List:
    """Returns approaching or late recurrences"""
    output = []
    for pay in get_payments()["payments"]:
        pay_obj = Payment(pay)
        if not pay_obj.cleared:
            scheme = pay_obj.scheme
            recs = scheme.approaching_or_late_recurrences
            if len(recs) > 0:
                output.append((pay_obj, scheme, recs))

    for output2 in output:
        output2[2].sort(key=lambda x: x.realistic_payment_date)

    output.sort(key=lambda x: x[2][0].realistic_payment_date)
    return output


def get_completed_payments() -> List:
    """Returns completed payments"""
    output = []

    for pay in get_payments()["payments"]:
        pay_obj = Payment(pay)
        open_amount, open_curr = pay_obj.open_amount  # pylint: disable=W0612
        if pay_obj.cleared or open_amount == 0:
            output.append(pay_obj)

    return output


def get_companies_without_payment() -> List[Company]:
    """Companies without payment
    Those may be considered deletable, in case
    they won't be needed in the future
    """
    output = []
    all_companies = Company.get_companies()
    all_payments = get_payments()
    for com in all_companies["companies"]:
        has_payment = False
        for pay in all_payments["payments"]:
            if pay["company"] == com["name"]:
                has_payment = True
                break
        if has_payment:
            continue
        com_obj = Company(com["name"])
        output.append(com_obj)
    return output


def get_direction_values() -> List:
    """Returns all payment directions as enum"""
    return [DIRECTION_IN, DIRECTION_OUT, DIRECTION_TRANSFER]


def get_open_vat_payments() -> List:
    """Returns open VAT payments"""
    output = []
    all_payments = get_payments()

    for payment in all_payments["payments"]:
        payment_obj = Payment(payment)
        if payment_obj.is_vat and (not payment_obj.cleared):
            output.append(payment_obj)
            continue

    return output


def get_open_income_tax_payments() -> List:
    """Returns open VAT payments"""
    output = []
    all_payments = get_payments()

    for payment in all_payments["payments"]:
        payment_obj = Payment(payment)
        if payment_obj.is_income_tax and (not payment_obj.cleared):
            output.append(payment_obj)
            continue

    return output


def get_open_payments_of_company(company: str) -> List:
    """Returns open payments of company"""
    output = []
    all_payments = get_payments()

    for payment in all_payments["payments"]:
        payment_obj = Payment(payment)
        payment_company = payment_obj.company.name
        payment_cleared = payment_obj.cleared

        if payment_company == company and (not payment_cleared):
            output.append(payment_obj)

    return output


def get_payment_balance() -> float:
    """Payment balance"""
    output = 0

    payment_dicts = get_payments()
    for payment_dict in payment_dicts["payments"]:
        payment = Payment(payment_dict)
        direction = payment.direction
        if direction == DIRECTION_TRANSFER:
            continue

        open_payment_amount = payment.open_amount_in_local_currency

        if direction == DIRECTION_IN:
            output += open_payment_amount
        else:
            output -= open_payment_amount

    return output


def get_period_values() -> List:
    """Returns all periods"""
    return [PERIOD_DAILY, PERIOD_WEEKLY, PERIOD_MONTHLY, PERIOD_YEARLY]


def record_cash_movement(
    company: str,
    direction: str,
    amount: float,
    currency: str,
    description: str,
    income_tax_only: bool = False,
):
    """Records a new cash movement"""
    ##############################
    # Preparation
    ##############################

    backup.execute()

    changed_payments = []
    curr_conv = CurrencyConverter()
    open_amount = amount
    open_payments = get_open_payments_of_company(company)
    date_iso = datetime.datetime.now().isoformat()

    ##############################
    # Deduct from open payments
    ##############################

    for payment in open_payments:
        if open_amount <= 0:
            break

        if payment.direction != direction:
            continue

        if income_tax_only and (not payment.is_income_tax):
            continue

        payment.generate_very_long_term_recurrences()

        scheme = payment.scheme
        recurrences = scheme.recurrences

        for recurrence in recurrences:
            if open_amount <= 0:
                break

            if not recurrence.cleared:
                rec_open_amount, rec_curr = recurrence.open_amount

                open_amount_conv = curr_conv.convert_to_currency(
                    from_amount=open_amount,
                    from_currency=currency,
                    to_currency=rec_curr,
                )

                if open_amount_conv >= rec_open_amount:
                    coll = {
                        "date": date_iso,
                        "description": description,
                        "amount": rec_open_amount,
                        "currency": rec_curr,
                    }
                    recurrence.add_collection(Collection(coll))
                    recurrence.cleared = True

                    remain_amount = open_amount_conv - rec_open_amount
                    open_amount = open_amount * (remain_amount / open_amount_conv)
                else:
                    coll = {
                        "date": date_iso,
                        "description": description,
                        "amount": open_amount_conv,
                        "currency": rec_curr,
                    }
                    recurrence.add_collection(Collection(coll))
                    open_amount = 0

        scheme.recurrences = recurrences
        payment.scheme = scheme
        if payment.open_amount[0] <= 0:
            payment.cleared = True
        changed_payments.append(payment)

    ##############################
    # Overpayment? Need to be paid back
    ##############################

    if open_amount > 0:
        if direction == DIRECTION_IN:
            pay_back_dir = DIRECTION_OUT
        else:
            pay_back_dir = DIRECTION_IN

        pay_back_dict = {
            "creation_date": date_iso,
            "company": company,
            "description": description + " - fazla ödeme iade",
            "direction": pay_back_dir,
            "amount": open_amount,
            "currency": currency,
            "cleared": False,
            "scheme": {
                "frequency": 1,
                "period": "D",
                "start": date_iso,
                "repeat": 1,
                "recurrence": [],
            },
        }

        changed_payments.append(Payment(pay_back_dict))

    ##############################
    # Finish
    ##############################

    for payment in changed_payments:
        payment.save()


def create_credit_card_transaction(
    bank: str,
    description: str,
    card: str,
    amount: float,
    currency: str = None,
    pay_date: str = None,
):
    """Creates a new credit card payment with the given details"""
    if currency is None:
        writeable_currency = config.CONSTANTS["HOME_CURRENCY"]
    else:
        writeable_currency = currency

    now_date = datetime.datetime.now().isoformat()

    if pay_date is None:
        writeable_date = now_date
    else:
        writeable_date = pay_date

    trn_pay_json = {
        "guid": identifier.get_guid(),
        "creation_date": now_date,
        "company": bank,
        "description": f"{description} - transfer to {card}",
        "invoice_guid": "",
        "direction": DIRECTION_TRANSFER,
        "amount": amount,
        "currency": writeable_currency,
        "cleared": False,
    }

    trn_scheme_json = {
        "frequency": 1,
        "period": PERIOD_DAILY,
        "start": writeable_date,
        "repeat": 1,
        "recurrence": [
            {
                "recurrence_date": writeable_date,
                "expected_payment_date": writeable_date,
                "amount": trn_pay_json["amount"],
                "currency": trn_pay_json["currency"],
                "cleared": False,
                "collections": [],
            }
        ],
    }

    trn_scheme = Scheme(trn_scheme_json)
    trn_pay = Payment(trn_pay_json)
    trn_pay.scheme = trn_scheme
    trn_pay.save()


def _create_investment_transaction(
    bank: str,
    description: str,
    trn_account: str,
    inv_account: str,
    amount: float,
    trn_date: datetime.datetime = None,
):

    post_trn_date = datetime.datetime.now() if trn_date is None else trn_date

    trn_pay_json = {
        "guid": identifier.get_guid(),
        "creation_date": post_trn_date.isoformat(),
        "company": bank,
        "description": f"{description} - transfer to {trn_account}",
        "invoice_guid": "",
        "direction": DIRECTION_TRANSFER,
        "amount": amount,
        "currency": config.CONSTANTS["HOME_CURRENCY"],
        "cleared": False,
    }

    trn_scheme_json = {
        "frequency": 1,
        "period": PERIOD_DAILY,
        "start": trn_pay_json["creation_date"],
        "repeat": 1,
        "recurrence": [
            {
                "recurrence_date": trn_pay_json["creation_date"],
                "expected_payment_date": trn_pay_json["creation_date"],
                "amount": trn_pay_json["amount"],
                "currency": trn_pay_json["currency"],
                "cleared": False,
                "collections": [],
            }
        ],
    }

    trn_scheme = Scheme(trn_scheme_json)
    trn_pay = Payment(trn_pay_json)
    trn_pay.scheme = trn_scheme

    inv_pay_json = {
        "guid": identifier.get_guid(),
        "creation_date": post_trn_date.isoformat(),
        "company": bank,
        "description": f"{description} - buy to {inv_account}",
        "invoice_guid": "",
        "direction": DIRECTION_TRANSFER,
        "amount": amount,
        "currency": config.CONSTANTS["HOME_CURRENCY"],
        "cleared": False,
    }

    inv_scheme_json = {
        "frequency": 1,
        "period": PERIOD_DAILY,
        "start": trn_pay_json["creation_date"],
        "repeat": 1,
        "recurrence": [
            {
                "recurrence_date": inv_pay_json["creation_date"],
                "expected_payment_date": inv_pay_json["creation_date"],
                "amount": inv_pay_json["amount"],
                "currency": inv_pay_json["currency"],
                "cleared": False,
                "collections": [],
            }
        ],
    }

    inv_scheme = Scheme(inv_scheme_json)
    inv_pay = Payment(inv_pay_json)
    inv_pay.scheme = inv_scheme

    trn_pay.save()
    inv_pay.save()


def record_investment_payment(
    investable_amount: float, paid_curr: str, description_prefix: str
):
    """Records a new investment payment into the most suitable account"""
    # Get investable amount
    investable_amount = CurrencyConverter().convert_to_local_currency(
        investable_amount, paid_curr
    )

    # Pay credit card debts
    if config.CONSTANTS["PAY_CREDIT_DEBT_BEFORE_INVESTMENT"]:
        credit_card_debts = get_credit_card_debts()
        for cc_debt in credit_card_debts.debts:
            if investable_amount < cc_debt.amount:
                payable_amount = investable_amount
                investable_amount = 0
            else:
                payable_amount = cc_debt.amount
                investable_amount -= payable_amount

            create_credit_card_transaction(
                cc_debt.bank_name, description_prefix, cc_debt.card_name, payable_amount
            )

            if investable_amount <= 0:
                return

    if investable_amount <= 0:
        return

    # Invest
    investments = InvestmentAdviser().advise(investable_amount)

    for inv in investments:
        _create_investment_transaction(
            inv["bank"],
            description_prefix,
            inv["account"],
            inv["account"],
            inv["amount"],
        )


def record_vat_payment(vat_guids: List, paid_amount: float, paid_curr: str):
    """Records a new VAT payment"""
    paid_vats = []
    all_vats = get_open_vat_payments()
    curr_conv = CurrencyConverter()
    vat_amount = 0

    for pay in all_vats:
        if pay.guid in vat_guids:
            paid_vats.append(pay)

    for pay in paid_vats:
        pay.generate_very_long_term_recurrences()
        debt_amount, debt_curr = pay.open_amount

        debt_amount_conv = curr_conv.convert_to_currency(
            from_amount=debt_amount, from_currency=debt_curr, to_currency=paid_curr
        )

        vat_amount += debt_amount_conv
        sch = pay.scheme
        recs = sch.recurrences
        if len(recs) != 1:
            raise Exception("Unexpected VAT scheme")
        rec = recs[0]

        coll_dict = {
            "date": datetime.datetime.now().isoformat(),
            "description": "KDV ödemesi",
            "amount": paid_amount,
            "currency": paid_curr,
        }

        coll = Collection(coll_dict)
        rec.add_collection(coll)
        rec.cleared = True

        sch.recurrences = recs
        pay.scheme = sch
        pay.cleared = True

    if vat_amount > paid_amount:
        investable_amount = vat_amount - paid_amount
        record_investment_payment(investable_amount, paid_curr, "VAT surplus")

    for pay in paid_vats:
        pay.save()


def create_pyf():
    """Pay yourself first"""
    pyf_day = get_domain_dict()["pyf_day"]
    now = datetime.datetime.now()
    pyf_date = datetime.datetime(now.year, now.month, pyf_day)

    pyf_amount = get_monthly_pyf_amount()
    investments = InvestmentAdviser().advise(pyf_amount)

    for inv in investments:
        _create_investment_transaction(
            inv["bank"],
            "Pay yourself first",
            inv["account"],
            inv["account"],
            inv["amount"],
            trn_date=pyf_date,
        )


class Payment:
    """Payment"""

    def __init__(self, payment: dict):
        self._payment = payment

    @property
    def amount(self) -> tuple:
        """Payment amount"""
        if "amount" not in self._payment:
            self._payment["amount"] = 0
        return float(self._payment["amount"]), self.currency

    @property
    def amount_in_local_currency(self) -> float:
        """Payment amount in home currency"""
        amount, currency = self.amount
        local_amount = CurrencyConverter().convert_to_local_currency(amount, currency)
        return local_amount

    @property
    def company(self) -> Company:
        """3rd party company"""
        if "company" not in self._payment:
            self._payment["company"] = config.CONSTANTS["HOME_COMPANY"]
        return Company(self._payment["company"])

    @company.setter
    def company(self, company: str):
        """3rd party company"""
        self._payment["company"] = company

    @property
    def description(self) -> str:
        """Payment description"""
        if "description" not in self._payment:
            self._payment["description"] = ""
        return self._payment["description"]

    @description.setter
    def description(self, description: str):
        """Payment description"""
        self._payment["description"] = description

    @property
    def direction(self) -> str:
        """Payment direction"""
        if "direction" not in self._payment:
            self._payment["direction"] = DIRECTION_OUT
        return self._payment["direction"]

    @direction.setter
    def direction(self, direction: str):
        """Payment direction"""
        self._payment["direction"] = direction

    @property
    def creation_date(self) -> datetime:
        """Payment creation date"""
        return date_time.parse_json_date(self._payment["creation_date"])

    @property
    def currency(self) -> str:
        """Payment currency"""
        if "currency" not in self._payment:
            self._payment["currency"] = config.CONSTANTS["HOME_CURRENCY"]
        return self._payment["currency"]

    @property
    def guid(self) -> str:
        """Unique payment guid"""
        if "guid" not in self._payment:
            self._payment["guid"] = identifier.get_guid()
        return self._payment["guid"]

    @property
    def invoice_guid(self) -> str:
        """Unique invoice guid"""
        if "invoice_guid" not in self._payment:
            self._payment["invoice_guid"] = ""
        return self._payment["invoice_guid"]

    @invoice_guid.setter
    def invoice_guid(self, guid: str):
        """Unique invoice guid"""
        self._payment["invoice_guid"] = guid

    @property
    def notes(self) -> str:
        """Payment notes"""
        if "notes" not in self._payment:
            self._payment["notes"] = ""
        return self._payment["notes"]

    @notes.setter
    def notes(self, notes: str):
        """Payment notes"""
        self._payment["notes"] = notes

    @property
    def open_amount(self) -> tuple:
        """Payment open amount"""
        currency_conv = CurrencyConverter()
        scheme = self.scheme

        open_amount, open_currency = self.amount

        if scheme.repeats_forever:
            return open_amount, open_currency

        open_amount *= self.scheme.repeat

        for rec in self.scheme.recurrences:
            paid_amount, paid_currency = rec.paid_amount
            converted_paid_amount = currency_conv.convert_to_currency(
                paid_amount, paid_currency, open_currency
            )
            open_amount -= converted_paid_amount

        return open_amount, open_currency

    @property
    def open_amount_in_local_currency(self) -> float:
        """Payment open amount in local currency"""
        open_amount, curr = self.open_amount
        local_amount = CurrencyConverter().convert_to_local_currency(open_amount, curr)
        return local_amount

    @property
    def scheme(self) -> Scheme:
        """Payment scheme"""
        scheme_dict = self._payment["scheme"]
        return Scheme(scheme_dict)

    @scheme.setter
    def scheme(self, scheme: Scheme):
        """Payment scheme"""
        self._payment["scheme"] = scheme.dict

    @property
    def total_amount(self) -> tuple:
        """Payment total amount and currency"""
        amt, curr = self.amount
        amt *= self.scheme.repeat
        return amt, curr

    @property
    def cleared(self) -> bool:
        """Is payment cleared"""
        if "cleared" not in self._payment:
            self._payment["cleared"] = False
        return self._payment["cleared"]

    @cleared.setter
    def cleared(self, cleared: bool):
        """Is payment cleared"""
        self._payment["cleared"] = cleared

    @property
    def is_income_tax(self) -> bool:
        """Is payment an income tax payment"""
        if "is_income_tax" not in self._payment:
            self._payment["is_income_tax"] = False
        return self._payment["is_income_tax"]

    @is_income_tax.setter
    def is_income_tax(self, is_tax: bool):
        """Is payment an income tax payment"""
        self._payment["is_income_tax"] = is_tax

    @property
    def is_vat(self) -> bool:
        """Is payment a VAT payment"""
        if "is_vat" not in self._payment:
            self._payment["is_vat"] = False
        return self._payment["is_vat"]

    @is_vat.setter
    def is_vat(self, is_tax: bool):
        """Is payment a VAT payment"""
        self._payment["is_vat"] = is_tax

    def generate_high_time_recurrences(self):
        """Generates recurrences which are approaching or due"""
        tick_limit_date = datetime.datetime.now() + datetime.timedelta(
            days=config.CONSTANTS["PAYMENT_RECURRENCE_BUFFER"]
        )  # pylint: disable=C0301
        self.generate_recurrences(tick_limit_date)

    def generate_recurrences(self, tick_limit_date: datetime.datetime):
        """Generates recurrences"""
        if self.cleared:
            return

        amount, currency = self.amount
        scheme = self.scheme
        start_date = scheme.start_date
        next_tick_date = start_date
        frequency, period = scheme.frequency
        scheme_changed = False
        repeat = scheme.repeat
        repeated = 0

        while True:
            if next_tick_date > tick_limit_date:
                break

            # Add recurrence if needed

            if not scheme.has_recurrence(next_tick_date):
                ticked_recurrence_dict = {
                    "recurrence_date": next_tick_date.isoformat(),
                    "expected_payment_date": next_tick_date.isoformat(),
                    "amount": amount,
                    "currency": currency,
                    "cleared": False,
                    "collections": [],
                }

                ticked_recurrence = Recurrence(ticked_recurrence_dict)
                scheme.add_recurrence(ticked_recurrence)
                scheme_changed = True

            # Tick next

            if period == PERIOD_YEARLY:
                next_tick_date = date_time.get_next_year(
                    next_tick_date, next_count=frequency
                )
            elif period == PERIOD_MONTHLY:
                next_tick_date = date_time.get_next_month(
                    next_tick_date, next_count=frequency
                )
            elif period == PERIOD_WEEKLY:
                next_tick_date = date_time.get_next_week(
                    next_tick_date, next_count=frequency
                )
            elif period == PERIOD_DAILY:
                next_tick_date = date_time.get_next_day(
                    next_tick_date, next_count=frequency
                )
            else:
                raise ValueError("Invalid period")

            # Repeat count?

            repeated += 1
            if repeated >= repeat:
                break

        if scheme_changed:
            self.scheme = scheme

    def generate_very_long_term_recurrences(self):
        """Generates very long term recurrences"""
        tick_limit_date = datetime.datetime.now() + datetime.timedelta(
            days=config.CONSTANTS["PAYMENT_LONG_RECURRENCE_BUFFER"]
        )  # pylint: disable=C0301
        self.generate_recurrences(tick_limit_date)

    def save(self):
        """Write payment to disk"""
        if "guid" not in self._payment:
            self._payment["guid"] = identifier.get_guid()
            self._payment["creation_date"] = datetime.datetime.now().isoformat()
        elif self._payment["guid"] == "":
            self._payment["guid"] = identifier.get_guid()
            self._payment["creation_date"] = datetime.datetime.now().isoformat()

        current_payments = get_payments()
        new_payments = {"payments": []}

        updated = False
        for pay in current_payments["payments"]:
            if pay["guid"] == self._payment["guid"]:
                new_payments["payments"].append(self._payment)
                updated = True
            else:
                new_payments["payments"].append(pay)

        if not updated:
            new_payments["payments"].append(self._payment)

        write_payments_to_disk(new_payments)

    def set_amount(self, amount: float, currency: str):
        """Set payment amount"""
        self._payment["amount"] = amount
        self._payment["currency"] = currency


def get_payment_with_guid(guid: str) -> Payment:
    """Returns a payment object having the provided GUID"""
    for pay in get_payments()["payments"]:
        if pay["guid"] == guid:
            return Payment(pay)
    return None


def write_payments_to_disk(payments: dict):
    """Write payments to disk"""
    with open(_get_file_path(), "w", encoding="utf-8") as payment_file:
        json.dump(payments, payment_file, indent=3)


def _get_file_path():
    return os.path.join(config.CONSTANTS["DATA_DIR_PATH"] + _PAYMENT_FILE)
