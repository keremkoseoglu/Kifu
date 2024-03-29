""" Labeled textbox """
import tkinter
import config
from gui.font import default_font


class LabeledTextbox:
    """ Labeled textbox """
    def __init__(self,
                 parent: tkinter.Toplevel,
                 label_text: str,
                 text_value: str,
                 x_pos: int,
                 y_pos: int):
        self._parent = parent
        self._label = tkinter.Label(parent, text=label_text, font=default_font())
        self._label.place(x=x_pos, y=y_pos)
        self._text_val = tkinter.StringVar()
        self._text_val.set(text_value)
        self._text_box = tkinter.Entry(parent, textvariable=self._text_val, font=default_font())
        self._text_box.place(x=x_pos + config.CONSTANTS["GUI_CELL_WIDTH"], y=y_pos)

    @property
    def value(self):
        """ Returns the value in the textbox """
        return self._text_val.get()

    @value.setter
    def value(self, value: str):
        """ Sets the value into the textbox """
        self._text_val.set(value)
        self._parent.update()

    def disable(self):
        """ Disables the textbox """
        self._text_box.configure(state="disabled")
