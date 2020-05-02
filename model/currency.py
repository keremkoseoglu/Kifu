import json, os
from config.constants import DATA_DIR_PATH, HOME_CURRENCY

_CURR_CONV_FILE = "currency_conv.json"


def save_currency_conv(conv_as_dict: {}):
    file_path = _get_file_path()
    with open(file_path, "w") as f:
        json.dump(conv_as_dict, f, indent=3)


def _get_file_path() -> str:
    return os.path.join(DATA_DIR_PATH + _CURR_CONV_FILE)


class CurrencyConverter:

    def __init__(self):
        self._conv_cache = {}

        file_path = _get_file_path()
        with open(file_path) as f:
            self._conv_rates = json.load(f)

    def convert_to_currency(self, from_amount: float, from_currency: str, to_currency: str) -> float:

        if from_currency == to_currency:
            return from_amount

        if from_currency == HOME_CURRENCY:
            return self.convert_to_foreign_currency(from_amount, to_currency)

        if to_currency == HOME_CURRENCY:
            return self.convert_to_local_currency(from_amount, to_currency)

        raise Exception("Unsupported currency conversion")

    def convert_to_foreign_currency(self, local_amount: float, foreign_currency) -> float:
        if foreign_currency == HOME_CURRENCY:
            return local_amount

        conv_rate = self.get_local_conversion_rate(foreign_currency)
        return local_amount / conv_rate

    def convert_to_local_currency(self, foreign_amount: float, foreign_currency: str) -> float:
        if foreign_currency == HOME_CURRENCY:
            return foreign_amount

        conv_rate = self.get_local_conversion_rate(foreign_currency)
        if conv_rate is None:
            return 0
        return foreign_amount * conv_rate

    def get_local_conversion_rate(self, foreign_currency: str) -> float:
        try:
            return self._conv_cache[foreign_currency]
        except:
            curr_list = self._conv_rates["Tarih_Date"]["Currency"]
            for i in range(len(curr_list)):
                curr_in_list = curr_list[i]
                if curr_in_list["@Kod"] == foreign_currency:
                    float_val = float(curr_in_list["BanknoteBuying"])
                    self._conv_cache[foreign_currency] = float_val
                    return float_val