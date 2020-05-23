""" Excel activity output """
import xlsxwriter
import model.activity
from model.activity import Activity
from model.company import Company
from model.project import Project
import util.file_system
from config.constants import COMPANY_NAME_1E1, HOME_COMPANY, COMPANY_NAME_ECZ_TUG


def _get_excel_key(year: int, month: int, project: Project):
    return year, month, project.payer.name


class ExcelFile:
    """ Excel file """

    FILE_EXTENSION = "xlsx"

    def __init__(self):
        self._activities = []
        self._home_company = Company(HOME_COMPANY)

    def add_activity(self, activity: model.activity.Activity):
        """ Add new activity to Excel file """
        self._activities.append(activity)

    def save_file(self, file_name: str):
        """ Write Excel file to disk """

        ##########
        # Preparation
        ##########

        workbook = xlsxwriter.Workbook(file_name)
        bold_format = workbook.add_format({'bold': True})
        money_format = workbook.add_format({'num_format': '0.00'})
        date_format = workbook.add_format({'num_format': 'd.mm.yyyy'})

        ##########
        # Regular worksheet
        ##########

        worksheet = workbook.add_worksheet("Activities")
        row = 0

        # Titles
        worksheet.write(row, 0, "Client", bold_format)
        worksheet.write(row, 1, "Project", bold_format)
        worksheet.write(row, 2, "Date", bold_format)
        worksheet.write(row, 3, "Hours", bold_format)
        worksheet.write(row, 4, "Earned", bold_format)
        worksheet.write(row, 5, "VAT", bold_format)
        worksheet.write(row, 6, "Total", bold_format)
        worksheet.write(row, 7, "Currency", bold_format)
        row += 1

        # Content
        for activity in self._activities:
            prj = activity.project
            earned_amount, currency = activity.earned_amount
            vat_amount = prj.get_vat_amount(earned_amount)
            total_amount = earned_amount + vat_amount

            worksheet.write(row, 0, prj.client.name)
            worksheet.write(row, 1, prj.name)
            worksheet.write(row, 2, activity.date, date_format)
            worksheet.write(row, 3, activity.hours)
            worksheet.write(row, 4, earned_amount, money_format)
            worksheet.write(row, 5, vat_amount, money_format)
            worksheet.write(row, 6, total_amount, money_format)
            worksheet.write(row, 7, currency)
            row += 1

        # Sum
        worksheet.write(row, 3, "Total", bold_format)
        worksheet.write(row, 4, "=SUM(E2:E" + str(row) + ")", money_format)
        worksheet.write(row, 5, "=SUM(F2:F" + str(row) + ")", money_format)
        worksheet.write(row, 6, "=SUM(G2:G" + str(row) + ")", money_format)
        row += 1

        ##########
        # 1e1 - Ecz
        ##########

        tug_found = False

        for activity in self._activities:
            prj = activity.project
            if prj.client.name == COMPANY_NAME_ECZ_TUG and prj.payer.name == COMPANY_NAME_1E1:
                if not tug_found:
                    tug_found = True
                    worksheet = workbook.add_worksheet("Eczacibasi")
                    row = 0
                    worksheet.write(row, 0, "Danışman", bold_format)
                    worksheet.write(row, 1, "Tarih", bold_format)
                    worksheet.write(row, 2, "Lokasyon", bold_format)
                    worksheet.write(row, 3, "Açıklama", bold_format)
                    worksheet.write(row, 4, "Faturalanabilir saat", bold_format)

                row += 1
                worksheet.write(row, 0, self._home_company.contact_person)
                worksheet.write(row, 1, activity.date, date_format)
                worksheet.write(row, 2, activity.location)
                worksheet.write(row, 3, activity.work)
                worksheet.write(row, 4, activity.hours, bold_format)

        ##########
        # Flush
        ##########

        workbook.close()


class Report:
    """ Report """

    def __init__(self):
        self._activities = []
        self._excel_files = {}

    def generate(self):
        """ Generate report with all activities """
        self._generate_with_dict(Activity.get_activities())

    def generate_with_activity_objects(self, activities: []):
        """ Generate report with given activities """
        act_dict = {}
        act_dict["activities"] = []
        for act in activities:
            act_dict["activities"].append(act.dict)

        self._generate_with_dict(act_dict)

    def _generate_with_dict(self, activity_dict: {}):
        self._activities = activity_dict.copy()
        self._plan_excel_files()
        self._save_excel_files()

    def _plan_excel_files(self):

        for activity in self._activities["activities"]:
            act = model.activity.Activity(activity)
            year, month = act.period
            excel_key = _get_excel_key(year, month, act.project)

            if excel_key not in self._excel_files:
                self._excel_files[excel_key] = ExcelFile()

            self._excel_files[excel_key].add_activity(act)

    def _save_excel_files(self):
        for excel_key in self._excel_files:
            file_name = ""
            for i in range(len(excel_key)): # pylint: disable=C0200
                if file_name != "":
                    file_name += " "
                file_name += str(excel_key[i])
            file_path = util.file_system.get_desktop_file_name(file_name, ExcelFile.FILE_EXTENSION)
            self._excel_files[excel_key].save_file(file_path)
