""" Activity """
import datetime
import json
import os
import copy
from typing import List, Dict
from model.currency import CurrencyConverter
from model.timesheet.project import Project
from model.company import Company
from util import date_time, identifier
import config


class Activity:
    """ Activity """
    _ACTIVITY_FILE = "activity.json"

    @staticmethod
    def delete_activities(activity_guids: List):
        """ Deletes the given activities """
        all_activities = Activity.get_activities()
        new_activities = {"activities": []}
        for i in range(len(all_activities["activities"])):
            activity_i = all_activities["activities"][i]
            if activity_i["guid"] not in activity_guids:
                new_activities["activities"].append(activity_i)
        Activity._write_activities_to_disk(new_activities)

    @staticmethod
    def get_activities():
        """ Returns all activities """
        with open(Activity._get_file_path(), encoding="utf-8") as act_file:
            json_data = json.load(act_file)
        return json_data

    @staticmethod
    def get_last_activity() -> Dict:
        """ Returns last activity """
        all_activities = Activity.get_activities()["activities"]
        if len(all_activities) == 0:
            return {}
        return all_activities[len(all_activities) - 1]

    @staticmethod
    def get_time_sum(client_name: str, date: datetime) -> int:
        """ Returns the sum of time spent """
        output = 0

        all_activities = Activity.get_activities()

        for candidate_activity in all_activities["activities"]:
            activity_obj = Activity(candidate_activity)
            activity_client = activity_obj.client.name
            activity_date = activity_obj.date
            if activity_client == client_name and date_time.equals(activity_date, date):
                output += activity_obj.hours

        return output

    @staticmethod
    def get_total_activity_earnings() -> float:
        """ Returns current activity earnings """
        output = 0
        for activity_dict in Activity.get_activities()["activities"]:
            activity = Activity(activity_dict)
            output += activity.earned_amount_in_local_currency
        return output

    @staticmethod
    def has_activity_for_today() -> bool:
        """ Has activity for today?
        Used in notifications to warn on missing activities
        """
        for act_json in Activity.get_activities()["activities"]:
            act_obj = Activity(act_json)
            if date_time.is_today(act_obj.date):
                return True
        return False

    @staticmethod
    def _get_file_path() -> str:
        return os.path.join(config.CONSTANTS["DATA_DIR_PATH"] + Activity._ACTIVITY_FILE)

    @staticmethod
    def _write_activities_to_disk(activities: Dict):
        with open(Activity._get_file_path(), "w", encoding="utf-8") as act_file:
            json.dump(activities, act_file, indent=3)

    def __init__(self, activity: Dict):
        self._activity = None
        self._project = None
        self.dict = activity

    @property
    def client(self) -> Company:
        """ Activity client """
        return self.project.client

    @property
    def date(self) -> datetime:
        """ Activity dateclient """
        return date_time.parse_json_date(self._activity["date"])

    @date.setter
    def date(self, date: datetime.datetime):
        """ Activity client """
        self._activity["date"] = date.isoformat()

    @property
    def guid(self) -> str:
        """ Activity guid """
        return self._activity["guid"]

    @guid.setter
    def guid(self, guid: str):
        """ Activity guid """
        self._activity["guid"] = guid

    @property
    def earned_amount(self) -> tuple:
        """ Activity generated amount """
        return self._project.get_earned_amount(self.hours)

    @property
    def earned_amount_in_local_currency(self) -> float:
        """ Activity generated amount in local currency """
        foreign_amount, foreign_currency = self.earned_amount
        return CurrencyConverter().convert_to_local_currency(foreign_amount, foreign_currency)

    @property
    def hours(self) -> int:
        """ Activity hours """
        return int(self._activity["duration"])

    @hours.setter
    def hours(self, hours: int):
        """ Activity hours """
        self._activity["duration"] = hours

    @property
    def dict(self) -> Dict:
        """ Activity as a dict """
        return self._activity

    @dict.setter
    def dict(self, activity: Dict):
        """ Activity as a dict """
        self._activity = activity
        self.set_project(activity["client_name"], activity["project_name"])

    @property
    def location(self) -> str:
        """ Activity location """
        return self._activity["location"]

    @property
    def month(self) -> int:
        """ Activity month """
        return self.date.month

    @property
    def period(self) -> tuple:
        """ Activity period """
        year = int(self._activity["date"][:4])
        month = int(self._activity["date"][5:7])
        return year, month

    @property
    def project(self) -> Project:
        """ Activity project """
        return self._project

    @property
    def year(self) -> int:
        """ Activity year """
        return self.date.year

    @property
    def work(self) -> str:
        """ Activity work """
        return self._activity["work"]

    @work.setter
    def work(self, work: str):
        """ Activity work """
        self._activity["work"] = work

    def is_in_month(self, p_year: int, p_month: int) -> bool:
        """ Is activity in the given month? """
        return self.year == p_year and self.month == p_month

    def save(self):
        """ Write activity to disk """
        if "guid" not in self._activity:
            self._activity["guid"] = identifier.get_guid()
        elif self._activity["guid"] == "":
            self._activity["guid"] = identifier.get_guid()

        current_activities = Activity.get_activities()
        new_activities = {"activities": []}

        updated = False
        for act in current_activities["activities"]:
            if act["guid"] == self._activity["guid"]:
                new_activities["activities"].append(self._activity)
                updated = True
            else:
                new_activities["activities"].append(act)

        if not updated:
            new_activities["activities"].append(self._activity)

        Activity._write_activities_to_disk(new_activities)

    def set_project(self, client_name: str, project_name: str):
        """ Activity project """
        self._activity["client_name"] = client_name
        self._activity["project_name"] = project_name
        self._project = Project(self._activity["client_name"], self._activity["project_name"])

    def split(self,
              client_name: str,
              project_name: str,
              hours: int,
              work: str):
        """ Splits the activity
        Used when you entered the activity in the morning,
        but worked for a different client during the day
        """

        self.hours -= hours

        new_activity_dict = copy.deepcopy(self.dict)
        new_activity_dict["guid"] = ""
        new_activity = Activity(new_activity_dict)
        new_activity.set_project(client_name, project_name)
        new_activity.work = work
        new_activity.hours = hours

        self.save()
        new_activity.save()
