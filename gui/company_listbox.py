""" Company list box control """
import tkinter
from typing import List
from model.company import Company


class CompanyListbox:
    """ Company list box control """

    def __init__(self,
                 parent: tkinter.Toplevel,
                 x_pos: int,
                 y_pos: int,
                 companies: List[Company] = None):
        self._combo_val = []

        if companies is None:
            all_companies = Company.get_companies()
            for cmp in all_companies["companies"]:
                self._combo_val.append(cmp["name"])
        else:
            for cmp in companies:
                self._combo_val.append(cmp.name)

        self._combo = tkinter.Listbox(parent, selectmode=tkinter.EXTENDED)

        for value in self._combo_val:
            self._combo.insert(tkinter.END, value)

        self._combo.place(x=x_pos, y=y_pos)

    @property
    def selected_company_names(self) -> List[str]:
        """ Returns selected company names """
        items = self._combo.curselection()
        return [self._combo_val[int(item)] for item in items]
