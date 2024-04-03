""" Module to buy foreign currency """
import tkinter
from gui.amount_textbox import AmountTextbox
from gui.font import default_font
from model.payment import payment
from model.bank.bank_account import get_accounts_with_currency
import config


class Invest: # pylint: disable=R0903
    """ Class to buy foreign currency """
    _NOTIF_HEIGHT = 250
    _WINDOW_WIDTH = 800
    _WINDOW_HEIGHT = 400

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

        self._acc_list = tkinter.Listbox(self._window,
                                         selectmode=tkinter.MULTIPLE,
                                         font=default_font())
        self._refresh()
        self._acc_list.place(x=0, y=cell_y, width=self._WINDOW_WIDTH, height=self._NOTIF_HEIGHT)
        cell_y += self._NOTIF_HEIGHT

        save_button = tkinter.Button(self._window,
                                     text="OK",
                                     command=self._ok_click,
                                     font=default_font())
        save_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"], y=cell_y)

    def _ok_click(self):
        sel_values = [self._acc_list.get(idx) for idx in self._acc_list.curselection()]
        if sel_values is None or len(sel_values) == 0:
            return

        payment.record_investment_payment(
            self._amount.amount,
            self._amount.currency,
            "Buy foreign currency from " + sel_values[0])

        self._window.destroy()

    def _refresh(self):
        self._acc_list.delete(0, tkinter.END)
        acc_count = 0
        for acc in get_accounts_with_currency(config.CONSTANTS["HOME_CURRENCY"]):
            acc_str = acc["bank_name"] + " - " + acc["account_name"]
            self._acc_list.insert(acc_count, acc_str)
            acc_count += 1
        self._window.update()
