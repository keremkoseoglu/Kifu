""" Credit card statement GUI """
import datetime
import tkinter
from gui.amount_textbox import AmountTextbox
from gui.company_combobox import CompanyCombobox
from gui.labeled_textbox import LabeledTextbox
from gui.prime_singleton import PrimeSingleton
import model.payment as payment
import config

class CreditCardStatement:
    """ GUI to record credit card statement """
    _WINDOW_WIDTH = 400
    _WINDOW_HEIGHT = 200

    def __init__(self):
        self._window = tkinter.Toplevel()
        self._window.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))
        cell_y = 0

        self._company = CompanyCombobox(self._window, "Bank", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._payment_date = LabeledTextbox(self._window,
                                            "Payment date",
                                            datetime.datetime.now().isoformat(),
                                            0,
                                            cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._amount = AmountTextbox(
            self._window,
            "Amount",
            0,
            config.CONSTANTS["HOME_CURRENCY"],
            0,
            cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        save_button = tkinter.Button(self._window, text="OK", command=self._ok_click)
        save_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"], y=cell_y)

    def _ok_click(self):
        payment.create_credit_card_transaction(
            bank=self._company.company_name,
            description=self._company.company_name + " statement",
            card="credit card",
            amount=self._amount.amount,
            currency=self._amount.currency,
            pay_date=self._payment_date.value
        )

        PrimeSingleton.get().refresh()
        self._window.destroy()
