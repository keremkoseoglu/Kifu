""" Payment scheme module """
from dataclasses import dataclass
from typing import List
import datetime
from model.payment.recurrence import Recurrence
from util import date_time

@dataclass
class Scheme:
    """ Payment scheme """
    scheme: dict

    @property
    def approaching_or_late_recurrences(self) -> List:
        """ Returns all approaching or late recurrences """
        output = []
        for rec in self.recurrences:
            if rec.approaching_or_late:
                output.append(rec)
        return output

    @property
    def frequency(self) -> tuple:
        """ Payment frequency """
        return self.scheme["frequency"], self.scheme["period"]

    @property
    def dict(self) -> dict:
        """ Returns scheme as a dict """
        return self.scheme

    @property
    def earliest_uncleared_recurrence(self) -> Recurrence:
        """ Earliest uncleared recurrence """
        all_recurrences = self.recurrences
        if len(all_recurrences) == 0:
            return None

        all_recurrences.sort(key=lambda x: x.recurrence_date)

        for rec in all_recurrences:
            if not rec.cleared:
                return rec

        return None

    @property
    def next_significant_date(self) -> datetime:
        """ Next significant date """
        next_recurrence = self.earliest_uncleared_recurrence
        if next_recurrence is not None:
            return next_recurrence.realistic_payment_date
        if self.has_cleared_recurrence:
            return datetime.datetime(year=8888, month=12, day=31)
        return self.start_date

    @property
    def recurrences(self) -> list:
        """ All recurrences """
        output = []
        for rec in self.scheme["recurrence"]:
            output.append(Recurrence(rec))
        return output

    @recurrences.setter
    def recurrences(self, recurrences: List):
        """ All recurrences """
        self.clear_recurrences()
        for rec in recurrences:
            self.add_recurrence(rec)

    @property
    def repeat(self) -> int:
        """ How many times the scheme will repeat """
        return self.scheme["repeat"]

    @repeat.setter
    def repeat(self, repeat: int):
        """ How many times the scheme will repeat """
        self.scheme["repeat"] = repeat

    @property
    def start_date(self) -> datetime:
        """ Scheme start date """
        if "start" not in self.scheme:
            self.scheme["start"] = datetime.datetime.now().isoformat()
        return date_time.parse_json_date(self.scheme["start"])

    @property
    def has_cleared_recurrence(self) -> bool:
        """ If scheme has any cleared recurrence, returns true """
        for rec in self.recurrences:
            if rec.cleared:
                return True
        return False

    @property
    def repeats_forever(self) -> bool:
        """ If scheme repeats forever, returns true """
        if "repeat_forever" in self.scheme:
            return self.scheme["repeat_forever"]
        return False

    def set_start_date_from_iso(self, start_date: str):
        """ Set start date """
        self.scheme["start"] = start_date

    def add_recurrence(self, recurrence: Recurrence):
        """ Adds a new recurrence """
        self.scheme["recurrence"].append(recurrence.json)

    def clear_recurrences(self):
        """ Initializes recurrences completely """
        self.scheme["recurrence"] = []

    def get_recurrence_on_date(self, year: int, month: int, day: int) -> Recurrence:
        """ Returns recurrence on given date """
        for rec in self.recurrences:
            rec_date = rec.recurrence_date
            if rec_date.year == year and rec_date.month == month and rec_date.day == day:
                return rec
        return None

    def has_recurrence(self, on_date: datetime.datetime) -> bool:
        """ Returns true if has recurrence on the given date """
        for rec in self.recurrences:
            if date_time.equals(rec.recurrence_date, on_date):
                return True
        return False

    def set_frequency(self, frequency: int, period: str):
        """ Sets payment frequency """
        self.scheme["frequency"] = frequency
        self.scheme["period"] = period
