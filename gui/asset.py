""" Asset window """

import datetime
import tkinter
import tkinter.ttk
import config
from gui.labeled_combobox import LabeledCombobox
from gui.labeled_textbox import LabeledTextbox
from gui.labeled_checkbox import LabeledCheckbox
from gui.font import default_font
import model.asset as asset_model


class AssetWindow(tkinter.Toplevel):
    """Asset window"""

    _WINDOW_WIDTH = 450
    _WINDOW_HEIGHT = 600

    def __init__(self):
        # Initialization

        tkinter.Toplevel.__init__(self)
        self.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))
        cell_y = 0

        # GUID
        self._guid = LabeledTextbox(self, "GUID", "", 0, cell_y)
        self._guid.disable()
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Name
        self._name = LabeledTextbox(self, "Name", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Type
        self._asset_types = asset_model.get_asset_types()
        self._asset_type_combo_val = []
        self._build_asset_type_combo_values()
        self._asset_type_combo = LabeledCombobox(
            self, "Type", self._asset_type_combo_val, 0, cell_y
        )
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Purcase date
        self._purchase_date = LabeledTextbox(
            self, "Pur. Date", datetime.datetime.now().isoformat(), 0, cell_y
        )
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Purchase value
        self._purchase_value = LabeledTextbox(self, "Pur. value", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Official purchase value
        self._official_purchase_value = LabeledTextbox(
            self, "Off. value", "", 0, cell_y
        )
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Sales value
        self._sales_value = LabeledTextbox(self, "Sales value", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Currency
        self._currency = LabeledTextbox(self, "Currency", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Quantity
        self._quantity = LabeledTextbox(self, "Quantity", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Own percentage
        self._own_percentage = LabeledTextbox(self, "Own percentage", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Partner percentage
        self._partner_percentage = LabeledTextbox(
            self, "Partner percentage", "", 0, cell_y
        )
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Bank
        self._bank = LabeledTextbox(self, "Bank", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # URL suffix
        self._url_suffix = LabeledTextbox(self, "URL suffix", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Income tax
        self._income_tax = LabeledCheckbox(self, "Income tax", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Button
        save_button = tkinter.Button(
            self, text="Save", command=self._save_click, font=default_font()
        )
        save_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"], y=cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Status
        self._status_label = tkinter.Label(master=self, text="", font=default_font())
        self._status_label.place(
            x=0,
            y=cell_y,
            width=self._WINDOW_WIDTH,
            height=config.CONSTANTS["GUI_CELL_HEIGHT"],
        )

    def fill_with_asset(self, asset: dict):
        """Fills window with given activity"""
        self._guid.value = asset["guid"]
        self._name.value = asset["name"]
        self._asset_type_combo.selected_value = asset["type"]
        self._purchase_date.value = asset["purchase_date"]
        self._purchase_value.value = asset["purchase_value"]
        self._official_purchase_value.value = asset["official_purchase_value"]
        self._sales_value.value = asset["sales_value"]
        self._currency.value = asset["currency"]
        self._quantity.value = asset["quantity"]
        self._own_percentage.value = asset["own_percentage"]
        self._partner_percentage.value = asset["partner_percentage"]
        self._url_suffix.value = asset["url_suffix"]
        self._income_tax.checked = asset["income_tax"]

        if "bank" in asset:
            self._bank.value = asset["bank"]
        else:
            self._bank.value = ""

    def _build_asset_type_combo_values(self):
        for asset_type in self._asset_types:
            self._asset_type_combo_val.append(asset_type)

    def _save_click(self):
        asset = {
            "guid": self._guid.value,
            "name": self._name.value,
            "type": self._asset_type_combo.selected_value,
            "purchase_date": self._purchase_date.value,
            "purchase_value": float(self._purchase_value.value),
            "official_purchase_value": float(self._official_purchase_value.value),
            "sales_value": float(self._sales_value.value),
            "currency": self._currency.value,
            "quantity": float(self._quantity.value),
            "own_percentage": float(self._own_percentage.value),
            "partner_percentage": float(self._partner_percentage.value),
            "bank": self._bank.value,
            "url_suffix": self._url_suffix.value,
            "income_tax": self._income_tax.checked,
            "value_history": [],
        }

        asset_model.set_asset(asset)
        self._set_status("Saved!")
        self.after(1, self.destroy())

    def _set_status(self, status: str):
        self._status_label["text"] = status
        self.update()
