""" Company list window """
import tkinter
import tkinter.ttk
from typing import List
from gui.company_listbox import CompanyListbox
from model.company import Company


class CompanyList(tkinter.Toplevel):
    """ Company list window """

    _WINDOW_WIDTH = 200
    _WINDOW_HEIGHT = 250

    def __init__(self, close_handler, companies: List[Company] = None):

        # Initialization
        self._close_handler = close_handler
        tkinter.Toplevel.__init__(self)
        self.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))

        # Listbox
        self._listbox = CompanyListbox(self, 0, 0, companies=companies)

        # Buttons
        print_button = tkinter.Button(self, text="Select", command=self._company_selected)
        print_button.place(x=0, y=200)

    def _company_selected(self):
        obj_array = []
        selected_companies = self._listbox.selected_company_names
        for selected_company in selected_companies:
            company_obj = Company(selected_company)
            obj_array.append(company_obj)
        if len(obj_array) <= 0:
            return
        self._close_handler(obj_array)
