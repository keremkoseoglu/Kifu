""" Cash movement GUI """
import tkinter
from gui.amount_textbox import AmountTextbox
from gui.company_combobox import CompanyCombobox
from gui.labeled_textbox import LabeledTextbox
from gui.labeled_combobox import LabeledCombobox
from gui.prime_singleton import PrimeSingleton
from gui.font import default_font
import model.payment as payment
import config


class CashMovement:
    """ GUI to record a cash movement
    The movement may be an incoming, outcoming or transfer payment
    """
    _WINDOW_WIDTH = 450
    _WINDOW_HEIGHT = 200

    def __init__(self):
        self._window = tkinter.Toplevel()
        self._window.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))
        cell_y = 0

        self._company = CompanyCombobox(self._window, "Company", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._direction = LabeledCombobox(self._window, "Direction", ["I", "O"], 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._amount = AmountTextbox(
            self._window,
            "Amount",
            0,
            config.CONSTANTS["HOME_CURRENCY"],
            0,
            cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._description = LabeledTextbox(self._window, "Description", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        save_button = tkinter.Button(self._window,
                                     text="OK",
                                     command=self._ok_click,
                                     font=default_font())
        save_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"], y=cell_y)

    def _ok_click(self):

        payment.record_cash_movement(
            company=self._company.company_name,
            direction=self._direction.selected_value,
            amount=self._amount.amount,
            currency=self._amount.currency,
            description=self._description.value
        )

        PrimeSingleton.get().refresh()
        self._window.destroy()
