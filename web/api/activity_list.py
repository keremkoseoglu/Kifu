""" Activity list API """
from model.activity import Activity
from util import date_time

class ActivityListAPI():
    """ Activity list API """
    def __init__(self):
        self._all_activities = {}
        self._all_activities_read = False
        self._todays_activities = {}
        self._todays_activities_read = False

    @property
    def all_activities(self) -> dict:
        """ Returns all activities """
        if not self._all_activities_read:
            self._all_activities = Activity.get_activities()
            for act in self._all_activities["activities"]:
                activity = Activity(act)
                act["date"] = date_time.get_formatted_date(activity.date)
            self._all_activities_read = True
        return self._all_activities

    @property
    def todays_activities(self) -> dict:
        """ Returns todays activities """
        if not self._todays_activities_read:
            self._todays_activities = {"activities": []}
            all_activities = self.all_activities
            for act in all_activities["activities"]:
                activity = Activity(act)
                if date_time.is_today(activity.date):
                    self._todays_activities["activities"].append(act)
            self._todays_activities_read = True
        return self._todays_activities

    @property
    def entire_dataset(self) -> dict:
        """ Returns entire dataset """
        hour_sum = 0
        for act in self.all_activities["activities"]:
            activity = Activity(act)
            hour_sum += activity.hours

        result = {"today": self.todays_activities["activities"],
                  "all": self.all_activities["activities"],
                  "hour_sum": hour_sum,
                  "day_sum": len(self.all_activities["activities"])}
        return result
