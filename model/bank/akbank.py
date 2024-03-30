""" Akbank related module """
from typing import List
import glob
from os import path
import csv
from openpyxl import load_workbook
import config
from model.bank.statement import StatementEntry
from util.date_time import parse_turkish_date

class _AccountStatementReader():
    """ Account statement reader
    PROTOCOL: model.bank.AbstractStatementReader
    """
    def __init__(self):
        self._out = []
        self._glob_path = path.join(config.CONSTANTS["DOWNLOAD_DIR"], "*.xlsx")

    def read(self) -> List[StatementEntry]:
        """ Reads statements """
        self._out = []
        xlsx_file_paths = glob.glob(self._glob_path)
        for xlsx_file_path in xlsx_file_paths:
            if "$" in xlsx_file_path:
                continue
            workbook = load_workbook(filename=xlsx_file_path)
            sheet = workbook.active
            for row in sheet.rows:
                if row[0].value == "Tarih":
                    continue
                if row[0].value == "":
                    break
                date = parse_turkish_date(row[0].value)
                amount = row[2].value
                text = row[4].value
                entry = StatementEntry(date, text, amount, config.CONSTANTS["HOME_CURRENCY"])
                self._out.append(entry)

        return self._out

class _CreditCardStatementReader():
    """ Credit card statement reader
    PROTOCOL: model.bank.AbstractStatementReader
    """
    def __init__(self):
        self._out = []
        self._glob_path = path.join(config.CONSTANTS["DOWNLOAD_DIR"], "*.csv")

    def read(self) -> List[StatementEntry]:
        """ Reads statements """
        self._out = []
        csv_file_paths = glob.glob(self._glob_path)
        for csv_file_path in csv_file_paths:
            with open(csv_file_path, "r", encoding="ISO-8859-9") as csv_file:
                csv_lines = csv.reader(csv_file)
                for csv_line in csv_lines:
                    str_line = "".join(csv_line)
                    if str_line.strip() == "":
                        break
                    if str_line[:5] == "Tarih":
                        continue
                    str_vals = str_line.split(";")
                    date = parse_turkish_date(str_vals[0])
                    amount_str = str_vals[2].split(" ")[0]
                    amount_str = amount_str.replace(".", "").replace(",", ".")
                    amount = float(amount_str) * -1 / 100
                    text = str_vals[1]
                    entry = StatementEntry(date, text, amount, config.CONSTANTS["HOME_CURRENCY"])
                    self._out.append(entry)

        return self._out

class StatementReader():
    """ Statement reader
    PROTOCOL: model.bank.AbstractStatementReader
    """
    def __init__(self):
        self._acc_reader = _AccountStatementReader()
        self._crd_reader = _CreditCardStatementReader()

    def read(self) -> List[StatementEntry]:
        """ Reads from sources """
        out = []
        for acc in self._acc_reader.read():
            if abs(acc.amount) >= config.CONSTANTS["STATEMENT_IGNORE_LIMIT"]:
                out.append(acc)
        for crd in self._crd_reader.read():
            if abs(crd.amount) >= config.CONSTANTS["STATEMENT_IGNORE_LIMIT"]:
                out.append(crd)
        return out

    def read_as_list(self) -> List:
        """ Returns statement as a list """
        out = []
        statement_entries = self.read()
        for entry in statement_entries:
            entry_dict = {"date": entry.date,
                          "text": entry.text,
                          "amount": entry.amount,
                          "currency": entry.currency}
            out.append(entry_dict)
        return out

    def read_as_sum_list(self) -> List:
        """ Returns statement as a list, summed by text """
        out = []
        statements = self.read_as_list()
        for statement in statements:
            found = False
            for out_entry in out:
                if out_entry["text"] != statement["text"]:
                    continue
                if out_entry["currency"] != statement["currency"]:
                    continue
                out_entry["amount"] += statement["amount"]
                found = True
            if found:
                continue
            out_entry = {"text": statement["text"],
                         "amount": statement["amount"],
                         "currency": statement["currency"]}
            out.append(out_entry)
        return out
