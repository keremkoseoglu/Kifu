""" Invoice window """
import tkinter
import webbrowser
import subprocess
from gui.amount_textbox import AmountTextbox
from gui.company_combobox import CompanyCombobox
from gui.labeled_textbox import LabeledTextbox
from gui.popup_file import popup_email, popup_open_file
from model.invoice import Invoice
import model.company
from model.company import Company
from model import payment
from report.address_book import AddressBook
from util.file_system import open_file
import config


def open_invoice_as_email(inv: Invoice):
    """ Opens E-Mail windows to send the invoice """
    recipients = []
    if inv.payer.email != "":
        recipients.append(inv.payer.email)
    accounting_company = Company(config.CONSTANTS["COMPANY_NAME_ACCOUNTING"])
    if accounting_company.email != "":
        recipients.append(accounting_company.email)

    popup_email(recipients=recipients,
                subject="Fatura " + inv.serial,
                attachment=inv.file_path)


class InvoiceWindow(tkinter.Toplevel):
    """ Invoice window """

    _SMALL_SPACE = 25
    _SPACE = 50
    _WINDOW_WIDTH = 400
    _WINDOW_HEIGHT = 425

    def __init__(self):

        # Initialization
        tkinter.Toplevel.__init__(self)
        self.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))
        cell_y = 0

        # GUID
        self._guid = LabeledTextbox(self, "GUID", "", 0, cell_y)
        self._guid.disable()
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Serial
        self._serial = LabeledTextbox(self, "Serial", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Payer
        self._payer_combo = CompanyCombobox(self, "Payer", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Invoice date
        self._invoice_date = LabeledTextbox(self, "Invoice date", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Due date
        self._due_date = LabeledTextbox(self, "Due date", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Amount
        self._amount = AmountTextbox(
            self,
            "Amount",
            0,
            config.CONSTANTS["HOME_CURRENCY"],
            0,
            cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # VAT
        self._vat = LabeledTextbox(self, "VAT %", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # VAT amount
        self._vat_amount = LabeledTextbox(self, "VAT amount", "", 0, cell_y)
        self._vat_amount.disable()
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Total amount
        self._total_amount = LabeledTextbox(self, "Total amount", "", 0, cell_y)
        self._total_amount.disable()
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Income tax rate
        self._income_tax = LabeledTextbox(self, "Inc.Tax %", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Income tax amount
        self._income_tax_amount = LabeledTextbox(self, "Inc.Tax amount", "", 0, cell_y)
        self._income_tax_amount.disable()
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # File Path
        self._file_path = LabeledTextbox(self, "File path", "", 0, cell_y)

        cell_x = (config.CONSTANTS["GUI_CELL_WIDTH"] * 2) + InvoiceWindow._SPACE
        file_path_button = tkinter.Button(self, text="...", command=self._file_path_click)
        file_path_button.place(x=cell_x, y=cell_y)

        cell_x += InvoiceWindow._SMALL_SPACE
        file_open_button = tkinter.Button(self, text="!", command=self._file_open_click)
        file_open_button.place(x=cell_x, y=cell_y)

        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Button
        save_button = tkinter.Button(self, text="Save", command=self._save_click)
        save_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"], y=cell_y)
        save2_button = tkinter.Button(self, text="Save with payments", command=self._save_pay_click)
        save2_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"] + InvoiceWindow._SPACE, y=cell_y)

        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Status
        self._status_label = tkinter.Label(master=self, text="")
        self._status_label.place(
            x=0,
            y=cell_y,
            width=self._WINDOW_WIDTH,
            height=config.CONSTANTS["GUI_CELL_HEIGHT"])

    def fill_with_invoice(self,
                          invoice: model.invoice.Invoice,
                          browser: bool = False,
                          invoice_dir: bool = False):
        """ Fills the window with the given invoice
        If browser == True, also opens a new browser window & address book.
        This functionality is typically used when creating a new invoice.
        """
        self._guid.value = invoice.guid
        self._serial.value = invoice.serial
        self._invoice_date.value = str(invoice.invoice_date)
        self._due_date.value = str(invoice.due_date)
        self._amount.set_value(invoice.amount, invoice.currency)
        self._payer_combo.company_name = invoice.payer.name
        self._vat.value = str(invoice.vat_rate)
        self._vat_amount.value = str(invoice.vat_amount)
        self._total_amount.value = str(invoice.amount_plus_vat)
        self._income_tax.value = str(invoice.income_tax_rate)
        self._income_tax_amount.value = str(invoice.income_tax_amount)
        self._file_path.value = invoice.file_path

        if browser:
            AddressBook(listable_companies=[invoice.payer.name]).execute()
            webbrowser.open(config.CONSTANTS["E_ARCHIVE_URL"])

        if invoice_dir and "INVOICE_FILE_PATH" in config.CONSTANTS:
            subprocess.call(["open", "-R", config.CONSTANTS["INVOICE_FILE_PATH"]])

    def _file_open_click(self):
        open_file(self._file_path.value)

    def _file_path_click(self):
        path = popup_open_file()
        if path is None or path == "":
            return
        self._file_path.value = path

    def _get_invoice_dict_from_gui(self) -> {}:
        return {
            "guid": self._guid.value,
            "serial": self._serial.value,
            "payer": self._payer_combo.company_name,
            "invoice_date": self._invoice_date.value,
            "due_date": self._due_date.value,
            "amount": self._amount.amount,
            "currency": self._amount.currency,
            "vat_rate": float(self._vat.value),
            "income_tax_rate": float(self._income_tax.value),
            "file_path": self._file_path.value
        }

    def _save_click(self):
        invoice_dict = self._get_invoice_dict_from_gui()
        model.invoice.Invoice(invoice_dict).save()
        self._saved()

    def _save_pay_click(self):
        invoice_dict = self._get_invoice_dict_from_gui()
        invoice_obj = model.invoice.Invoice(invoice_dict)
        invoice_obj.save()

        new_payments = payment.get_payment_objects_from_invoice(invoice_obj)
        for new_payment in new_payments:
            new_payment.save()

        self._saved()

    def _saved(self):
        self._set_status("Saved!")
        self.after(1, self.destroy())

    def _set_status(self, status: str):
        self._status_label["text"] = status
        self.update()
