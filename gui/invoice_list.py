""" Invoice list window """
import tkinter.ttk
from typing import List
from util import amount, backup, date_time, invoice_label
from gui.payment_list import PaymentListWindow
from gui.invoice import InvoiceWindow, open_invoice_as_email
from gui.prime_singleton import PrimeSingleton
from gui.font import default_font
from model.timesheet.invoice import Invoice
from model.timesheet.invoice_file_reader import get_invoices
from model.payment import payment
import config

class InvoiceListWindow(tkinter.Toplevel):
    """ Invoice list window """

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

        self._tree["columns"] = ("Payer", "Amount", "Serial", "GUID")
        self._tree.heading("Payer", text="Payer")
        self._tree.heading("Amount", text="Amount")
        self._tree.column("Amount", anchor="e")
        self._tree.heading("Serial", text="Serial")
        self._tree.heading("GUID", text="GUID")

        # Fill tree with data
        self._invoices = []
        self._tree_content = {}
        self._fill_tree_with_invoices()

        # Buttons
        cell_x = 0

        edit_button = tkinter.Button(self,
                                     text="Edit",
                                     command=self._edit_click,
                                     font=default_font())
        edit_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        invoice_button = tkinter.Button(self,
                                        text="Create payments",
                                        command=self._payment_click,
                                        font=default_font())
        invoice_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH * 2

        email_button = tkinter.Button(self,
                                      text="E-Mail",
                                      command=self._email_click,
                                      font=default_font())
        email_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        label_button = tkinter.Button(self,
                                      text="Labels",
                                      command=self._label_click,
                                      font=default_font())
        label_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        invoice_button = tkinter.Button(self,
                                        text="Delete",
                                        command=self._delete_click,
                                        font=default_font())
        invoice_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

    @property
    def _selected_invoices(self) -> List:
        selected_invoices = []

        for selected_id in self._tree.selection():
            selected_invoice = self._tree_content[selected_id]
            selected_invoices.append(selected_invoice)

        return selected_invoices

    def _delete_click(self):
        deletable_invoices = self._selected_invoices
        if len(deletable_invoices) == 0:
            return

        deletable_guids = []
        for inv in deletable_invoices:
            deletable_guids.append(inv.guid)

        backup.execute()
        Invoice.delete_invoices(deletable_guids)

        self._fill_tree_with_invoices()
        PrimeSingleton.get().refresh()

    def _edit_click(self):
        selected_invoices = self._selected_invoices
        if len(selected_invoices) == 0:
            return

        first_selected_invoice = selected_invoices[0]

        invoice_window = InvoiceWindow()
        invoice_window.fill_with_invoice(first_selected_invoice, browser=False)
        self.after(1, self.destroy())
        invoice_window.mainloop()

    def _email_click(self):
        selected_invoices = self._selected_invoices
        if len(selected_invoices) == 0:
            return
        open_invoice_as_email(selected_invoices[0])

    def _fill_tree_with_invoices(self):
        self._invoices = get_invoices()
        self._invoices["invoices"].sort(key=lambda x: x["invoice_date"], reverse=True)
        self._tree_content = {}

        self._tree.delete(*self._tree.get_children())

        for invoice_line in self._invoices["invoices"]:
            invoice_obj = Invoice(invoice_line)
            tree_val = (
                invoice_obj.payer.name,
                amount.get_formatted_amount(invoice_obj.amount) + " " + invoice_obj.currency,
                invoice_obj.serial,
                invoice_obj.guid
            )

            id_in_tree = self._tree.insert(
                '',
                'end',
                text=date_time.get_formatted_date(invoice_obj.invoice_date),
                value=tree_val
            )
            self._tree_content[id_in_tree] = invoice_obj

        self.update()

    def _label_click(self):
        invoice_label.InvoiceLabel.generate(self._selected_invoices)

    def _payment_click(self):
        selected_invoices = self._selected_invoices

        for selected_invoice in selected_invoices:
            new_payments = payment.get_payment_objects_from_invoice(selected_invoice)
            for new_payment in new_payments:
                new_payment.save()

        payment_list_window = PaymentListWindow()
        payment_list_window.mainloop()
