""" Primary window """

import os
import tkinter
import urllib
from typing import List
from incubus import IncubusFactory
from util import backup, file_system
from util.company_label import CompanyLabel
from util.tax_info import TaxInfo
from gui import activity, activity_list
from gui import asset_list
from gui import (
    cash_movement,
    company_list,
    invoice_list,
    pay_income_tax,
    credit_card_statement,
)
from gui import payment, payment_list, pay_vat, activity_split, invest
from gui.font import default_font, configure_treeview_style
from model import notification
from model.timesheet.activity import Activity
from model.payment.payment import (
    delete_completed_payments,
    get_companies_without_payment,
    create_pyf,
)
from model.payment import payment as payment_model
import config
from update import currency_update
from web.app import startup_url


class Prime:
    """Primary window"""

    _NOTIF_HEIGHT = 500
    _WINDOW_WIDTH = 1600
    _WINDOW_HEIGHT = 600

    def __init__(self, add_activity: bool = False):
        # Initialization
        cell_y = 0

        # Main container
        self._root = tkinter.Tk()
        if config.TEST_MODE:
            self._root.title("Kifu [TEST MODE]")
        else:
            self._root.title("Kifu")
        self._root.geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))

        # Status label
        self._status_label = tkinter.Label(
            master=self._root, text="Welcome to Kifu", font=default_font()
        )
        self._status_label.place(
            x=0,
            y=cell_y,
            width=self._WINDOW_WIDTH,
            height=config.CONSTANTS["GUI_CELL_HEIGHT"],
        )

        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Notifications
        self._notif_list = tkinter.Listbox(self._root, font=default_font())
        self.refresh()
        self._notif_list.place(
            x=0, y=cell_y, width=self._WINDOW_WIDTH, height=self._NOTIF_HEIGHT
        )
        self._notif_list.bind("<Double-1>", self._notif_double_click)
        cell_y += self._NOTIF_HEIGHT

        refresh_button = tkinter.Button(
            self._root, text="Refresh", command=self.refresh, font=default_font()
        )
        refresh_button.place(x=0, y=cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Main menu
        self._menu = tkinter.Menu(self._root, tearoff=0)

        file_menu = tkinter.Menu(self._menu, tearoff=0)
        for data_file in file_system.get_data_file_list():
            file_menu.add_command(
                label=data_file, command=lambda df=data_file: Prime._edit_data_file(df)
            )
        file_menu.add_separator()
        file_menu.add_command(label="Show data files", command=Prime._show_data_files)
        file_menu.add_command(label="Backup data files", command=self._backup_data)
        file_menu.add_command(label="Exit", command=self._root.quit)
        self._menu.add_cascade(menu=file_menu, label="File")

        timesheet_menu = tkinter.Menu(self._menu, tearoff=0)
        timesheet_menu.add_command(label="Add", command=Prime._add_activity)
        timesheet_menu.add_command(label="Edit", command=Prime._list_activity)
        timesheet_menu.add_command(
            label="Split latest", command=Prime._split_latest_activity
        )
        timesheet_menu.add_separator()
        timesheet_menu.add_command(
            label="Activity report", command=Prime._activity_report
        )
        timesheet_menu.add_command(
            label="Workdays without activity", command=Prime._workdays_wo_activity
        )
        timesheet_menu.add_command(
            label="Sanipak activity comparison", command=Prime._ecz_activity
        )
        self._menu.add_cascade(menu=timesheet_menu, label="Timesheet")
        timesheet_menu.add_command(label="Invoices", command=Prime._list_invoice)

        payment_menu = tkinter.Menu(self._menu, tearoff=0)
        payment_menu.add_command(label="Add", command=Prime._add_payment)
        payment_menu.add_command(label="Edit", command=Prime._list_payment)
        payment_menu.add_command(
            label="Delete completed payments", command=self._del_completed_payments
        )
        payment_menu.add_separator()
        payment_menu.add_command(
            label="Book CC statement", command=Prime._add_cc_statement
        )
        payment_menu.add_command(label="Book cash movement", command=Prime._add_cash)
        payment_menu.add_command(label="Invest", command=Prime._invest)
        payment_menu.add_command(label="Pay VAT", command=Prime._pay_vat)
        payment_menu.add_command(label="Pay income tax", command=Prime._pay_tax)
        payment_menu.add_separator()
        payment_menu.add_command(label="Reconciliation", command=Prime._reconciliation)
        payment_menu.add_command(label="Income tax rates", command=Prime._inc_tax_rates)
        payment_menu.add_command(label="IBAN list", command=Prime._iban_list)
        payment_menu.add_command(label="Address book", command=Prime._address_book)
        payment_menu.add_command(label="Tax info", command=Prime._tax_info)
        self._menu.add_cascade(menu=payment_menu, label="Payment")

        asset_menu = tkinter.Menu(self._menu, tearoff=0)
        asset_menu.add_separator()
        asset_menu.add_command(label="Edit assets", command=Prime._edit_assets)
        asset_menu.add_command(
            label="Update commodities", command=Prime._update_commodities
        )
        asset_menu.add_separator()
        asset_menu.add_command(label="Net worth", command=Prime._net_worth)
        asset_menu.add_command(
            label="Account balances", command=Prime._bank_account_balance
        )
        asset_menu.add_command(
            label="Currency balances", command=Prime._currency_account
        )
        asset_menu.add_command(label="Asset profit", command=Prime._asset_profit)
        asset_menu.add_separator()
        self._menu.add_cascade(menu=asset_menu, label="Asset")

        budget_menu = tkinter.Menu(self._menu, tearoff=0)
        budget_menu.add_command(label="Plan", command=Prime._budget_plan)
        budget_menu.add_command(
            label="Salary simulation", command=Prime._salary_simulation
        )
        budget_menu.add_command(
            label="Pay yourself first", command=Prime._pay_yourself_first
        )
        self._menu.add_cascade(menu=budget_menu, label="Budget")

        util_menu = tkinter.Menu(self._menu, tearoff=0)
        util_menu.add_command(label="Update currencies", command=self._currency_update)
        util_menu.add_command(label="Print labels", command=self._print_label)
        util_menu.add_command(
            label="Delete idle companies", command=Prime._del_idle_companies
        )

        self._menu.add_cascade(menu=util_menu, label="Util")

        # Flush
        self._root.configure(menu=self._menu)
        configure_treeview_style()
        if add_activity:
            Prime._add_activity()

        IncubusFactory.get_instance().start(15)

    def start(self):
        """Starts main loop"""
        self._root.mainloop()

    @staticmethod
    def _activity_report():
        IncubusFactory.get_instance().user_event()
        startup_url("activity_list")

    @staticmethod
    def _budget_plan():
        IncubusFactory.get_instance().user_event()
        startup_url("budget_plan")

    @staticmethod
    def _salary_simulation():
        IncubusFactory.get_instance().user_event()
        startup_url("salary_simulation")

    @staticmethod
    def _pay_yourself_first():
        IncubusFactory.get_instance().user_event()
        create_pyf()

    @staticmethod
    def _workdays_wo_activity():
        IncubusFactory.get_instance().user_event()
        startup_url("workdays_wo_activity")

    @staticmethod
    def _add_activity():
        IncubusFactory.get_instance().user_event()
        activity_window = activity.ActivityWindow()
        activity_window.fill_with_last_activity()
        activity_window.mainloop()

    @staticmethod
    def _add_cash():
        IncubusFactory.get_instance().user_event()
        cash_movement.CashMovement()

    @staticmethod
    def _add_cc_statement():
        IncubusFactory.get_instance().user_event()
        credit_card_statement.CreditCardStatement()

    @staticmethod
    def _add_payment():
        IncubusFactory.get_instance().user_event()
        payment_window = payment.PaymentWindow()
        payment_window.fill_with_new_payment()
        payment_window.mainloop()

    @staticmethod
    def _address_book():
        IncubusFactory.get_instance().user_event()
        startup_url("address_book")

    @staticmethod
    def _tax_info():
        IncubusFactory.get_instance().user_event()
        TaxInfo().generate_for_home()

    def _backup_data(self):
        IncubusFactory.get_instance().user_event()
        self._set_status("Backing up")
        backup.execute()
        self._set_status("Backup complete")

    @staticmethod
    def _bank_account_balance():
        IncubusFactory.get_instance().user_event()
        startup_url("bank_account_balances")

    @staticmethod
    def _invest():
        IncubusFactory.get_instance().user_event()
        invest.Invest()

    @staticmethod
    def _currency_account():
        IncubusFactory.get_instance().user_event()
        startup_url("curr_acc_dist")

    @staticmethod
    def _asset_profit():
        IncubusFactory.get_instance().user_event()
        startup_url("asset_profit")

    def _currency_update(self):
        IncubusFactory.get_instance().user_event()
        self._set_status("Updating currencies")
        currency_update.execute()
        self._set_status("Currencies updated")

    def _del_completed_payments(self):
        IncubusFactory.get_instance().user_event()
        self._set_status("Deleting completed payments")
        delete_completed_payments()
        self._set_status("Deletion complete")
        self.refresh()

    @staticmethod
    def _del_idle_companies():
        IncubusFactory.get_instance().user_event()
        idle_companies = get_companies_without_payment()
        if len(idle_companies) <= 0:
            return
        company_list.CompanyList(
            Prime._del_idle_companies__selected, companies=idle_companies
        ).mainloop()

    @staticmethod
    def _del_idle_companies__selected(companies: List):
        IncubusFactory.get_instance().user_event()
        for company in companies:
            company.delete()

    @staticmethod
    def _ecz_activity():
        IncubusFactory.get_instance().user_event()
        startup_url("ecz_activity_comparison")

    @staticmethod
    def _edit_data_file(file_name: str):
        IncubusFactory.get_instance().user_event()
        full_path = os.path.join(config.CONSTANTS["DATA_DIR_PATH"], file_name)
        os.system(f"open {full_path}")

    @staticmethod
    def _inc_tax_rates():
        IncubusFactory.get_instance().user_event()
        startup_url("income_tax_rates")

    @staticmethod
    def _iban_list():
        IncubusFactory.get_instance().user_event()
        startup_url("iban_list")

    @staticmethod
    def _list_activity():
        IncubusFactory.get_instance().user_event()
        list_window = activity_list.ActivityListWindow()
        list_window.mainloop()

    @staticmethod
    def _list_invoice():
        IncubusFactory.get_instance().user_event()
        inv_window = invoice_list.InvoiceListWindow()
        inv_window.mainloop()

    @staticmethod
    def _list_payment():
        IncubusFactory.get_instance().user_event()
        payment_window = payment_list.PaymentListWindow()
        payment_window.mainloop()

    @staticmethod
    def _edit_assets():
        IncubusFactory.get_instance().user_event()
        asset_window = asset_list.AssetListWindow()
        asset_window.mainloop()

    @staticmethod
    def _update_commodities():
        IncubusFactory.get_instance().user_event()
        startup_url("asset_commodity_val")

    @staticmethod
    def _net_worth():
        IncubusFactory.get_instance().user_event()
        startup_url("net_worth")

    def _notif_double_click(self, dummy):  # pylint: disable=W0613
        IncubusFactory.get_instance().user_event()
        selection = self._notif_list.get(self._notif_list.curselection())
        if "Payment" in selection:
            payment_guid = selection[selection.find("{") + 1 : selection.find("}")]
            payment_obj = payment_model.get_payment_with_guid(payment_guid)
            if payment_obj is None:
                return
            payment_win = payment.PaymentWindow()
            payment_win.fill_with_payment(payment_obj)
            payment_win.mainloop()

    @staticmethod
    def _pay_tax():
        IncubusFactory.get_instance().user_event()
        pay_income_tax.PayIncomeTax()

    @staticmethod
    def _pay_vat():
        IncubusFactory.get_instance().user_event()
        pay_vat.PayVat()

    @staticmethod
    def _print_label():
        IncubusFactory.get_instance().user_event()
        company_list.CompanyList(Prime._print_label__company_selected).mainloop()

    @staticmethod
    def _print_label__company_selected(companies: List):
        IncubusFactory.get_instance().user_event()
        CompanyLabel().generate(companies)

    @staticmethod
    def _reconciliation():
        IncubusFactory.get_instance().user_event()
        company_list.CompanyList(Prime._reconciliation__company_selected).mainloop()

    @staticmethod
    def _reconciliation__company_selected(companies: List):
        IncubusFactory.get_instance().user_event()
        names = ""
        for selco in companies:
            if names != "":
                names += ","
            names += selco.name

        startup_url(
            "reconciliation", query_string="names=" + urllib.parse.quote(names, safe="")
        )

    def refresh(self):
        """Refreshes notifications"""
        IncubusFactory.get_instance().user_event()
        self._notif_list.delete(0, tkinter.END)
        notif_count = 0
        for ntf in notification.get_notifications():
            self._notif_list.insert(notif_count, ntf)
            notif_count += 1
        self._root.update()

    def _set_status(self, status: str):
        IncubusFactory.get_instance().user_event()
        self._status_label["text"] = status
        self._root.update()

    @staticmethod
    def _show_data_files():
        IncubusFactory.get_instance().user_event()
        os.system(f"open {config.CONSTANTS['DATA_DIR_PATH']}")

    @staticmethod
    def _split_latest_activity():
        IncubusFactory.get_instance().user_event()
        last_activity = Activity(Activity.get_last_activity())

        as_window = activity_split.ActivitySplit()
        as_window.fill_with_activity(last_activity)
        as_window.mainloop()
