""" Labeled combobox control """
from typing import List
import tkinter
import config
from gui.font import default_font


class LabeledCombobox:
    """ Labeled combobox control """

    def __init__(self,
                 parent: tkinter.Toplevel,
                 label_text: str,
                 combo_values: List,
                 x_pos: int,
                 y_pos: int,
                 width=0):
        self._label = tkinter.Label(parent, text=label_text, font=default_font())
        self._label.place(x=x_pos, y=y_pos)
        self._selected_value = tkinter.StringVar()

        if width > 0:
            self._combobox = tkinter.ttk.Combobox(
                parent,
                textvariable=self._selected_value,
                width=150,
                font=default_font())
        else:
            self._combobox = tkinter.ttk.Combobox(
                parent,
                textvariable=self._selected_value,
                font=default_font())

        self._combobox.config(values=combo_values)
        self._combobox.place(x=x_pos + config.CONSTANTS["GUI_CELL_WIDTH"], y=y_pos)

    @property
    def selected_value(self) -> str:
        """ Returns selected value """
        return self._selected_value.get()

    @selected_value.setter
    def selected_value(self, value: str):
        """ Sets selected value """
        self._selected_value.set(value)
