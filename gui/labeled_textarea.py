""" Labeled text area control """
import tkinter
from config.constants import GUI_CELL_WIDTH


class LabeledTextarea:
    """ Labeled text area control """

    _LINE_FEED = "\r\n"

    def __init__(self,
                 parent: tkinter.Toplevel,
                 label_text: str,
                 text_value,
                 x_pos: int,
                 y_pos: int):
        self._parent = parent
        self._label = tkinter.Label(parent, text=label_text)
        self._label.place(x=x_pos, y=y_pos)
        self._text_box = tkinter.Text(parent, height=10)
        self._text_box.place(x=x_pos + GUI_CELL_WIDTH, y=y_pos)

        if isinstance(text_value, str):
            self.value = text_value
        elif isinstance(text_value, list):
            string_value = ""
            for val in text_value:
                string_value += val # pylint: disable=R1713
            self.value = string_value

    @property
    def value(self):
        """ Returns value of control """
        return self._text_box.get("1.0", tkinter.END)

    @value.setter
    def value(self, value):
        """ Sets value of control """
        if isinstance(value, str):
            self._text_box.insert(tkinter.INSERT, value)
        elif isinstance(value, list):
            string_value = ""
            for val in value:
                string_value += val # pylint: disable=R1713
            self.value = string_value
        self._parent.update()

    def disable(self):
        """ Disables control """
        self._text_box.configure(state="disabled")
