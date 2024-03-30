""" Recurrence module """
from dataclasses import dataclass
import datetime
import config
from model.currency import CurrencyConverter
from util import date_time

@dataclass
class Collection:
    """ Money collection """
    collection: dict

    @property
    def amount(self) -> tuple:
        """ Collection amount """
        return float(self.collection["amount"]), self.collection["currency"]

    @property
    def date(self) -> datetime:
        """ Collection date """
        return date_time.parse_json_date(self.collection["date"])

    @property
    def description(self) -> str:
        """ Description """
        return self.collection["description"]

    @property
    def json(self) -> dict:
        """ Collection in JSON format """
        return self.collection

@dataclass
class Recurrence:
    """ Payment recurrence """
    recurrence: dict

    @property
    def amount(self) -> tuple:
        """ Amount """
        return float(self.recurrence["amount"]), self.currency

    @property
    def collections(self) -> list:
        """ All collections in recurrence """
        output = []
        for col in self.recurrence["collections"]:
            output.append(Collection(col))
        return output

    @property
    def currency(self) -> str:
        """ Currency """
        return self.recurrence["currency"]

    @property
    def expected_payment_date(self) -> datetime:
        """ Expected payment date """
        return date_time.parse_json_date(self.recurrence["expected_payment_date"])

    @expected_payment_date.setter
    def expected_payment_date(self, date: datetime):
        """ Expected payment date """
        self.recurrence["expected_payment_date"] = date.isoformat()

    @property
    def open_amount(self) -> tuple:
        """ Open amount """
        if self.cleared:
            return 0, self.currency

        open_amount, open_currency = self.amount
        currency_conv = CurrencyConverter()

        for coll in self.collections:
            coll_amount, coll_curr = coll.amount
            converted_coll_amount = currency_conv.convert_to_currency(
                coll_amount,
                coll_curr,
                open_currency)
            open_amount -= converted_coll_amount

        return open_amount, open_currency

    @property
    def paid_amount(self) -> tuple:
        """ Paid amount """
        full_amount, full_currency = self.amount
        open_amount, open_currency = self.open_amount
        assert full_currency == open_currency
        return (full_amount - open_amount), full_currency

    @property
    def realistic_payment_date(self) -> datetime:
        """ Realistic payment date """
        epd = self.expected_payment_date
        rcd = self.recurrence_date

        if epd > rcd:
            output = epd
        else:
            output = rcd

        return date_time.get_nearest_workday(output, backwards=True)

    @property
    def json(self) -> dict:
        """ Recurrence as JSON (dict) """
        return self.recurrence

    @property
    def recurrence_date(self) -> datetime:
        """ Recurrence date """
        return date_time.parse_json_date(self.recurrence["recurrence_date"])

    @property
    def approaching_or_late(self) -> bool:
        """ Is recurrence approaching or late? """
        if self.cleared:
            return False
        return self.recurrence_date <= datetime.datetime.now() + datetime.timedelta(
            days=config.CONSTANTS["PAYMENT_NOTIFICATION_BUFFER"])

    @property
    def cleared(self) -> bool:
        """ Is recurrence cleared? """
        return self.recurrence["cleared"]

    @cleared.setter
    def cleared(self, cleared: bool):
        """ Is recurrence cleared? """
        self.recurrence["cleared"] = cleared

    def add_collection(self, collection: Collection):
        """ Add new collection """
        self.recurrence["collections"].append(collection.json)

    def toggle_cleared(self):
        """ Toggle cleared forth and back """
        if self.cleared:
            self.cleared = False
        else:
            self.cleared = True
