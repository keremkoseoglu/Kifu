import json
import os
from model.company import Company
from config.constants import *


class Project:

    _PROJECT_FILE = "project.json"

    @staticmethod
    def get_projects():
        file_path = os.path.join(DATA_DIR_PATH + Project._PROJECT_FILE)
        with open(file_path) as f:
            json_data = json.load(f)
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
        return self._client

    @property
    def income_tax_rate(self) -> float:
        return float(self._project["tax"]["income_tax_rate"])

    @property
    def payer(self) -> Company:
        return self._payer

    @property
    def vat_rate(self) -> float:
        return float(self._project["tax"]["vat_rate"])

    @property
    def name(self) -> str:
        return self._project["project_name"]

    @property
    def rate(self) -> tuple:
        amount = float(self._project["rate"]["amount"])
        currency = self._project["rate"]["currency"]
        per_hour = int(self._project["rate"]["per_hour"])
        return amount, currency, per_hour

    def get_earned_amount(self, hours: int) -> tuple:
        amount, currency, per_hour = self.rate
        earned_amount = (amount / per_hour) * hours
        return earned_amount, currency

    def get_vat_amount(self, base_amount: float) -> float:
        return base_amount * self.vat_rate / 100