""" Payment list window """
import urllib
import tkinter
import tkinter.ttk
from typing import List
from model import payment
from util import backup, date_time
from util import amount as util_amount
from gui.payment import PaymentWindow
from gui.prime_singleton import PrimeSingleton
import config
from web.app import startup_url


class PaymentListWindow(tkinter.Toplevel):
    """ Payment list window """

    _BUTTON_WIDTH = 150
    _WINDOW_WIDTH = 1200
    _WINDOW_HEIGHT = 400
    _Y_SPACING = 10

    def __init__(self):
        # Initialization
        tkinter.Toplevel.__init__(self)
        self.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))

        # Build tree
        self._tree = tkinter.ttk.Treeview(self)
        tree_height = self._WINDOW_HEIGHT - config.CONSTANTS["GUI_CELL_HEIGHT"] - self._Y_SPACING
        self._tree.place(x=0, y=0, width=self._WINDOW_WIDTH, height=tree_height)
        cell_y = tree_height + self._Y_SPACING

        self._tree["columns"] = ("Company", "Amount", "Open Amount", "Direction", "Description")
        self._tree.column("Amount", anchor="e")
        self._tree.column("Open Amount", anchor="e")
        self._tree.heading("Company", text="Company")
        self._tree.heading("Amount", text="Amount")
        self._tree.heading("Open Amount", text="Open Amount")
        self._tree.heading("Direction", text="Direction")
        self._tree.heading("Description", text="Description")

        # Fill tree with data
        self._payments = []
        self._tree_content = {}
        self._fill_tree_with_payments()

        # Buttons
        cell_x = 0

        refresh_button = tkinter.Button(self, text="Refresh", command=self._refresh_click)
        refresh_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        edit_button = tkinter.Button(self, text="Edit", command=self._edit_click)
        edit_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        edit_button = tkinter.Button(self, text="Status", command=self._status_rep_click)
        edit_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        edit_button = tkinter.Button(self, text="Reconciliation", command=self._recon_rep_click)
        edit_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        invoice_button = tkinter.Button(self, text="Delete", command=self._delete_click)
        invoice_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

    def _delete_click(self):
        deletable_payments = self._get_selected_payments()
        if len(deletable_payments) == 0:
            return

        deletable_guids = []
        for pay in deletable_payments:
            deletable_guids.append(pay.guid)

        backup.execute()
        payment.delete_payments(deletable_guids)

        self._fill_tree_with_payments()
        PrimeSingleton.get().refresh()

    def _edit_click(self):
        selected_payments = self._get_selected_payments()
        if len(selected_payments) == 0:
            return

        first_selected_payment = selected_payments[0]

        payment_window = PaymentWindow()
        payment_window.fill_with_payment(first_selected_payment)
        payment_window.mainloop()

    def _fill_tree_with_payments(self):
        self._payments = payment.get_payments()
        self._tree_content = {}

        self._tree.delete(*self._tree.get_children())

        sorted_payments = self._payments["payments"]
        sorted_payments.sort(key=lambda x: payment.Payment(x).scheme.next_significant_date)

        for payment_line in sorted_payments:
            payment_obj = payment.Payment(payment_line)
            amount, currency = payment_obj.amount
            open_amount, open_currency = payment_obj.open_amount

            tree_val = (
                payment_obj.company.name,
                util_amount.get_formatted_amount(amount) + " " + currency,
                util_amount.get_formatted_amount(open_amount) + " " + open_currency,
                payment_obj.direction,
                payment_obj.description
            )

            tree_txt_date = payment_obj.scheme.next_significant_date
            id_in_tree = self._tree.insert(
                '',
                'end',
                text=date_time.get_formatted_date(tree_txt_date),
                value=tree_val
            )
            self._tree_content[id_in_tree] = payment_obj

        self.update()

    def _get_selected_payments(self) -> List:
        selected_payments = []

        for selected_id in self._tree.selection():
            selected_payment = self._tree_content[selected_id]
            selected_payments.append(selected_payment)

        return selected_payments

    def _recon_rep_click(self):
        selected_payments = self._get_selected_payments()
        if len(selected_payments) == 0:
            return

        selected_companies = []
        for sel_pay in selected_payments:
            already_appended = False
            for sel_comp in selected_companies:
                if sel_pay.company.name == sel_comp.name:
                    already_appended = True
                    break
            if not already_appended:
                selected_companies.append(sel_pay.company)

        names = ""
        for selco in selected_companies:
            if names != "":
                names += ","
            names += selco.name

        startup_url("reconciliation", query_string="names="+urllib.parse.quote(names, safe=''))

    def _refresh_click(self):
        self._fill_tree_with_payments()

    def _status_rep_click(self):
        selected_payments = self._get_selected_payments()
        if len(selected_payments) == 0:
            return

        first_selected_payment = selected_payments[0]
        startup_url("payment_status", query_string=f"guid={first_selected_payment.guid}")
