""" Income tax payment window """
import tkinter
from gui.amount_textbox import AmountTextbox
from config.constants import GUI_CELL_WIDTH, GUI_CELL_HEIGHT, HOME_GOVERNMENT, HOME_CURRENCY
import model.payment as payment


class PayIncomeTax:
    """ Income tax payment window """

    _WINDOW_WIDTH = 400
    _WINDOW_HEIGHT = 200

    def __init__(self):

        self._window = tkinter.Toplevel()
        self._window.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))
        cell_y = 0

        self._amount = AmountTextbox(self._window, "Amount", 0, HOME_CURRENCY, 0, cell_y)
        cell_y += GUI_CELL_HEIGHT

        save_button = tkinter.Button(self._window, text="OK", command=self._ok_click)
        save_button.place(x=GUI_CELL_WIDTH, y=cell_y)

    def _ok_click(self):

        payment.record_cash_movement(
            company=HOME_GOVERNMENT,
            direction=payment.DIRECTION_OUT,
            amount=self._amount.get_amount(),
            currency=self._amount.get_currency(),
            description="Geçici vergi ödemesi",
            income_tax_only=True
        )

        self._window.destroy()
