""" Primary window """
import os
import tkinter
from incubus import IncubusFactory
from util import backup, currency_update, file_system
from util.company_label import CompanyLabel
from gui import activity, activity_list
from gui import cash_movement, company_list, invoice_list, pay_income_tax
from gui import payment, payment_list, pay_vat, activity_split, buy_foreign_currency
from model import notification, payment as payment_model
from model.activity import Activity
from model.payment import delete_completed_payments, get_companies_without_payment
from report import \
    activity_list as activity_list_report, \
    bank_account_balance, \
    curr_acc_dist, \
    iban_list, \
    net_worth, \
    ecz_activity_comparison, \
    reconciliation, \
    address_book, \
    workdays_wo_activity
import config


class Prime:
    """ Primary window """
    _NOTIF_HEIGHT = 250
    _WINDOW_WIDTH = 800
    _WINDOW_HEIGHT = 350

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
        self._status_label = tkinter.Label(master=self._root, text="Welcome to Kifu")
        self._status_label.place(
            x=0,
            y=cell_y,
            width=self._WINDOW_WIDTH,
            height=config.CONSTANTS["GUI_CELL_HEIGHT"])

        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Notifications
        self._notif_list = tkinter.Listbox(self._root)
        self.refresh()
        self._notif_list.place(x=0, y=cell_y, width=self._WINDOW_WIDTH, height=self._NOTIF_HEIGHT)
        self._notif_list.bind('<Double-1>', self._notif_double_click)
        cell_y += self._NOTIF_HEIGHT

        refresh_button = tkinter.Button(self._root, text="Refresh", command=self.refresh)
        refresh_button.place(x=0, y=cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Main menu
        self._menu = tkinter.Menu(self._root, tearoff=0)

        file_menu = tkinter.Menu(self._menu, tearoff=0)
        for data_file in file_system.get_data_file_list():
            file_menu.add_command(
                label=data_file,
                command=lambda df=data_file: Prime._edit_data_file(df))
        file_menu.add_separator()
        file_menu.add_command(label="Show data files", command=Prime._show_data_files)
        file_menu.add_command(label="Backup data files", command=self._backup_data)
        file_menu.add_command(label="Exit", command=self._root.quit)
        self._menu.add_cascade(menu=file_menu, label="File")

        timesheet_menu = tkinter.Menu(self._menu, tearoff=0)
        timesheet_menu.add_command(label="Add activity", command=Prime._add_activity)
        timesheet_menu.add_command(label="Edit activities", command=Prime._list_activity)
        timesheet_menu.add_command(label="Split latest", command=Prime._split_latest_activity)
        timesheet_menu.add_separator()
        timesheet_menu.add_command(label="List invoices", command=Prime._list_invoice)

        self._menu.add_cascade(menu=timesheet_menu, label="Timesheet")

        payment_menu = tkinter.Menu(self._menu, tearoff=0)
        payment_menu.add_command(label="Add payment", command=Prime._add_payment)
        payment_menu.add_command(label="Book cash movement", command=Prime._add_cash)
        payment_menu.add_command(label="Buy foreign currency", command=Prime._buy_curr)
        payment_menu.add_command(label="Pay VAT", command=Prime._pay_vat)
        payment_menu.add_command(label="Pay income tax", command=Prime._pay_tax)
        payment_menu.add_separator()
        payment_menu.add_command(label="List payments", command=Prime._list_payment)
        payment_menu.add_separator()
        payment_menu.add_command(
            label="Delete completed payments",
            command=self._del_completed_payments)
        self._menu.add_cascade(menu=payment_menu, label="Payment")

        report_menu = tkinter.Menu(self._menu, tearoff=0)
        report_menu.add_command(label="Activity report", command=Prime._activity_report)
        report_menu.add_command(
            label="Workdays without activity",
            command=Prime._workdays_wo_activity)
        report_menu.add_command(label="Ecz activity comparison", command=Prime._ecz_activity)
        report_menu.add_command(label="Reconciliation", command=Prime._reconciliation)
        report_menu.add_separator()
        report_menu.add_command(label="Net worth", command=Prime._net_worth)
        report_menu.add_command(label="Account balances", command=Prime._bank_account_balance)
        report_menu.add_command(label="Currency balances", command=Prime._currency_account)
        report_menu.add_separator()
        report_menu.add_command(label="IBAN list", command=Prime._iban_list)
        report_menu.add_command(label="Address book", command=Prime._address_book)
        self._menu.add_cascade(menu=report_menu, label="Report")

        util_menu = tkinter.Menu(self._menu, tearoff=0)
        util_menu.add_command(label="Update currencies", command=self._currency_update)
        util_menu.add_command(label="Print labels", command=self._print_label)
        util_menu.add_command(label="Delete idle companies", command=Prime._del_idle_companies)

        self._menu.add_cascade(menu=util_menu, label="Util")

        # Flush
        self._root.configure(menu=self._menu)
        if add_activity:
            Prime._add_activity()

        IncubusFactory.get_instance().start(5)

    def start(self):
        """ Starts main loop """
        self._root.mainloop()

    @staticmethod
    def _activity_report():
        IncubusFactory.get_instance().user_event()
        activity_list_report.ActivityList().execute()

    @staticmethod
    def _workdays_wo_activity():
        IncubusFactory.get_instance().user_event()
        workdays_wo_activity.WorkdaysWithoutActivityReport().execute()

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
    def _add_payment():
        IncubusFactory.get_instance().user_event()
        payment_window = payment.PaymentWindow()
        payment_window.fill_with_new_payment()
        payment_window.mainloop()

    @staticmethod
    def _address_book():
        IncubusFactory.get_instance().user_event()
        address_book.AddressBook().execute()

    def _backup_data(self):
        IncubusFactory.get_instance().user_event()
        self._set_status("Backing up")
        backup.execute()
        self._set_status("Backup complete")

    @staticmethod
    def _bank_account_balance():
        IncubusFactory.get_instance().user_event()
        bank_account_balance.BankAccountBalance().execute()

    @staticmethod
    def _buy_curr():
        IncubusFactory.get_instance().user_event()
        buy_foreign_currency.BuyForeignCurrency()

    @staticmethod
    def _currency_account():
        IncubusFactory.get_instance().user_event()
        curr_acc_dist.CurrencyAccountDistribution().execute()

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
            Prime._del_idle_companies__selected,
            companies=idle_companies).mainloop()

    @staticmethod
    def _del_idle_companies__selected(companies: []):
        IncubusFactory.get_instance().user_event()
        for company in companies:
            company.delete()

    @staticmethod
    def _ecz_activity():
        IncubusFactory.get_instance().user_event()
        ecz_activity_comparison.EczActivityComparison().execute()

    @staticmethod
    def _edit_data_file(file_name: str):
        IncubusFactory.get_instance().user_event()
        full_path = os.path.join(config.CONSTANTS["DATA_DIR_PATH"], file_name)
        os.system("open " + full_path)

    @staticmethod
    def _iban_list():
        IncubusFactory.get_instance().user_event()
        iban_list.IbanList().execute()

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
    def _net_worth():
        IncubusFactory.get_instance().user_event()
        net_worth.NetWorth().execute()

    def _notif_double_click(self, dummy): # pylint: disable=W0613
        IncubusFactory.get_instance().user_event()
        selection = self._notif_list.get(self._notif_list.curselection())
        if selection.__contains__("Payment"):
            payment_guid = selection[selection.find("{")+1:selection.find("}")]
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
    def _print_label__company_selected(companies: []):
        IncubusFactory.get_instance().user_event()
        CompanyLabel().generate(companies)

    @staticmethod
    def _reconciliation():
        IncubusFactory.get_instance().user_event()
        company_list.CompanyList(Prime._reconciliation__company_selected).mainloop()

    @staticmethod
    def _reconciliation__company_selected(companies: []):
        IncubusFactory.get_instance().user_event()
        reconciliation.Reconciliation(companies).execute()

    def refresh(self):
        """ Refreshes notifications """
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
        os.system("open " + config.CONSTANTS["DATA_DIR_PATH"])

    @staticmethod
    def _split_latest_activity():
        IncubusFactory.get_instance().user_event()
        last_activity = Activity(Activity.get_last_activity())

        as_window = activity_split.ActivitySplit()
        as_window.fill_with_activity(last_activity)
        as_window.mainloop()
