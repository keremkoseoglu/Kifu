""" Activity list window """
import tkinter
import tkinter.ttk
from typing import List
from model.timesheet import invoice
from model.timesheet import activity
from model.timesheet.activity import Activity
from model.timesheet.project import Project
from model.company import Company
from gui.activity import ActivityWindow
from gui.activity_split import ActivitySplit
from gui.font import default_font
from gui.invoice import InvoiceWindow
from gui.popup_file import popup_email
from gui.prime_singleton import PrimeSingleton
from util import activity_xlsx_report, backup, date_time
from util.amount import get_formatted_amount
from util.text import replace_turkish_chars
import config


class ActivityListWindow(tkinter.Toplevel):
    """Activity list window"""

    _BUTTON_WIDTH = 150
    _WINDOW_WIDTH = 1200
    _WINDOW_HEIGHT = 400
    _Y_SPACING = 10

    def __init__(self):
        # Initialization
        tkinter.Toplevel.__init__(self)
        self.wm_geometry(str(self._WINDOW_WIDTH) + "x" + str(self._WINDOW_HEIGHT))

        # Build tree
        self._tree = tkinter.ttk.Treeview(self)
        tree_height = (
            self._WINDOW_HEIGHT - config.CONSTANTS["GUI_CELL_HEIGHT"] - self._Y_SPACING
        )
        self._tree.place(x=0, y=0, width=self._WINDOW_WIDTH, height=tree_height)
        cell_y = tree_height + self._Y_SPACING

        self._tree["columns"] = ("Client", "Project", "Location", "GUID")
        self._tree.heading("Client", text="Client")
        self._tree.heading("Project", text="Project")
        self._tree.heading("Location", text="Location")
        self._tree.heading("GUID", text="GUID")

        # Fill tree with data
        self._activities = []
        self._tree_content = {}
        self._fill_tree_with_activities()

        # Buttons
        cell_x = 0

        edit_button = tkinter.Button(
            self, text="Edit", command=self._edit_click, font=default_font()
        )
        edit_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        edit_button = tkinter.Button(
            self, text="Excel", command=self._excel_click, font=default_font()
        )
        edit_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        edit_button = tkinter.Button(
            self, text="Mail sum", command=self._mail_sum_click, font=default_font()
        )
        edit_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        split_button = tkinter.Button(
            self, text="Split", command=self._split_click, font=default_font()
        )
        split_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        invoice_button = tkinter.Button(
            self, text="Invoice", command=self._invoice_click, font=default_font()
        )
        invoice_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

        invoice_button = tkinter.Button(
            self, text="Delete", command=self._delete_click, font=default_font()
        )
        invoice_button.place(x=cell_x, y=cell_y)
        cell_x += self._BUTTON_WIDTH

    @property
    def _first_selected_activity(self) -> activity.Activity:
        selected_activities = self._selected_activities
        if len(selected_activities) == 0:
            return None

        return selected_activities[0]

    @property
    def _selected_activities(self) -> List:
        selected_activities = []

        for selected_id in self._tree.selection():
            selected_activity = self._tree_content[selected_id]
            selected_activities.append(selected_activity)

        return selected_activities

    def _delete_click(self):
        deletable_activities = self._selected_activities
        if len(deletable_activities) == 0:
            return

        deletable_guids = []
        for act in deletable_activities:
            deletable_guids.append(act.guid)

        backup.execute()
        Activity.delete_activities(deletable_guids)

        self._fill_tree_with_activities()
        PrimeSingleton.get().refresh()

    def _edit_click(self):
        first_selected_activity = self._first_selected_activity
        if first_selected_activity is None:
            return

        activity_window = ActivityWindow()
        activity_window.fill_with_activity(first_selected_activity)
        self.after(1, self.destroy())
        activity_window.mainloop()

    def _excel_click(self):
        selected_activity_objects = self._selected_activities
        xlsx_report = activity_xlsx_report.Report()
        xlsx_report.generate_with_activity_objects(selected_activity_objects)

        activity_company = Company(config.CONSTANTS["COMPANY_NAME_1E1"])

        popup_email(
            recipients=activity_company.activity_emails,
            subject="Bu ayki aktivitelerim",
            attachment=xlsx_report.last_saved_files[0],
        )

    def _mail_sum_click(self):
        # Get activities
        selected_activity_objects = self._selected_activities

        # Build list of payers
        selected_payer_names = []
        for sel_activity in selected_activity_objects:
            if sel_activity.project.payer.name not in selected_payer_names:
                selected_payer_names.append(sel_activity.project.payer.name)

        # Process each payer
        for payer_name in selected_payer_names:
            hour_sum = 0
            day_sum = 0
            body = ""
            payer_activities = []
            payer_projects = []
            subject = f"Bu ayki {payer_name} aktivitelerim"

            for sel_activity in selected_activity_objects:
                if sel_activity.project.payer.name != payer_name:
                    continue
                hour_sum += sel_activity.hours
                day_sum += sel_activity.days
                payer_activities.append(sel_activity)

                act_proj_name = self._get_project_name(sel_activity.project)
                if act_proj_name not in payer_projects:
                    payer_projects.append(act_proj_name)

            tmp_payer_invoice = invoice.get_invoice_obj_from_activities(
                payer_activities
            )
            amt_txt = get_formatted_amount(tmp_payer_invoice.amount)
            vat_txt = get_formatted_amount(tmp_payer_invoice.vat_amount)
            sum_txt = get_formatted_amount(tmp_payer_invoice.amount_plus_vat)
            cur_txt = tmp_payer_invoice.currency

            body = f"Bu ayki aktivitelerim toplam {hour_sum} saat = {day_sum} gündür."
            body += f" Onayınıza istinaden; {amt_txt} + {vat_txt} (KDV) = {sum_txt} {cur_txt}"
            body += " fatura kesebilirim."

            body += "\r\n\r\n"

            if len(payer_projects) <= 0:
                pass
            elif len(payer_projects) == 1:
                project_name = payer_projects[0]
                subject += f" [{project_name}]"
                body += f"Proje: {project_name}"
            else:
                body += "Projeler:"
                for payer_project in payer_projects:
                    body += f"\r\n- { payer_project }"

            popup_email(
                recipients=sel_activity.project.payer.activity_emails,
                subject=subject,
                body=body,
            )

    def _fill_tree_with_activities(self):
        self._activities = Activity.get_activities()

        self._activities["activities"] = sorted(
            self._activities["activities"], key=lambda x: x["date"], reverse=True
        )

        self._tree_content = {}

        self._tree.delete(*self._tree.get_children())

        for activity_line in self._activities["activities"]:
            activity_obj = activity.Activity(activity_line)
            project_obj = activity_obj.project
            tree_val = (
                project_obj.client.name,
                project_obj.name,
                activity_obj.location,
                activity_obj.guid,
            )

            id_in_tree = self._tree.insert(
                "",
                "end",
                text=date_time.get_formatted_date(activity_obj.date),
                value=tree_val,
            )
            self._tree_content[id_in_tree] = activity_obj

        self.update()

    def _invoice_click(self):
        selected_activities = self._selected_activities
        if len(selected_activities) == 0:
            return

        new_invoice = invoice.get_invoice_obj_from_activities(selected_activities)
        invoice_window = InvoiceWindow()
        invoice_window.fill_with_invoice(new_invoice, browser=True, invoice_dir=True)
        invoice_window.mainloop()

    def _split_click(self):
        first_selected_activity = self._first_selected_activity
        if first_selected_activity is None:
            return
        activity_split = ActivitySplit()
        activity_split.fill_with_activity(first_selected_activity)
        self.after(1, self.destroy())
        activity_split.mainloop()

    def _get_project_name(self, project: Project) -> str:
        result = replace_turkish_chars(project.client_and_name)
        inv_int = project.invoice_interval
        if inv_int != "":
            result += f" ({inv_int})"
        return result
