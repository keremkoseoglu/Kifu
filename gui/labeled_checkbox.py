""" Labeled checkbox """
import tkinter
import config
from gui.font import default_font


class LabeledCheckbox:
    """ Labeled checkbox """

    def __init__(self, parent: tkinter.Toplevel, label_text: str, x_pos: int, y_pos: int):
        self._label = tkinter.Label(parent, text=label_text, font=default_font())
        self._label.place(x=x_pos, y=y_pos)

        self._val = tkinter.BooleanVar()
        self._checkbox = tkinter.Checkbutton(parent, text="", variable=self._val)
        self._checkbox.place(x=x_pos + config.CONSTANTS["GUI_CELL_WIDTH"], y=y_pos)

    @property
    def checked(self) -> bool:
        """ Returns true if the checkbox is checked """
        return self._val.get()

    @checked.setter
    def checked(self, val: bool):
        """ Sets the checkbox """
        self._val.set(val)
