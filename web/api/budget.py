""" Budget API """
from model import budget
from model import akbank

class BudgetAPI():
    """ Budget API """

    _FORMAT_FIELDS = ["monthly_plan_amount",
                      "annual_plan_amount",
                      "avg_monthly_actual",
                      "monthly_remain_budget",
                      "annual_remain_budget",
                      "actual_sum",
                      "jan_actual",
                      "feb_actual",
                      "mar_actual",
                      "apr_actual",
                      "may_actual",
                      "jun_actual",
                      "jul_actual",
                      "aug_actual",
                      "sep_actual",
                      "oct_actual",
                      "nov_actual",
                      "dec_actual"]

    @property
    def domains(self) -> {}:
        """ Budget domains """
        return budget.get_domain_dict()

    @property
    def subjects(self) -> []:
        """ Subjects """
        return budget.get_subject_list()

    @property
    def domain_and_subjects(self) -> {}:
        """ Domain and subjects in same dataset """
        return budget.get_domain_and_subject_dict()

    @property
    def plan(self) -> {}:
        """ Budget plan values """
        out = budget.get_plan_list_and_sums_flat()
        BudgetAPI._format_plan(out)
        return out

    @property
    def plan_vs_actual(self) -> {}:
        """ Plan vs actual """
        out = budget.get_plan_vs_actual_list_and_sums_flat()
        BudgetAPI._format_plan(out["plan_vs_actuals"])
        return out

    @property
    def salary_simulation(self) -> {}:
        """ Salary simulation """
        out = budget.get_salary_simulation_and_sum_flat()
        BudgetAPI._format_plan(out)
        return out

    @property
    def akbank_statement(self) -> []:
        """ Akbank statements """
        out = akbank.StatementReader().read_as_list()
        out.sort(key=lambda x: x["text"])
        return out

    @property
    def akbank_statement_sum(self) -> []:
        """ Akbank statement sum """
        statement = akbank.StatementReader().read_as_sum_list()
        statement.sort(key=lambda x: x["text"])

        subjects = budget.get_subject_list_combo()

        out = {"statement": statement,
               "subjects": subjects}

        return out

    @staticmethod
    def save_akbank_statement_actuals(actuals: []):
        """ Save Akbank statement actuals """
        budget.save_actuals_with_subject_list_combo(actuals)

    @staticmethod
    def _format_plan(plan: []):
        for entry in plan:
            for field in BudgetAPI._FORMAT_FIELDS:
                if field not in entry:
                    continue
                entry[field] = int(entry[field])
                if entry["direction"] == "expenses":
                    entry[field] *= -1
            if "actuals" in entry:
                for actual in entry["actuals"]:
                    actual["amount"] = int(actual["amount"])
                    if entry["direction"] == "expenses":
                        actual["amount"] *= -1
