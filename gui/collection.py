""" Money collection window """
import datetime
import tkinter
from gui.amount_textbox import AmountTextbox
from gui.labeled_checkbox import LabeledCheckbox
from gui.labeled_textbox import LabeledTextbox
from config.constants import GUI_CELL_WIDTH, GUI_CELL_HEIGHT
from model.payment import Collection as Collection_Model


class Collection:
    """ Money collection window """

    _WINDOW_WIDTH = 400
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
        cell_y += GUI_CELL_HEIGHT

        self._description = LabeledTextbox(self._window, "Description", "", 0, cell_y)
        cell_y += GUI_CELL_HEIGHT

        self._amount = AmountTextbox(self._window, "Amount", 0, default_currency, 0, cell_y)
        cell_y += GUI_CELL_HEIGHT

        self._cleared = LabeledCheckbox(self._window, "Clear", 0, cell_y)
        cell_y += GUI_CELL_HEIGHT

        save_button = tkinter.Button(self._window, text="OK", command=self._ok_click)
        save_button.place(x=GUI_CELL_WIDTH, y=cell_y)

    def _ok_click(self):

        collection_dict = {
            "date": self._date.get_value(),
            "description": self._description.get_value(),
            "amount": self._amount.get_amount(),
            "currency": self._amount.get_currency()
        }

        collection_obj = Collection_Model(collection_dict)

        self._click_handler(collection_obj, clear=self._cleared.is_checked())
        self._window.destroy()
