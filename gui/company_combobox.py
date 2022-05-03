""" Company combobox """
import tkinter
from gui.labeled_combobox import LabeledCombobox
from model.company import Company


class CompanyCombobox:
    """ Company combobox """
    def __init__(self, parent: tkinter.Toplevel, label_text: str, x_pos: int, y_pos: int):
        self._companies = Company.get_companies()

        self._combo_val = []
        for cmp in self._companies["companies"]:
            self._combo_val.append(cmp["name"])

        self._combo = LabeledCombobox(parent, label_text, self._combo_val, x_pos, y_pos)

    @property
    def company_name(self) -> str:
        """ Returns company name """
        return self._combo.selected_value

    @company_name.setter
    def company_name(self, name: str):
        """ Sets company name """
        self._combo.selected_value = name
