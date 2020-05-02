import os
import tkinter
from util import backup, currency_update, file_system
from util.company_label import CompanyLabel
from gui import activity, activity_list
from gui import cash_movement, company_list, invoice_list, pay_income_tax
from gui import payment, payment_list, pay_vat, activity_split, buy_foreign_currency
from config.constants import DATA_DIR_PATH, GUI_CELL_HEIGHT
from model import notification, payment as payment_model
from model.activity import Activity
from model.payment import get_companies_without_payment
from report import \
    activity_list as activity_list_report, \
    bank_account_balance, \
    curr_acc_dist, \
    iban_list, \
    net_worth, \
    ecz_activity_comparison, \
    reconciliation


class Prime:
    _NOTIF_HEIGHT = 250
    _WINDOW_WIDTH = 800
    _WINDOW_HEIGHT = 350

    def __init__(self):

        # Initialization
        cell_y = 0

        # Main container
        self._root = tkinter.Tk()
        self._root.title("Kifu")
        self._root.geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))

        # Status label
        self._status_label = tkinter.Label(master = self._root, text="Welcome to Kifu")
        self._status_label.place(x=0, y=cell_y, width=self._WINDOW_WIDTH, height=GUI_CELL_HEIGHT)
        cell_y += GUI_CELL_HEIGHT

        # Notifications

        self._notif_list = tkinter.Listbox(self._root)
        self._refresh()
        self._notif_list.place(x=0, y=cell_y, width=self._WINDOW_WIDTH, height=self._NOTIF_HEIGHT)
        self._notif_list.bind('<Double-1>', self._notif_double_click)
        cell_y += self._NOTIF_HEIGHT

        refresh_button = tkinter.Button(self._root, text="Refresh", command=self._refresh)
        refresh_button.place(x=0, y=cell_y)
        cell_y += GUI_CELL_HEIGHT

        # Main menu

        self._menu = tkinter.Menu(self._root, tearoff=0)

        file_menu = tkinter.Menu(self._menu, tearoff=0)
        for data_file in file_system.get_data_file_list():
            file_menu.add_command(label=data_file, command=lambda df=data_file: self._edit_data_file(df))
        file_menu.add_separator()
        file_menu.add_command(label="Show data files", command=self._show_data_files)
        file_menu.add_command(label="Backup data files", command=self._backup_data)
        file_menu.add_command(label="Exit", command=self._root.quit)
        self._menu.add_cascade(menu=file_menu, label="File")

        timesheet_menu = tkinter.Menu(self._menu, tearoff=0)
        timesheet_menu.add_command(label="Add activity", command=self._add_activity)
        timesheet_menu.add_command(label="Edit activities", command=self._list_activity)
        timesheet_menu.add_command(label="Split latest", command=self._split_latest_activity)
        timesheet_menu.add_separator()
        timesheet_menu.add_command(label="List invoices", command=self._list_invoice)

        self._menu.add_cascade(menu=timesheet_menu, label="Timesheet")

        payment_menu = tkinter.Menu(self._menu, tearoff=0)
        payment_menu.add_command(label="Add payment", command=self._add_payment)
        payment_menu.add_command(label="Book cash movement", command=self._add_cash)
        payment_menu.add_command(label="Buy foreign currency", command=self._buy_curr)
        payment_menu.add_command(label="Pay VAT", command=self._pay_vat)
        payment_menu.add_command(label="Pay income tax", command=self._pay_tax)
        payment_menu.add_separator()
        payment_menu.add_command(label="List payments", command=self._list_payment)
        self._menu.add_cascade(menu=payment_menu, label="Payment")

        report_menu = tkinter.Menu(self._menu, tearoff=0)
        report_menu.add_command(label="Activity report", command=self._activity_report)
        report_menu.add_command(label="Ecz activity comparison", command=self._ecz_activity)
        report_menu.add_command(label="Reconciliation", command=self._reconciliation)
        report_menu.add_separator()
        report_menu.add_command(label="Net worth", command=self._net_worth)
        report_menu.add_command(label="Account balances", command=self._bank_account_balance)
        report_menu.add_command(label="Currency balances", command=self._currency_account)
        report_menu.add_command(label="IBAN list", command=self._iban_list)
        self._menu.add_cascade(menu=report_menu, label="Report")

        util_menu = tkinter.Menu(self._menu, tearoff=0)
        util_menu.add_command(label="Update currencies", command=self._currency_update)
        util_menu.add_command(label="Print labels", command=self._print_label)
        util_menu.add_command(label="Delete idle companies", command=self._del_idle_companies)

        self._menu.add_cascade(menu=util_menu, label="Util")


        # Flush

        self._root.configure(menu=self._menu)
        self._root.mainloop()

    def _activity_report(self):
        activity_list_report.ActivityList().execute()

    def _add_activity(self):
        activity_window = activity.ActivityWindow()
        activity_window.fill_with_last_activity()
        activity_window.mainloop()

    def _add_cash(self):
        cash_movement.CashMovement()

    def _add_payment(self):
        payment_window = payment.PaymentWindow()
        payment_window.fill_with_new_payment()
        payment_window.mainloop()

    def _backup_data(self):
        self._set_status("Backing up")
        backup.execute()
        self._set_status("Backup complete")

    def _bank_account_balance(self):
        bank_account_balance.BankAccountBalance().execute()

    def _buy_curr(self):
        buy_foreign_currency.BuyForeignCurrency()

    def _currency_account(self):
        curr_acc_dist.CurrencyAccountDistribution().execute()

    def _currency_update(self):
        self._set_status("Updating currencies")
        currency_update.execute()
        self._set_status("Currencies updated")

    def _del_idle_companies(self):
        idle_companies = get_companies_without_payment()
        if len(idle_companies) <= 0:
            return
        company_list.CompanyList(self._del_idle_companies__selected, companies=idle_companies).mainloop()

    def _del_idle_companies__selected(self, companies: []):
        for c in companies:
            c.delete()

    def _ecz_activity(self):
        ecz_activity_comparison.EczActivityComparison().execute()

    def _edit_data_file(self, file_name: str):
        full_path = os.path.join(DATA_DIR_PATH, file_name)
        os.system("open " + full_path)

    def _iban_list(self):
        iban_list.IbanList().execute()

    def _list_activity(self):
        list_window = activity_list.ActivityListWindow()
        list_window.mainloop()

    def _list_invoice(self):
        inv_window = invoice_list.InvoiceListWindow()
        inv_window.mainloop()

    def _list_payment(self):
        payment_window = payment_list.PaymentListWindow()
        payment_window.mainloop()

    def _net_worth(self):
        net_worth.NetWorth().execute()

    def _notif_double_click(self, event):
        s = self._notif_list.get(self._notif_list.curselection())
        if s.__contains__("Payment"):
            payment_guid = s[s.find("{")+1:s.find("}")]
            payment_obj = payment_model.get_payment_with_guid(payment_guid)
            if payment_obj is None:
                return
            payment_win = payment.PaymentWindow()
            payment_win.fill_with_payment(payment_obj)
            payment_win.mainloop()

    def _pay_tax(self):
        pay_income_tax.PayIncomeTax()

    def _pay_vat(self):
        pay_vat.PayVat()

    def _print_label(self):
        company_list.CompanyList(self._print_label__company_selected).mainloop()

    def _print_label__company_selected(self, companies: []):
        CompanyLabel().generate(companies)

    def _reconciliation(self):
        company_list.CompanyList(self._reconciliation__company_selected).mainloop()

    def _reconciliation__company_selected(self, companies: []):
        reconciliation.Reconciliation(companies).execute()

    def _refresh(self):
        self._notif_list.delete(0, tkinter.END)
        notif_count = 0
        for ntf in notification.get_notifications():
            self._notif_list.insert(notif_count, ntf)
            notif_count += 1
        self._root.update()

    def _set_status(self, status: str):
        self._status_label["text"] = status
        self._root.update()

    def _show_data_files(self):
        os.system("open " + DATA_DIR_PATH)

    def _split_latest_activity(self):
        last_activity = Activity(Activity.get_last_activity())

        as_window = activity_split.ActivitySplit()
        as_window.fill_with_activity(last_activity)
        as_window.mainloop()

