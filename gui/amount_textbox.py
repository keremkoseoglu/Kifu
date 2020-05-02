from config.constants import *
import tkinter
from util import amount as util_amount

class AmountTextbox:

    def __init__(self, parent: tkinter.Toplevel, label_text: str, amount: float, currency: str, x_pos: int, y_pos: int):
        self._parent = parent
        self._label = tkinter.Label(parent, text=label_text)
        self._label.place(x=x_pos, y=y_pos)

        amount_width = int(GUI_CELL_WIDTH * 70 / 1000)
        self._amount_val = tkinter.StringVar()
        self._amount_val.set(util_amount.get_formatted_amount(amount))
        self._amount_box = tkinter.Entry(parent, textvariable=self._amount_val)
        self._amount_box.config(width=amount_width)
        self._amount_box.place(x=x_pos + GUI_CELL_WIDTH, y=y_pos)

        currency_width = int((GUI_CELL_WIDTH / 10) - amount_width)
        self._currency_val = tkinter.StringVar()
        self._currency_val.set(currency)
        self._currency_box = tkinter.Entry(parent, textvariable=self._currency_val)
        self._currency_box.config(width=currency_width)
        self._currency_box.place(x=x_pos + GUI_CELL_WIDTH + (amount_width * 10), y=y_pos)

    def disable(self):
        self._amount_box.configure(state="disabled")
        self._currency_box.configure(state="disabled")

    def get_amount(self) -> float:
        x = self._amount_val.get()
        x = x.replace(",", "")
        return float(x)

    def get_currency(self):
        return self._currency_val.get()

    def set_value(self, amount: float, currency: str):
        self._amount_val.set(util_amount.get_formatted_amount(amount))
        self._currency_val.set(currency)
        self._parent.update()