""" Money collection window """
import datetime
import tkinter
from gui.amount_textbox import AmountTextbox
from gui.labeled_checkbox import LabeledCheckbox
from gui.labeled_textbox import LabeledTextbox
from gui.prime_singleton import PrimeSingleton
from gui.font import default_font
from model.payment.recurrence import Collection as Collection_Model
import config


class Collection:
    """ Money collection window """

    _WINDOW_WIDTH = 450
    _WINDOW_HEIGHT = 200

    def __init__(self, click_handler, default_currency: str):
        self._click_handler = click_handler

        self._window = tkinter.Toplevel()
        self._window.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))
        cell_y = 0

        self._date = LabeledTextbox(
            self._window,
            "Date",
            datetime.datetime.now().isoformat(),
            0,
            cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._description = LabeledTextbox(self._window, "Description", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._amount = AmountTextbox(self._window, "Amount", 0, default_currency, 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._cleared = LabeledCheckbox(self._window, "Clear", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        save_button = tkinter.Button(self._window,
                                     text="OK",
                                     command=self._ok_click,
                                     font=default_font())
        save_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"], y=cell_y)

    def _ok_click(self):

        collection_dict = {
            "date": self._date.value,
            "description": self._description.value,
            "amount": self._amount.amount,
            "currency": self._amount.currency
        }

        collection_obj = Collection_Model(collection_dict)

        self._click_handler(collection_obj, clear=self._cleared.checked)
        PrimeSingleton.get().refresh()
        self._window.destroy()
