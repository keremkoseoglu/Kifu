""" Payment window """
import datetime
import urllib
import tkinter
import tkinter.ttk
from gui.amount_textbox import AmountTextbox
from gui.collection import Collection
from gui.company_combobox import CompanyCombobox
from gui.labeled_checkbox import LabeledCheckbox
from gui.labeled_combobox import LabeledCombobox
from gui.labeled_textarea import LabeledTextarea
from gui.labeled_textbox import LabeledTextbox
from gui.popup_with_single_value import PopupWithSingleValue
from gui.prime_singleton import PrimeSingleton
import model.payment as payment_model
from util import amount as util_amount
from util import date_time
import config
from web.app import startup_url


class PaymentWindow(tkinter.Toplevel):
    """ Payment window """

    _SPACING = 100
    _WINDOW_WIDTH = 1000
    _WINDOW_HEIGHT = 950

    def __init__(self):

        # Initialization
        tkinter.Toplevel.__init__(self)
        self.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))
        cell_x = 0
        cell_y = 0
        self._payment = None

        ##########
        # Payment
        ##########

        # GUID
        self._guid = LabeledTextbox(self, "GUID", "", cell_x, cell_y)
        self._guid.disable()
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Creation date
        self._creation_date = LabeledTextbox(self, "Creation", "", cell_x, cell_y)
        self._creation_date.disable()
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Company
        self._company_combo = CompanyCombobox(self, "Company", cell_x, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Description
        self._description = LabeledTextbox(self, "Description", "", cell_x, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Invoice GUID
        self._invoice_guid = LabeledTextbox(self, "Invoice GUID", "", cell_x, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Direction
        self._direction = LabeledCombobox(
            self,
            "Direction",
            payment_model.get_direction_values(),
            cell_x,
            cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Amount

        self._amount = AmountTextbox(
            self,
            "Amount",
            0,
            config.CONSTANTS["HOME_CURRENCY"],
            cell_x,
            cell_y)

        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Open amount

        self._open_amount = AmountTextbox(
            self,
            "Open Amount",
            0,
            config.CONSTANTS["HOME_CURRENCY"],
            cell_x,
            cell_y)

        self._open_amount.disable()
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Cleared

        self._cleared = LabeledCheckbox(self, "Cleared", cell_x, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Tax

        self._is_vat = LabeledCheckbox(self, "Is VAT", cell_x, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._is_income_tax = LabeledCheckbox(self, "Is Income Tax", cell_x, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]
        cell_y_bookmark = cell_y

        ##########
        # Scheme
        ##########

        cell_x = (config.CONSTANTS["GUI_CELL_WIDTH"] * 2) + self._SPACING
        cell_y = 0

        # Frequency
        self._frequency = LabeledTextbox(self, "Frequency", "", cell_x, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Period
        self._period = LabeledCombobox(
            self,
            "Period",
            payment_model.get_period_values(),
            cell_x,
            cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Start
        self._start = LabeledTextbox(self, "Start", "", cell_x, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Repeat
        self._repeat = LabeledTextbox(self, "Repeat", "", cell_x, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Notes
        self._notes = LabeledTextarea(self, "Notes", "", cell_x, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        ##########
        # Recurrence
        ##########

        cell_x = 0
        cell_y = cell_y_bookmark + config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Visual

        tkinter.Label(
            self,
            text="Recurrence:").place(x=cell_x, y=cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._recurrence_tree = tkinter.ttk.Treeview(self)
        tree_height = config.CONSTANTS["GUI_CELL_HEIGHT"] * 5
        self._recurrence_tree.place(
            x=cell_x,
            y=cell_y,
            width=self._WINDOW_WIDTH,
            height=tree_height)
        cell_y += tree_height

        self._recurrence_tree["columns"] = ("Exp.Date", "Amount", "Open Amount", "Cleared")
        self._recurrence_tree.heading("Exp.Date", text="Exp.Date")
        self._recurrence_tree.heading("Amount", text="Amount")
        self._recurrence_tree.heading("Open Amount", text="Open Amount")
        self._recurrence_tree.heading("Cleared", text="Cleared")
        self._recurrence_tree.bind("<<TreeviewSelect>>", self._recurrence_select)
        self._recurrence_tree.bind("<Double-1>", self._recurrence_double_click)

        recurrence_clear_button = tkinter.Button(self, text="Clear", command=self._clear_recurrence)
        recurrence_clear_button.place(x=0, y=cell_y)

        recurrence_postpone_button = tkinter.Button(
            self,
            text="Postpone",
            command=self._rec_postpone_popup)
        recurrence_postpone_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"], y=cell_y)
        recurrence_add_button = tkinter.Button(self, text="Add", command=self._recurrence_popup)
        recurrence_add_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"]*2, y=cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Data
        self._recurrence_tree_content = {}

        ##########
        # Collections
        ##########

        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]
        tkinter.Label(self, text="Collections:").place(x=cell_x, y=cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._collection_tree = tkinter.ttk.Treeview(self)
        self._collection_tree.place(
            x=cell_x,
            y=cell_y,
            width=self._WINDOW_WIDTH,
            height=tree_height)
        cell_y += tree_height

        self._collection_tree["columns"] = ("Description", "Amount")
        self._collection_tree.heading("Description", text="Description")
        self._collection_tree.heading("Amount", text="Amount")

        add_collection_button = tkinter.Button(self, text="Add", command=self._collection_popup)
        add_collection_button.place(x=0, y=cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Data
        self._collection_tree_content = {}

        ##########
        # Final
        ##########

        cell_y += (self._SPACING / 2)

        status_button = tkinter.Button(self, text="Status", command=self._status)
        status_button.place(x=0, y=cell_y)

        recon_button = tkinter.Button(self, text="Reconciliation", command=self._reconciliation)
        recon_button.place(x=50, y=cell_y)

        save_button = tkinter.Button(self, text="Save", command=self._save)
        save_button.place(x=200, y=cell_y)

        del_button = tkinter.Button(self, text="Delete", command=self._delete)
        del_button.place(x=300, y=cell_y)
        self._delete_warning_label = tkinter.Label(self, text="!")
        self._delete_warning_label.place(x=350, y=cell_y)

        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

    def add_collection(self, collection: payment_model.Collection, clear=False):
        """ Adds a new payment collection """
        rec = self._get_selected_recurrence()
        if rec is None:
            return

        rec.add_collection(collection)
        if clear:
            rec.cleared = True
        self._paint_recurrences()
        self._clear_collection_tree()

    def add_recurrence(self, date: str):
        """ Adds a new payment recurrence """
        amount, currency = self._payment.amount

        recurrence_json = {
            "recurrence_date": date,
            "expected_payment_date": date,
            "amount": amount,
            "currency": currency,
            "cleared": False,
            "collections": []
        }

        recurrence_obj = payment_model.Recurrence(recurrence_json)
        self._payment.scheme.add_recurrence(recurrence_obj)
        self._paint_recurrences()

    def fill_with_new_payment(self):
        """ Fills the form with a new payment """
        payment_json = {
            "creation_date": datetime.datetime.now().isoformat(),
            "scheme": {
                "frequency": 1,
                "period": "D",
                "repeat": 1,
                "recurrence": []
            }
        }

        new_payment = payment_model.Payment(payment_json)
        self.fill_with_payment(new_payment)

    def fill_with_payment(self, pay: payment_model.Payment):
        """ Fills the form with the given payment """

        # Preparation

        self._payment = pay
        amount, currency = self._payment.amount
        open_amount, open_currency = self._payment.open_amount

        # Payment

        self._guid.value = self._payment.guid
        self._creation_date.value = self._payment.creation_date.isoformat()
        self._company_combo.company_name = self._payment.company.name
        self._description.value = self._payment.description
        self._notes.value = self._payment.notes
        self._invoice_guid.value = self._payment.invoice_guid
        self._direction.selected_value = self._payment.direction
        self._amount.set_value(amount, currency)
        self._open_amount.set_value(open_amount, open_currency)
        self._cleared.checked = self._payment.cleared
        self._is_vat.checked = self._payment.is_vat
        self._is_income_tax.checked = self._payment.is_income_tax

        # Scheme

        scheme = self._payment.scheme
        frequency, period = scheme.frequency
        repeat = scheme.repeat
        self._frequency.value = frequency
        self._period.selected_value = period
        self._start.value = scheme.start_date
        self._repeat.value = str(repeat)

        # Recurrences
        self._paint_recurrences()

        # warning label
        del_warning_text = "!"
        if repeat > 1:
            del_warning_text = "!RECURRING"
        self._delete_warning_label["text"] = del_warning_text

    def postpone_recurrence(self, date_txt: str):
        """ Click handler for postpone """
        rec = self._get_selected_recurrence()
        rec.expected_payment_date = date_time.parse_json_date(date_txt)
        self._paint_recurrences()

    def _clear_collection_tree(self):
        self._collection_tree_content = {}
        self._collection_tree.delete(*self._collection_tree.get_children())
        self.update()

    def _clear_recurrence(self):
        selected_recurrence = self._get_selected_recurrence()
        if selected_recurrence is not None:
            selected_recurrence.toggle_cleared()

        self._paint_recurrences()

    def _collection_popup(self):
        Collection(self.add_collection, self._payment.currency)

    def _get_selected_recurrence(self) -> payment_model.Recurrence:
        try:
            item = self._recurrence_tree.selection()[0]
        except Exception:
            return None
        clicked_date_txt = self._recurrence_tree.item(item, "text")
        clicked_year = int(clicked_date_txt[:4])
        clicked_month = int(clicked_date_txt[5:7])
        clicked_day = int(clicked_date_txt[8:10])

        clicked_recurrence = self._payment.scheme.get_recurrence_on_date(
            clicked_year,
            clicked_month,
            clicked_day)

        return clicked_recurrence

    def _delete(self):
        payment_model.delete_payments([self._payment.guid])
        PrimeSingleton.get().refresh()
        self.destroy()

    def _paint_recurrences(self):
        self._recurrence_tree_content = {}
        self._recurrence_tree.delete(*self._recurrence_tree.get_children())
        self.update()

        recurrences = self._payment.scheme.recurrences

        for recurrence in recurrences:
            amount, currency = recurrence.amount
            open_amount, open_currency = recurrence.open_amount
            tree_val = (
                date_time.get_formatted_date(recurrence.expected_payment_date),
                util_amount.get_formatted_amount(amount) + currency,
                util_amount.get_formatted_amount(open_amount) + open_currency,
                str(recurrence.cleared)
            )

            id_in_tree = self._recurrence_tree.insert(
                '',
                'end',
                text=date_time.get_formatted_date(recurrence.recurrence_date),
                value=tree_val
            )
            self._recurrence_tree_content[id_in_tree] = recurrence

        self.update()

    def _recurrence_double_click(self, event):
        pass

    def _recurrence_popup(self):
        PopupWithSingleValue(self.add_recurrence, "Date", datetime.datetime.now().isoformat())

    def _rec_postpone_popup(self):
        rec = self._get_selected_recurrence()
        PopupWithSingleValue(self.postpone_recurrence, "Date", rec.expected_payment_date)

    def _recurrence_select(self, dummy): # pylint: disable=W0613
        # Prepare
        self._clear_collection_tree()

        # Get clicked recurrence payments
        clicked_recurrence = self._get_selected_recurrence()
        if clicked_recurrence is None:
            return

        collections = clicked_recurrence.collections

        # Paint
        for collection in collections:
            amount, currency = collection.amount
            tree_val = (
                collection.description,
                util_amount.get_formatted_amount(amount) + currency
            )

            id_in_tree = self._collection_tree.insert(
                '',
                'end',
                text=date_time.get_formatted_date(collection.date),
                value=tree_val
            )
            self._collection_tree_content[id_in_tree] = collection

        self.update()

    def _save(self):
        self._payment.company = self._company_combo.company_name
        self._payment.description = self._description.value
        self._payment.notes = self._notes.value
        self._payment.invoice_guid = self._invoice_guid.value
        self._payment.direction = self._direction.selected_value
        self._payment.set_amount(self._amount.amount, self._amount.currency)
        self._payment.cleared = self._cleared.checked
        self._payment.is_vat = self._is_vat.checked
        self._payment.is_income_tax = self._is_income_tax.checked

        scheme = self._payment.scheme
        scheme.set_frequency(int(self._frequency.value), self._period.selected_value)
        scheme.set_start_date_from_iso(self._start.value)
        scheme.repeat = int(self._repeat.value)

        self._payment.save()
        PrimeSingleton.get().refresh()
        self.destroy()

    def _status(self):
        startup_url("payment_status", query_string=f"guid={self._payment.guid}")

    def _reconciliation(self):
        query = "names="+urllib.parse.quote(self._payment.company.name, safe='')
        startup_url("reconciliation", query_string=query)
