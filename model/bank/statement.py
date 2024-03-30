""" Bank statement """
from dataclasses import dataclass
from datetime import datetime
from typing import List, Protocol
from model.currency import CurrencyConverter

@dataclass
class StatementEntry():
    """ Bank statement entry """
    date: datetime = None
    text: str = ""
    amount: float = 0
    currency: str = ""

    def __post_init__(self):
        self._curr_conv = None

    @property
    def amount_in_home_currency(self) -> float:
        """ Amount in home currency """
        if self._curr_conv is None:
            self._curr_conv = CurrencyConverter()
        return self._curr_conv.convert_to_local_currency(self.amount, self.currency)

class AbstractStatementReader(Protocol):
    """ Statement reader class """
    def read(self) -> List[StatementEntry]:
        """ Reads statements """
