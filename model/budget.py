""" Budget module """
import json
from os import path, listdir
from copy import deepcopy
from datetime import datetime
import config
from model.currency import CurrencyConverter

_DOMAIN_FILE = "budget_domain.json"
_FISCAL_FILE_PREFIX = "budget_fy_"
_INCOME_ICON = "➕"
_EXPENSE_ICON = "➖"
_RED_ICON = "🔴"
_YELLOW_ICON = "🟡"
_GREEN_ICON = "🟢"
_SUM_DOMAIN = "∑"
_MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

def get_domain_dict() -> dict:
    """ Returns domain dict """
    with open(_get_domain_file_path()) as domain_file:
        out = json.load(domain_file)
    return out

def get_subject_list() -> []:
    """ Subjects """
    global _INCOME_ICON, _EXPENSE_ICON

    out = []
    domain_dict = get_domain_dict()
    for domain in domain_dict["domains"]:
        for income in domain["incomes"]:
            is_salary = "salaries" in domain and income in domain["salaries"]

            inc_dict = {"domain": domain["name"],
                        "direction": "incomes",
                        "subject": income,
                        "icon": _INCOME_ICON,
                        "is_salary": is_salary}

            out.append(inc_dict)

        for expense in domain["expenses"]:
            is_salary = "salaries" in domain and expense in domain["salaries"]

            exp_dict = {"domain": domain["name"],
                        "direction": "expenses",
                        "subject": expense,
                        "icon": _EXPENSE_ICON,
                        "is_salary": is_salary}
            out.append(exp_dict)
    return out

def get_subject_list_combo() -> []:
    """ Returns subject list suitable for combobox """
    out = []
    subjects = get_subject_list()
    subjects.sort(key=lambda x: x["direction"])
    for subject in subjects:
        entry_val = "[" + subject["direction"][0:1] + "]"
        entry_val += " " + subject["domain"]
        entry_val += " - " + subject["subject"]
        entry = {"name": entry_val, "value": entry_val}
        out.append(entry)
    return out

def get_domain_and_subject_dict() -> {}:
    """ Domain and subjects in same dataset """
    return {"domains": get_domain_dict()["domains"],
            "subjects": get_subject_list()}

def get_plan_list() -> []:
    """ Plan values """
    conv = CurrencyConverter()
    out = get_subject_list()
    fiscal = _get_latest_fiscal_file_content()
    for subject in out:
        subject["monthly_plan_amount"] = 0
        subject["annual_plan_amount"] = 0
        subject["currency"] = config.CONSTANTS["HOME_CURRENCY"]
        subject["currency_symbol"] = config.CONSTANTS["HOME_CURRENCY_SYMBOL"]

        if "plans" in fiscal:
            for plan in fiscal["plans"]:
                if subject["domain"] == plan["domain"] and subject["subject"] == plan["subject"]:
                    json_amount = conv.convert_to_local_currency(plan["amount"], plan["currency"])
                    if plan["period"] == "month":
                        monthly_amount = json_amount / plan["frequency"]
                        annual_amount = json_amount * (12 / plan["frequency"])
                    elif plan["period"] == "year":
                        monthly_amount = json_amount / (12 * plan["frequency"])
                        annual_amount = json_amount / plan["frequency"]
                    else:
                        raise Exception("Unknown budget period: " + plan["period"])
                    subject["monthly_plan_amount"] = monthly_amount
                    subject["annual_plan_amount"] = annual_amount
                    break

    return out

def get_plan_vs_actual_list() -> []:
    """ Plan vs actual """
    global _GREEN_ICON
    conv = CurrencyConverter()
    out = get_plan_list()
    fiscal = _get_latest_fiscal_file_content()

    for subject in out:
        subject["actuals"] = [{"month": 1, "amount": 0, "status_icon": _GREEN_ICON},
                              {"month": 2, "amount": 0, "status_icon": _GREEN_ICON},
                              {"month": 3, "amount": 0, "status_icon": _GREEN_ICON},
                              {"month": 4, "amount": 0, "status_icon": _GREEN_ICON},
                              {"month": 5, "amount": 0, "status_icon": _GREEN_ICON},
                              {"month": 6, "amount": 0, "status_icon": _GREEN_ICON},
                              {"month": 7, "amount": 0, "status_icon": _GREEN_ICON},
                              {"month": 8, "amount": 0, "status_icon": _GREEN_ICON},
                              {"month": 9, "amount": 0, "status_icon": _GREEN_ICON},
                              {"month": 10, "amount": 0, "status_icon": _GREEN_ICON},
                              {"month": 11, "amount": 0, "status_icon": _GREEN_ICON},
                              {"month": 12, "amount": 0, "status_icon": _GREEN_ICON}]

        for actual_months in fiscal["actuals"]:
            for actual in actual_months["values"]:
                if actual["domain"] != subject["domain"]:
                    continue
                if actual["subject"] != subject["subject"]:
                    continue
                if actual["direction"] != subject["direction"]:
                    continue

                local_amount = conv.convert_to_local_currency(actual["amount"],
                                                              actual["currency"])

                for out_actual in subject["actuals"]:
                    if out_actual["month"] == actual_months["month"]:
                        out_actual["amount"] += local_amount
                        out_actual["status_icon"] = _get_status_icon(subject["monthly_plan_amount"],
                                                                     out_actual["amount"],
                                                                     subject["direction"])
                        break

    return out

def get_plan_list_and_sums() -> dict:
    """ Returns plan with sums """
    out = {"plans": get_plan_list(),
           "sum": {"monthly_income": 0,
                   "monthly_expense": 0,
                   "monthly_balance": 0,
                   "annual_income": 0,
                   "annual_expense": 0,
                   "annual_balance": 0,
                   "currency": config.CONSTANTS["HOME_CURRENCY"],
                   "currency_symbol": config.CONSTANTS["HOME_CURRENCY_SYMBOL"]}}

    for plan in out["plans"]:
        if plan["direction"] == "incomes":
            out["sum"]["monthly_income"] += plan["monthly_plan_amount"]
            out["sum"]["monthly_balance"] += plan["monthly_plan_amount"]
            out["sum"]["annual_income"] += plan["annual_plan_amount"]
            out["sum"]["annual_balance"] += plan["annual_plan_amount"]
        elif plan["direction"] == "expenses":
            out["sum"]["monthly_expense"] += plan["monthly_plan_amount"]
            out["sum"]["monthly_balance"] -= plan["monthly_plan_amount"]
            out["sum"]["annual_expense"] += plan["annual_plan_amount"]
            out["sum"]["annual_balance"] -= plan["annual_plan_amount"]
        else:
            raise Exception("Unknown budget direction: " + plan["direction"])

    return out

def get_plan_vs_actual_list_and_sums() -> dict:
    """ Plan vs actual with sums """
    global _MONTHS

    out = {"plan_vs_actuals": get_plan_vs_actual_list(),
           "plan_sum": {},
           "actual_sum": {"annual_income": 0,
                          "annual_expense": 0,
                          "annual_balance": 0,
                          "avg_monthly_income": 0,
                          "avg_monthly_expense": 0,
                          "avg_monthly_balance": 0,
                          "currency": config.CONSTANTS["HOME_CURRENCY"],
                          "currency_symbol": config.CONSTANTS["HOME_CURRENCY_SYMBOL"]}}

    for pva in out["plan_vs_actuals"]:
        for act in pva["actuals"]:
            month_idx = act["month"] - 1
            month_fld = _MONTHS[month_idx]
            month_fld += "_actual"
            pva[month_fld] = act["amount"]

    pws = get_plan_list_and_sums()
    out["plan_sum"] = pws["sum"]
    latest_month = 0

    for pva in out["plan_vs_actuals"]:
        pva["actual_sum"] = 0
        for actual in pva["actuals"]:
            if actual["amount"] > 0 and actual["month"] > latest_month:
                latest_month = actual["month"]
            pva["actual_sum"] += actual["amount"]
            if pva["direction"] == "incomes":
                out["actual_sum"]["annual_income"] += actual["amount"]
                out["actual_sum"]["annual_balance"] += actual["amount"]
            elif pva["direction"] == "expenses":
                out["actual_sum"]["annual_expense"] += actual["amount"]
                out["actual_sum"]["annual_balance"] -= actual["amount"]
            else:
                raise Exception("Unknown budget direction: " + pva["direction"])
        pva["annual_remain_budget"] = pva["annual_plan_amount"] - pva["actual_sum"]
        month_div = 12 - datetime.today().month + 1
        pva["monthly_remain_budget"] = pva["annual_remain_budget"] / month_div

    for pva in out["plan_vs_actuals"]:
        if latest_month == 0:
            pva["avg_monthly_actual"] = 0
        else:
            pva["avg_monthly_actual"] = pva["actual_sum"] / latest_month

        pva["monthly_delta"] = pva["monthly_plan_amount"] - pva["avg_monthly_actual"]
        pva["monthly_delta_icon"] = _get_status_icon(pva["monthly_plan_amount"],
                                                     pva["avg_monthly_actual"],
                                                     pva["direction"])

        if pva["direction"] == "incomes":
            out["actual_sum"]["avg_monthly_income"] += pva["avg_monthly_actual"]
            out["actual_sum"]["avg_monthly_balance"] += pva["avg_monthly_actual"]
        elif pva["direction"] == "expenses":
            out["actual_sum"]["avg_monthly_expense"] += pva["avg_monthly_actual"]
            out["actual_sum"]["avg_monthly_balance"] -= pva["avg_monthly_actual"]
        else:
            raise Exception("Unknown budget direction: " + pva["direction"])

    out["delta"] = {
        "annual_income": out["plan_sum"]["annual_income"] - out["actual_sum"]["annual_income"],
        "annual_expense": out["plan_sum"]["annual_expense"] - out["actual_sum"]["annual_expense"],
        "avg_monthly_income": out["plan_sum"]["monthly_income"] - out["actual_sum"]["avg_monthly_income"], # pylint: disable = C0301
        "avg_monthly_expense": out["plan_sum"]["monthly_expense"] - out["actual_sum"]["avg_monthly_expense"], # pylint: disable = C0301
        "currency": config.CONSTANTS["HOME_CURRENCY"],
        "currency_symbol": config.CONSTANTS["HOME_CURRENCY_SYMBOL"]}

    out["delta"]["annual_balance"] = out["delta"]["annual_income"] - out["delta"]["annual_expense"]
    out["delta"]["avg_monthly_balance"] = out["delta"]["avg_monthly_income"] - out["delta"]["avg_monthly_expense"] # pylint: disable = C0301

    return out

def get_plan_list_and_sums_flat() -> []:
    """ Returns plan + sums, but shows sums as a plan category """
    global _SUM_DOMAIN
    pws = get_plan_list_and_sums()
    out = pws["plans"]

    out.append({"domain": _SUM_DOMAIN,
                "direction": "incomes",
                "subject": "incomes",
                "icon": _INCOME_ICON,
                "monthly_plan_amount": pws["sum"]["monthly_income"],
                "annual_plan_amount": pws["sum"]["annual_income"],
                "currency": config.CONSTANTS["HOME_CURRENCY"],
                "currency_symbol": config.CONSTANTS["HOME_CURRENCY_SYMBOL"]})

    out.append({"domain": _SUM_DOMAIN,
                "direction": "expenses",
                "subject": "expenses",
                "icon": _INCOME_ICON,
                "monthly_plan_amount": pws["sum"]["monthly_expense"],
                "annual_plan_amount": pws["sum"]["annual_expense"],
                "currency": config.CONSTANTS["HOME_CURRENCY"],
                "currency_symbol": config.CONSTANTS["HOME_CURRENCY_SYMBOL"]})

    out.append({"domain": _SUM_DOMAIN,
                "direction": "incomes",
                "subject": "BALANCE",
                "icon": _INCOME_ICON,
                "monthly_plan_amount": pws["sum"]["monthly_balance"],
                "annual_plan_amount": pws["sum"]["annual_balance"],
                "currency": config.CONSTANTS["HOME_CURRENCY"],
                "currency_symbol": config.CONSTANTS["HOME_CURRENCY_SYMBOL"]})

    return out

def get_plan_vs_actual_list_and_sums_flat() -> dict:
    """ Returns with an additional sum line """
    global _GREEN_ICON, _INCOME_ICON
    out = get_plan_vs_actual_list_and_sums()

    pva_sum = {}

    for pva in out["plan_vs_actuals"]:
        if pva_sum == {}:
            pva_sum = deepcopy(pva)
            pva_sum["domain"] = "SUM"
            pva_sum["subject"] = ""
            pva_sum["direction"] = "incomes"
            pva_sum["icon"] = _INCOME_ICON

            if pva["direction"] == "expenses":
                for field in pva:
                    if isinstance(pva[field], int) or isinstance(pva[field], float): # pylint: disable=R1701
                        pva_sum[field] *= -1
                actual_pos = -1
                for actual in pva["actuals"]:
                    pva_sum["actuals"][actual_pos]["amount"] *= -1

        else:
            for field in pva:
                if isinstance(pva[field], int) or isinstance(pva[field], float): # pylint: disable=R1701
                    if pva["direction"] == "incomes":
                        pva_sum[field] += pva[field]
                    elif pva["direction"] == "expenses":
                        pva_sum[field] -= pva[field]
                    else:
                        raise Exception("Unknown direction: " + pva["direction"])
            actual_pos = -1
            for actual in pva["actuals"]:
                actual_pos += 1
                if pva["direction"] == "incomes":
                    pva_sum["actuals"][actual_pos]["amount"] += actual["amount"]
                elif pva["direction"] == "expenses":
                    pva_sum["actuals"][actual_pos]["amount"] -= actual["amount"]
                else:
                    raise Exception("Unknown direction: " + pva["direction"])

    if pva_sum != {}:
        pva_sum["monthly_delta_icon"] = _get_status_icon(pva_sum["monthly_plan_amount"],
                                                         pva_sum["avg_monthly_actual"],
                                                         pva_sum["direction"])

        for act in pva_sum["actuals"]:
            act["status_icon"] = _get_status_icon(pva_sum["monthly_plan_amount"],
                                                  act["amount"],
                                                  pva_sum["direction"])

        out["plan_vs_actuals"].append(pva_sum)

    return out

def get_salary_simulation() -> []:
    """ Simulate salary """
    out = {"plan": [],
           "sum": {"monthly": 0,
                   "annual": 0,
                   "currency": config.CONSTANTS["HOME_CURRENCY"],
                   "currency_symbol": config.CONSTANTS["HOME_CURRENCY_SYMBOL"]}}

    plans = get_plan_list()

    for plan in plans:
        if not plan["is_salary"]:
            continue

        out["plan"].append(plan)

        if plan["direction"] == "incomes":
            out["sum"]["monthly"] += plan["monthly_plan_amount"]
            out["sum"]["annual"] += plan["annual_plan_amount"]
        elif plan["direction"] == "expenses":
            out["sum"]["monthly"] -= plan["monthly_plan_amount"]
            out["sum"]["annual"] -= plan["annual_plan_amount"]
        else:
            raise Exception("Unknown direction: " + plan["direction"])

    return out

def get_salary_simulation_and_sum_flat() -> []:
    """ Salary simulation and sum """
    simulation = get_salary_simulation()
    out = simulation["plan"]
    out.append({"domain": _SUM_DOMAIN,
                "direction": "incomes",
                "subject": "SALARY",
                "icon": _INCOME_ICON,
                "monthly_plan_amount": simulation["sum"]["monthly"],
                "annual_plan_amount": simulation["sum"]["annual"],
                "currency": config.CONSTANTS["HOME_CURRENCY"],
                "currency_symbol": config.CONSTANTS["HOME_CURRENCY_SYMBOL"]})
    return out

def save_actuals_with_subject_list_combo(actuals: []):
    """ Save actuals """
    month_values = []
    for actual in actuals:
        if "value" not in actual:
            continue
        if actual["value"].strip() == "":
            continue
        frags = actual["value"].split(" ") # [e] car - gas

        direction_letter = frags[0][1:2]
        if direction_letter == "i":
            direction = "incomes"
        elif direction_letter == "e":
            direction = "expenses"
        else:
            raise Exception("Unknown direction: " + direction_letter)

        month_entry = {"domain": frags[1],
                       "direction": direction,
                       "subject": frags[3],
                       "amount": actual["amount"],
                       "currency": actual["currency"]}
        month_values.append(month_entry)

    month = datetime.now().month - 1
    if month == 0:
        month = 12

    fiscal_file_dict = _get_latest_fiscal_file_content()

    for fiscal_file_act in fiscal_file_dict["actuals"]:
        if fiscal_file_act["month"] != month:
            continue
        fiscal_file_act["values"] = month_values
        break

    fiscal_file_name = _get_latest_fiscal_file()
    fiscal_path = path.join(config.CONSTANTS["DATA_DIR_PATH"] + fiscal_file_name)
    with open(fiscal_path, "w") as fiscal_file:
        fiscal_file.write(json.dumps(fiscal_file_dict, indent=4))

def migrate_from_excel():
    """ Reads old Excel file and writes into budget
    This method is planned to be executed only once.
    Therefore, it contains lots of hard coded values
    """
    excel = []
    with open('/Users/kerem/Downloads/tmp_budget.csv') as budget_file:
        excel = budget_file.read().splitlines()

    subject_defs = get_subject_list()
    fiscal_file_dict = _get_latest_fiscal_file_content()

    for excel_line in excel:
        excel_cols = excel_line.split(";")
        domain = str(excel_cols[0]).lower().replace("\ufeff", "")
        subject = str(excel_cols[1]).lower()
        direction = ""

        for subject_def in subject_defs:
            if subject_def["domain"] == domain and subject_def["subject"] == subject:
                direction = subject_def["direction"]
                break

        if direction == "":
            raise Exception("Unknown subject")

        for i in range(0, 4):
            excel_value = abs(float(excel_cols[i+2]))
            month = i + 1
            for fiscal_act in fiscal_file_dict["actuals"]:
                if fiscal_act["month"] != month:
                    continue
                value_dict = {"domain": domain,
                              "direction": direction,
                              "subject": subject,
                              "amount": excel_value,
                              "currency": "TRY"}
                fiscal_act["values"].append(value_dict)
                break

    fiscal_file_name = _get_latest_fiscal_file()
    fiscal_path = path.join(config.CONSTANTS["DATA_DIR_PATH"] + fiscal_file_name)
    with open(fiscal_path, "w") as fiscal_file:
        fiscal_file.write(json.dumps(fiscal_file_dict, indent=4))


def _get_domain_file_path() -> str:
    return path.join(config.CONSTANTS["DATA_DIR_PATH"] + _DOMAIN_FILE)

def _get_latest_fiscal_file() -> str:
    global _FISCAL_FILE_PREFIX
    out = ""

    cdir = config.CONSTANTS["DATA_DIR_PATH"]
    fiscal_files = [f for f in listdir(cdir) if f.startswith(_FISCAL_FILE_PREFIX)]

    if fiscal_files is None or len(fiscal_files) <= 0:
        return out

    max_year = 0
    prefix_len = len(_FISCAL_FILE_PREFIX)
    for fiscal_file in fiscal_files:
        year = int(fiscal_file[prefix_len:prefix_len+4])
        if year > max_year:
            year = max_year
            out = fiscal_file

    return out

def _get_latest_fiscal_file_content() -> dict:
    out = {}
    latest_file = _get_latest_fiscal_file()
    if latest_file != "":
        fiscal_path = path.join(config.CONSTANTS["DATA_DIR_PATH"] + latest_file)
        with open(fiscal_path) as fiscal_file:
            out = json.load(fiscal_file)
    return out

def _get_status_icon(plan: float, actual: float, direction: str) -> str:
    global _GREEN_ICON, _YELLOW_ICON, _RED_ICON
    result = _GREEN_ICON
    diff = plan - actual
    if direction == "expenses" and diff < 0:
        if plan == 0:
            result = _RED_ICON
        else:
            diff_perc = abs((diff / plan) * 100)
            if diff_perc > config.CONSTANTS["BUDGET_EXCEED_RATE"]:
                result = _RED_ICON
            else:
                result = _YELLOW_ICON
    elif direction == "incomes" and diff > 0:
        if plan == 0:
            result = _RED_ICON
        else:
            diff_perc = abs((diff / plan) * 100)
            if diff_perc > config.CONSTANTS["BUDGET_EXCEED_RATE"]:
                result = _RED_ICON
            else:
                result = _YELLOW_ICON
    return result
