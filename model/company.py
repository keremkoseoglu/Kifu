import json
import os
from config.constants import DATA_DIR_PATH, HOME_COUNTRY


class Company:
    _COMPANY_FILE = "company.json"

    @staticmethod
    def get_companies():
        with open(Company._get_company_data_file_path()) as f:
            json_data = json.load(f)
        return json_data

    def __init__(self, company_name: str):
        self._company = {}
        all_companies = Company.get_companies()
        for company in all_companies["companies"]:
            if company["name"] == company_name:
                self._company = company
                break

    @property
    def address(self) -> str:
        if "address" in self._company:
            return self._company["address"]
        else:
            return ""

    @property
    def contact_person(self) -> str:
        if "contact_person" in self._company:
            return self._company["contact_person"]
        else:
            return ""

    @property
    def country(self) -> str:
        if "country" in self._company:
            return self._company["country"]
        else:
            return ""

    @property
    def email(self) -> str:
        if "email" in self._company:
            return self._company["email"]
        else:
            return ""

    @property
    def name(self) -> str:
        if "name" in self._company:
            return self._company["name"]
        else:
            return ""

    @property
    def phone(self) -> str:
        if "phone" in self._company:
            return self._company["phone"]
        else:
            return ""

    @property
    def sender_address(self) -> str:
        if "sender_address" in self._company:
            return self._company["sender_address"]
        else:
            return ""

    @property
    def shipping_note(self) -> str:
        if "shipping_note" in self._company:
            return self._company["shipping_note"]
        else:
            return ""

    @property
    def is_foreign(self) -> bool:
        return self.country != HOME_COUNTRY

    def delete(self):
        all_companies = Company.get_companies()
        index = -1
        for com in all_companies["companies"]:
            index += 1
            if com["name"] == self.name:
                break
        if index < 0:
            return
        all_companies["companies"].pop(index)
        Company._write_json_to_disk(all_companies)

    @staticmethod
    def _get_company_data_file_path() -> str:
        return os.path.join(DATA_DIR_PATH + Company._COMPANY_FILE)

    @staticmethod
    def _write_json_to_disk(data: {}):
        with open(Company._get_company_data_file_path(), "w") as f:
            json.dump(data, f)
