""" Eczacibasi activity comparison module """
from datetime import datetime
from util import date_time, ecz_daha
from model.timesheet.activity import Activity
import config

class EczActivityComparisonAPI():
    """ Eczacibasi activity comparison class """
    def __init__(self):
        self._result = {}
        self._ecz = config.CONSTANTS["COMPANY_NAME_ECZ_TUG"]

    @property
    def result(self) -> dict:
        """ Returns output """
        self._result = {"ThisMonth": [], "PrevMonth": []}

        this_year = datetime.now().year
        this_month = datetime.now().month
        self._append_month(this_year, this_month, "ThisMonth")

        prev_year = this_year
        prev_month = this_month - 1
        if prev_month == 0:
            prev_year -= 1
            prev_month = 12
        self._append_month(prev_year, prev_month, "PrevMonth")

        return self._result

    def _append_month(self, year: int, month: int, elem: str):
        sap_year = str(year)
        sap_month = date_time.get_two_digit_month(month)
        ecz_activities = ecz_daha.get_monthly_activity(p_sap_year=sap_year, p_sap_month=sap_month)

        for ecz_activity in ecz_activities:
            date_of_activity = date_time.parse_sap_date(ecz_activity["date"])

            kifu_hour_sum = Activity.get_time_sum(client_name=self._ecz,
                                                  date=date_of_activity)

            date = date_time.get_formatted_date(date_time.parse_sap_date(ecz_activity["date"]))

            entry = {"date": date,
                     "comment": ecz_activity["comment"],
                     "ecz_hours": ecz_activity["hours"],
                     "kifu_hours": kifu_hour_sum,
                     "different": kifu_hour_sum != ecz_activity["hours"]}

            self._result[elem].append(entry)
