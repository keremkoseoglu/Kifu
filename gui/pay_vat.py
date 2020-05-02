import tkinter
from gui.amount_textbox import AmountTextbox
from config.constants import *
import model.payment as payment
from util import amount


class PayVat:
    _NOTIF_HEIGHT = 250
    _WINDOW_WIDTH = 800
    _WINDOW_HEIGHT = 400

    def __init__(self):

        self._window = tkinter.Toplevel()
        self._window.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))
        cell_y = 0

        self._amount = AmountTextbox(self._window, "Amount", 0, HOME_CURRENCY, 0, cell_y)
        cell_y += GUI_CELL_HEIGHT

        self._vat_list = tkinter.Listbox(self._window, selectmode=tkinter.MULTIPLE)
        self._refresh()
        self._vat_list.place(x=0, y=cell_y, width=self._WINDOW_WIDTH, height=self._NOTIF_HEIGHT)
        cell_y += self._NOTIF_HEIGHT

        save_button = tkinter.Button(self._window, text="OK", command=self._ok_click)
        save_button.place(x=GUI_CELL_WIDTH, y=cell_y)

    def _ok_click(self):
        vat_guids = []
        sel_values = [self._vat_list.get(idx) for idx in self._vat_list.curselection()]
        if sel_values is None or len(sel_values) == 0:
            return
        for s in sel_values:
            vat_guid = s[s.find("{") + 1:s.find("}")]
            vat_guids.append(vat_guid)

        payment.record_vat_payment(
            vat_guids=vat_guids,
            paid_amount=self._amount.get_amount(),
            paid_curr=self._amount.get_currency()
        )

        self._window.destroy()

    def _refresh(self):
        self._vat_list.delete(0, tkinter.END)
        vat_count = 0
        for vat in payment.get_open_vat_payments():
            amt, curr = vat.open_amount
            astr = amount.get_formatted_amount(amt)
            self._vat_list.insert(vat_count, vat.description + " " + astr + curr + " {" + vat.guid + "}")
            vat_count += 1
        self._window.update()
