from config.constants import *
from gui.labeled_combobox import LabeledCombobox
from gui.labeled_textbox import LabeledTextbox
import model.activity, model.project
from model.project import Project
from model.activity import Activity
import tkinter, tkinter.ttk


class ActivitySplit(tkinter.Toplevel):

    _WINDOW_WIDTH = 400
    _WINDOW_HEIGHT = 250

    def __init__(self):

        self._debut_activity = None

        # Initialization

        tkinter.Toplevel.__init__(self)
        self.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))
        cell_y = 0

        # Project

        self._projects = Project.get_projects()
        self._project_combo_val = []
        self._build_project_combo_values()
        self._project_combo = LabeledCombobox(self, "Project", self._project_combo_val, 0, cell_y)
        cell_y += GUI_CELL_HEIGHT

        # Duration

        self._duration = LabeledTextbox(self, "Duration", "", 0, cell_y)
        cell_y += GUI_CELL_HEIGHT

        # Work

        self._work = LabeledTextbox(self, "Work", "", 0, cell_y)
        cell_y += GUI_CELL_HEIGHT

        # Button

        save_button = tkinter.Button(self, text="Save", command=self._save_click)
        save_button.place(x=GUI_CELL_WIDTH, y=cell_y)
        cell_y += GUI_CELL_HEIGHT

    def fill_with_activity(self, act: model.activity.Activity):

        self._debut_activity = act

        proj = self._debut_activity.project
        clnt = self._debut_activity.client

        self._project_combo.set_selected_value(clnt.name + " - " + proj.name)
        self._duration.set_value(str(0))
        self._work.set_value(act.work)

    def fill_with_last_activity(self):
        last_activity = Activity.get_last_activity()
        if last_activity == {}:
            return
        self.fill_with_activity(last_activity)

    def _build_project_combo_values(self):
        for prj in self._projects["projects"]:
            self._project_combo_val.append(prj["client_name"] + " - " + prj["project_name"])

    def _save_click(self):

        project_full = self._project_combo.get_selected_value()
        client, project = project_full.split(" - ")

        self._debut_activity.split(
            client_name=client,
            project_name=project,
            hours=int(self._duration.get_value()),
            work=self._work.get_value()
        )

        self.destroy()