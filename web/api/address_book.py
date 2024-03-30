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
            comp_obj = Company(comp["name"])
            comp["address"] = comp_obj.address
            comp["phone"] = comp_obj.phone
            comp["email"] = comp_obj.email
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
            if "tax_number" in comp:
                comp["tax_number"] = comp["tax_number"].replace(" ", "")
        return result
