""" Activity window """
import datetime
import tkinter
import tkinter.ttk
from gui.labeled_combobox import LabeledCombobox
from gui.labeled_textbox import LabeledTextbox
from gui.prime_singleton import PrimeSingleton
from gui.font import default_font
from util import ecz_daha
import model.activity
import model.location
import model.project
from model.project import Project
from model.activity import Activity
import config


class ActivityWindow(tkinter.Toplevel):
    """ Activity window """

    _WINDOW_WIDTH = 550
    _WINDOW_HEIGHT = 300

    def __init__(self):
        # Initialization

        tkinter.Toplevel.__init__(self)
        self.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))
        cell_y = 0

        # GUID
        self._guid = LabeledTextbox(self, "GUID", "", 0, cell_y)
        self._guid.disable()
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Project
        self._projects = Project.get_projects()
        self._project_combo_val = []
        self._build_project_combo_values()
        self._project_combo = LabeledCombobox(self, "Project", self._project_combo_val, 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Location
        self._locations = model.location.get_locations()
        self._location_combo_val = []
        self._build_location_combo_values()
        self._location_combo = LabeledCombobox(
            self,
            "Location",
            self._location_combo_val,
            0,
            cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Date
        self._date = LabeledTextbox(self, "Date", datetime.datetime.now().isoformat(), 0, cell_y)
        save_button = tkinter.Button(self, text="Ecz", command=self._ecz_click, font=default_font())
        save_button.place(x=(config.CONSTANTS["GUI_CELL_WIDTH"]*2+150), y=cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Duration
        self._duration = LabeledTextbox(self, "Duration", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Work
        self._work = LabeledTextbox(self, "Work", "", 0, cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Button
        save_button = tkinter.Button(self,
                                     text="Save",
                                     command=self._save_click,
                                     font=default_font())
        save_button.place(x=config.CONSTANTS["GUI_CELL_WIDTH"], y=cell_y)
        cell_y += config.CONSTANTS["GUI_CELL_HEIGHT"]

        # Status
        self._status_label = tkinter.Label(master=self, text="", font=default_font())
        self._status_label.place(
            x=0,
            y=cell_y,
            width=self._WINDOW_WIDTH,
            height=config.CONSTANTS["GUI_CELL_HEIGHT"])

    def fill_with_activity(self, act: model.activity.Activity):
        """ Fills window with given activity """
        proj = act.project
        clnt = proj.client

        self._project_combo.selected_value = clnt.name + " - " + proj.name
        self._location_combo.selected_value = act.location
        self._date.value = act.date.isoformat()
        self._duration.value = str(act.hours)
        self._work.value = act.work
        self._guid.value = act.guid

    def fill_with_last_activity(self):
        """ Fills window with last activity """
        last_activity = Activity.get_last_activity()
        if last_activity == {}:
            return
        act_obj = model.activity.Activity(last_activity)
        act_obj.guid = ""
        act_obj.date = datetime.datetime.today()
        self.fill_with_activity(act_obj)
        self._set_status("(filled with last activity)")

    def _build_project_combo_values(self):
        for prj in self._projects["projects"]:
            self._project_combo_val.append(prj["client_name"] + " - " + prj["project_name"])

    def _build_location_combo_values(self):
        for loc in self._locations:
            self._location_combo_val.append(loc)

    def _ecz_click(self):
        sap_date = self._date.value[:12].replace("-", "")
        daily_activity = ecz_daha.get_daily_activity(sap_date)
        self._duration.value = daily_activity["hours"]
        self._work.value = daily_activity["comment"]

    def _save_click(self):
        project_full = self._project_combo.selected_value
        client, project = project_full.split(" - ")
        location = self._location_combo.selected_value
        date = self._date.value
        duration = self._duration.value
        work = self._work.value
        guid = self._guid.value

        act = {
            "date": date,
            "client_name": client,
            "project_name": project,
            "location": location,
            "duration": duration,
            "work": work,
            "guid": guid
        }

        model.activity.Activity(act).save()
        self._set_status("Saved!")
        PrimeSingleton.get().refresh()
        self.after(1, self.destroy())

    def _set_status(self, status: str):
        self._status_label["text"] = status
        self.update()
