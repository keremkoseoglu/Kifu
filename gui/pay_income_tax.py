""" Income tax payment window """
import tkinter
from gui.amount_textbox import AmountTextbox
from gui.prime_singleton import PrimeSingleton
from gui.font import default_font
from model.payment import payment
import config


class PayIncomeTax:
    """ Income tax payment window """
    _WINDOW_WIDTH = 450
    _WINDOW_HEIGHT = 75

    def __init__(self):
        self._window = tkinter.Toplevel()
        self._window.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))
        cell_y = 0

        self._amount = AmountTextbox(
            self._window,
            "Amount",
            0,
            config.CONSTANTS["HOME_CURRENCY"],
            0,
            cell_y)

        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]
        save_button = tkinter.Button(self._window,
                                     text="OK",
                                     command=self._ok_click,
                                     font=default_font())
        save_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"], y=cell_y)

    def _ok_click(self):
        payment.record_cash_movement(
            company=config.CONSTANTS["HOME_GOVERNMENT"],
            direction=payment.DIRECTION_OUT,
            amount=self._amount.amount,
            currency=self._amount.currency,
            description="Geçici vergi ödemesi",
            income_tax_only=True
        )

        PrimeSingleton.get().refresh()
        self._window.destroy()
