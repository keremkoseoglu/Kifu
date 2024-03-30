""" Single value popup window """
import tkinter
from gui.labeled_textbox import LabeledTextbox


class PopupWithSingleValue:
    """ Single value popup window """

    _WINDOW_WIDTH = 400
    _WINDOW_HEIGHT = 200

    def __init__(self, click_handler, label_text: str, text_value: str):

        self._click_handler = click_handler

        self._window = tkinter.Toplevel()
        self._window.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))

        self._labeled_textbox = LabeledTextbox(self._window, label_text, text_value, 0, 0)

        save_button = tkinter.Button(self._window, text="OK", command=self._ok_click)
        save_button.place(x=200, y=100)

    def _ok_click(self):
        self._click_handler(self._labeled_textbox.value)
        self._window.destroy()
