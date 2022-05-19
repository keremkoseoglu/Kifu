""" Project """
import json
import os
from model.company import Company
import config


class Project:
    """ Project """
    _PROJECT_FILE = "project.json"

    @staticmethod
    def get_projects():
        """ Returns all projects """
        file_path = os.path.join(config.CONSTANTS["DATA_DIR_PATH"] + Project._PROJECT_FILE)
        with open(file_path, encoding="utf-8") as project_file:
            json_data = json.load(project_file)
        return json_data

    def __init__(self, client_name: str, project_name: str):
        all_projects = Project.get_projects()

        self._project = {}
        for prj in all_projects["projects"]:
            if prj["client_name"] == client_name and prj["project_name"] == project_name:
                self._project = prj
                break

        self._client = Company(self._project["client_name"])
        self._payer = Company(self._project["payer_name"])

    @property
    def client(self) -> Company:
        """ Returns the client of the project """
        return self._client

    @property
    def payer(self) -> Company:
        """ Project payer """
        return self._payer

    @property
    def vat_rate(self) -> float:
        """ Project VAT rate """
        return float(self._project["tax"]["vat_rate"])

    @property
    def name(self) -> str:
        """ Project name """
        return self._project["project_name"]

    @property
    def rate(self) -> tuple:
        """ Hourly project rate """
        amount = float(self._project["rate"]["amount"])
        currency = self._project["rate"]["currency"]
        per_hour = int(self._project["rate"]["per_hour"])
        return amount, currency, per_hour

    def get_earned_amount(self, hours: int) -> tuple:
        """ Calculates earned amount based on given hours """
        amount, currency, per_hour = self.rate
        earned_amount = (amount / per_hour) * hours
        return earned_amount, currency

    def get_vat_amount(self, base_amount: float) -> float:
        """ Calculates VAT based on given amount """
        return base_amount * self.vat_rate / 100
