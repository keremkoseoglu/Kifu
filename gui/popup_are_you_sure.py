import tkinter


class PopupAreYouSure:

    _WINDOW_WIDTH = 400
    _WINDOW_HEIGHT = 200

    def __init__(self, ok_handler, label_text: str):

        self._ok_handler = ok_handler

        self._window = tkinter.Toplevel()
        self._window.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))

        self._label = tkinter.Label(self._window, text=label_text)
        self._label.place(x=0, y=0)

        ok_button = tkinter.Button(self._window, text="OK", command=self._ok_click)
        ok_button.place(x=200, y=100)

        cancel_button = tkinter.Button(self._window, text="OK", command=self._cancel_click)
        cancel_button.place(x=200, y=100)

    def _ok_click(self):
        self._ok_handler()
        self._window.destroy()

    def _cancel_click(self):
        self._window.destroy()