""" Company module """
import json
import os
from typing import List
from config.constants import DATA_DIR_PATH, HOME_COUNTRY


class Company:
    """ Company class """
    _COMPANY_FILE = "company.json"

    @staticmethod
    def get_companies():
        """ Returns a dictionary of companies """
        with open(Company._get_company_data_file_path()) as company_file:
            json_data = json.load(company_file)
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
        """ Returns company address """
        return self._get_string_from_dict("address")

    @property
    def contact_person(self) -> str:
        """ Returns contact person address """
        return self._get_string_from_dict("contact_person")

    @property
    def country(self) -> str:
        """ Returns company country """
        return self._get_string_from_dict("country")

    @property
    def email(self) -> str:
        """ Returns company email """
        return self._get_string_from_dict("email")

    @property
    def ibans(self) -> List[str]:
        """ Returns company iban list """
        return self._get_list_from_dict("ibans")

    @property
    def is_foreign(self) -> bool:
        """ Returns if the company belongs to the home company country or not """
        return self.country != HOME_COUNTRY

    @property
    def locations(self) -> List[str]:
        """ Returns company location list """
        return self._get_list_from_dict("locations")

    @property
    def name(self) -> str:
        """ Returns company name """
        return self._get_string_from_dict("name")

    @property
    def phone(self) -> str:
        """ Returns company phone """
        return self._get_string_from_dict("phone")

    @property
    def sender_address(self) -> str:
        """ Returns company sender address
        Typically, this method will only return a value for the home company
        """
        return self._get_string_from_dict("sender_address")

    @property
    def shipping_note(self) -> str:
        """ Returns company shipping note
        Typically, this method will only return a value for the home company
        """
        return self._get_string_from_dict("shipping_note")

    @property
    def tax_info(self) -> tuple:
        """ Returns tax info as tuple
        Format: tax_number, tax_office
        """
        tax_number = ""
        tax_office = ""
        if "tax_number" in self._company:
            tax_number = self._company["tax_number"]
        if "tax_office" in self._company:
            tax_office = self._company["tax_office"]
        return tax_number, tax_office

    def delete(self):
        """ Deletes the company from the JSON file """
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
        with open(Company._get_company_data_file_path(), "w") as json_file:
            json.dump(data, json_file)

    def _get_list_from_dict(self, key: str) -> List[str]:
        if key in self._company:
            return self._company[key]
        return []

    def _get_string_from_dict(self, key: str) -> str:
        if key in self._company:
            return self._company[key]
        return ""
