""" VAT payment window """
import tkinter
from gui.amount_textbox import AmountTextbox
from gui.prime_singleton import PrimeSingleton
from gui.font import default_font
from model.payment import payment
from model.bank.bank_account import add_amount_to_vat_account
from util import amount
import config

class PayVat:
    """ VAT payment window """
    _NOTIF_HEIGHT = 250
    _WINDOW_WIDTH = 825
    _WINDOW_HEIGHT = 350

    def __init__(self):
        self._window = tkinter.Toplevel()
        self._window.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))
        cell_y = 0

        self._amount = AmountTextbox(
            self._window,
            "Amount",
            0,
            config.CONSTANTS["HOME_CURRENCY"],
            0,
            cell_y)

        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._vat_list = tkinter.Listbox(self._window,
                                         selectmode=tkinter.MULTIPLE,
                                         font=default_font())
        self._refresh()
        self._vat_list.place(x=0, y=cell_y, width=self._WINDOW_WIDTH, height=self._NOTIF_HEIGHT)
        cell_y += self._NOTIF_HEIGHT

        save_button = tkinter.Button(self._window,
                                     text="OK",
                                     command=self._ok_click,
                                     font=default_font())
        save_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"], y=cell_y)

    def _ok_click(self):
        vat_guids = []
        sel_values = [self._vat_list.get(idx) for idx in self._vat_list.curselection()]
        if sel_values is None or len(sel_values) == 0:
            return
        for sel_value in sel_values:
            vat_guid = sel_value[sel_value.find("{") + 1:sel_value.find("}")]
            vat_guids.append(vat_guid)

        payment.record_vat_payment(
            vat_guids=vat_guids,
            paid_amount=self._amount.amount,
            paid_curr=self._amount.currency
        )

        add_amount_to_vat_account(self._amount.amount * -1, self._amount.currency)

        PrimeSingleton.get().refresh()
        self._window.destroy()

    def _refresh(self):
        self._vat_list.delete(0, tkinter.END)
        vat_count = 0
        for vat in payment.get_open_vat_payments():
            amt, curr = vat.open_amount
            astr = amount.get_formatted_amount(amt)
            self._vat_list.insert(
                vat_count,
                vat.description + " " + astr + curr + " {" + vat.guid + "}")
            vat_count += 1
        self._window.update()
