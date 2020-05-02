import tkinter
from gui.labeled_combobox import LabeledCombobox
from model.company import Company


class CompanyCombobox:

    def __init__(self, parent: tkinter.Toplevel, label_text: str, x_pos: int, y_pos: int):
        self._companies = Company.get_companies()

        self._combo_val = []
        for cmp in self._companies["companies"]:
            self._combo_val.append(cmp["name"])

        self._combo = LabeledCombobox(parent, label_text, self._combo_val, x_pos, y_pos)

    def get_company_name(self) -> str:
        return self._combo.get_selected_value()

    def set_company(self, name: str):
        self._combo.set_selected_value(name)