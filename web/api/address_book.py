""" Address book API """
from typing import List
from model.company import Company

class AddressBookAPI():
    """ Address book API """

    @staticmethod
    def get_result(listable_companies: List[str] = None) -> dict:
        """ Address book """
        result = {"companies": []}

        for comp in Company.get_companies()["companies"]:
            if listable_companies is not None and len(listable_companies) > 0:
                if comp["name"] not in listable_companies:
                    continue
            result["companies"].append(comp)

        for comp in result["companies"]:
            if "locations" not in comp:
                comp["locations"] = []
            if "ibans" not in comp:
                comp["ibans"] = []
            if len(comp["ibans"]) > 0:
                comp["default_iban"] = comp["ibans"][0]["name"] + " - " + comp["ibans"][0]["number"]
            else:
                comp["default_iban"] = ""
            if "activity_emails" not in comp:
                comp["activity_emails"] = []
        return result