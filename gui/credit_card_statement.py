""" Credit card statement GUI """
import datetime
import json
from os import path
import tkinter
from typing import List
import config
from gui.amount_textbox import AmountTextbox
from gui.company_combobox import CompanyCombobox
from gui.labeled_textbox import LabeledTextbox
from gui.prime_singleton import PrimeSingleton
from gui.font import default_font
from model.payment import payment
from util import date_time


class LastCompanyCreditCardStatement:
    """Last credit card statement"""

    _JSON_FILE = "cc_statement_last.json"

    def __init__(self, company_name: str):
        self._company_name = company_name
        self._json_path = path.join(
            config.CONSTANTS["DATA_DIR_PATH"],
            LastCompanyCreditCardStatement._JSON_FILE,
        )

    @property
    def last_statement_date_str(self) -> str:
        """Last statement date string"""
        companies = self._companies_as_list
        for company in companies:
            if company["company"] == self._company_name:
                return company["date"]
        return ""

    @property
    def next_statement_date(self) -> str:
        """Next statement date string"""
        last_date_str = self.last_statement_date_str
        if last_date_str == "":
            return ""
        last_date = date_time.parse_json_date(last_date_str)
        next_date = date_time.get_next_month(last_date)
        next_date_str = str(next_date)
        return f"{ next_date_str[:10] }{last_date_str[10:]}"

    @last_statement_date_str.setter
    def last_statement_date_str(self, new_value):
        company_in_json = False
        companies = self._companies_as_list

        for company in companies:
            if company["company"] == self._company_name:
                company_in_json = True
                company["date"] = new_value
                break

        if not company_in_json:
            companies.append({"company": self._company_name, "date": new_value})

        with open(self._json_path, "w", encoding="utf-8") as file:
            json.dump(companies, file)

    @property
    def _companies_as_list(self) -> List:
        with open(self._json_path, "r", encoding="utf-8") as file:
            return json.load(file)


class CreditCardStatement:
    """GUI to record credit card statement"""

    _WINDOW_WIDTH = 600
    _WINDOW_HEIGHT = 200

    def __init__(self):
        self._window = tkinter.Toplevel()
        self._window.wm_geometry(
            str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT)
        )
        cell_y = 0

        self._company = CompanyCombobox(self._window, "Bank", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._payment_date = LabeledTextbox(
            self._window, "Payment date", datetime.datetime.now().isoformat(), 0, cell_y
        )

        edit_button = tkinter.Button(
            self._window,
            text="Auto",
            command=self._auto_date_click,
            font=default_font(),
        )
        edit_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"] * 3, y=cell_y)

        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        self._amount = AmountTextbox(
            self._window, "Amount", 0, config.CONSTANTS["HOME_CURRENCY"], 0, cell_y
        )
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        save_button = tkinter.Button(
            self._window, text="OK", command=self._ok_click, font=default_font()
        )

        save_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"], y=cell_y)

    def _ok_click(self):
        payment.create_credit_card_transaction(
            bank=self._company.company_name,
            description=self._company.company_name + " statement",
            card="credit card",
            amount=self._amount.amount,
            currency=self._amount.currency,
            pay_date=self._payment_date.value,
        )

        LastCompanyCreditCardStatement(
            self._company.company_name
        ).last_statement_date_str = self._payment_date.value

        PrimeSingleton.get().refresh()
        self._window.destroy()

    def _auto_date_click(self):
        date_text = LastCompanyCreditCardStatement(
            self._company.company_name
        ).next_statement_date
        if date_text != "":
            self._payment_date.value = date_text
