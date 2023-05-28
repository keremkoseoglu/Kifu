""" Flask web server module """
from threading import Thread
import webbrowser
import json
from flask import Flask, jsonify, request
from waitress import serve
import config
from update.update_facade import UpdateFacadeFactory
from web.api.net_worth import NetWorthAPI
from web.api.iban_list import IbanListAPI
from web.api.income_tax_rates import IncomeTaxRatesAPI
from web.api.activity_list import ActivityListAPI
from web.api.address_book import AddressBookAPI
from web.api.asset_profit import AssetProfitAPI
from web.api.asset_value import AssetValueAPI
from web.api.budget import BudgetAPI
from web.api.curr_acc_dist import CurrAccDistAPI
from web.api.ecz_activity_comparison import EczActivityComparisonAPI
from web.api.payment_status import PaymentStatusAPI
from web.api.reconciliation import ReconciliationAPI
from web.api.workdays_wo_activity import WorkdaysWoActivityAPI
from web.api.bank_account_balances import BankAccountBalanceAPI

##############################
# Main stuff
##############################

_APP = Flask(__name__)
_APP.secret_key = "kifu"
_APP.config["CACHE_TYPE"] = "null"
_APP.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
_APP.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

_WEB_RUNNING = False


def run_web_server():
    """Starts the web server"""
    serve(_APP, port=config.CONSTANTS["WEB_PORT"])


def run_web_server_new_thread():
    """Starts the web server in a new thread"""
    global _WEB_RUNNING
    if _WEB_RUNNING:
        return
    _WEB_RUNNING = True
    Thread(target=run_web_server, daemon=True).start()


def build_url(suffix: str, query_string: str = None) -> str:
    """Builds an URL"""
    result = "http://"
    result += config.CONSTANTS["WEB_HOST"]
    result += ":" + str(config.CONSTANTS["WEB_PORT"])
    result += "/static/" + suffix + "/index.html"
    if query_string is not None:
        result += "?" + query_string
    return result


def startup_url(suffix: str, query_string: str = None):
    """Runs web server and starts an URL"""
    run_web_server_new_thread()
    if config.CONSTANTS["UPDATE_ON_REPORT"]:
        UpdateFacadeFactory().get_instance().execute()
    url = build_url(suffix, query_string=query_string)
    webbrowser.open(url)


##############################
# Pages
##############################


@_APP.route("/test")
def _test():
    return _APP.send_static_file("test.html")


##############################
# API
##############################


@_APP.route("/api/net_worth")
def _api_net_worth():
    return jsonify(NetWorthAPI().result)


@_APP.route("/api/iban_list")
def _api_iban():
    return jsonify(IbanListAPI().result)


@_APP.route("/api/activity_list")
def _api_activity_list():
    return jsonify(ActivityListAPI().entire_dataset)


@_APP.route("/api/address_book")
def _api_address_book():
    name = request.args.get("name")
    if name is None or name == "":
        names = None
    else:
        names = [name]
    return jsonify(AddressBookAPI.get_result(listable_companies=names))


@_APP.route("/api/asset_profit")
def _api_asset_profit():
    return jsonify(AssetProfitAPI().result)


@_APP.route("/api/asset_commodity_values_get")
def _api_asset_commodity_values_get():
    return jsonify(AssetValueAPI.get_commodity_values())


@_APP.route("/api/asset_commodity_values_set", methods=["POST"])
def _api_asset_commodity_values_set():
    entries = request.get_json()
    AssetValueAPI.set_commodity_values(entries)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@_APP.route("/api/curr_acc_dist")
def _api_curr_acc_dist():
    return jsonify(CurrAccDistAPI().result)


@_APP.route("/api/ecz_activity_comparison")
def _api_ecz_activity_comparison():
    return jsonify(EczActivityComparisonAPI().result)


@_APP.route("/api/payment_status")
def _api_payment_status():
    guid = request.args.get("guid")
    return jsonify(PaymentStatusAPI().get_result(guid))


@_APP.route("/api/reconciliation")
def _api_reconciliation():
    names = request.args.get("names")
    names_list = names.split(",")
    return jsonify(ReconciliationAPI().get_result(names_list))


@_APP.route("/api/workdays_wo_activity")
def _api_workdays_wo_activity():
    return jsonify(WorkdaysWoActivityAPI().result)


@_APP.route("/api/income_tax_rates")
def _api_income_tax_rates():
    return jsonify(IncomeTaxRatesAPI().result)


@_APP.route("/api/budget_domains")
def _api_budget_domains():
    return jsonify(BudgetAPI().domains)


@_APP.route("/api/budget_subjects")
def _api_budget_subjects():
    return jsonify(BudgetAPI().subjects)


@_APP.route("/api/budget_domains_and_subjects")
def _api_budget_domains_and_subjects():
    return jsonify(BudgetAPI().domain_and_subjects)


@_APP.route("/api/budget_plan")
def _api_budget_plan():
    return jsonify(BudgetAPI().plan)


@_APP.route("/api/budget_plan_vs_actual")
def _api_budget_plan_vs_actual():
    return jsonify(BudgetAPI().plan_vs_actual)


@_APP.route("/api/salary_simulation")
def _api_salary_simulation():
    return jsonify(BudgetAPI().salary_simulation)


@_APP.route("/api/akbank_statement")
def _api_akbank_statement():
    return jsonify(BudgetAPI().akbank_statement)


@_APP.route("/api/akbank_statement_sum")
def _api_akbank_statement_sum():
    return jsonify(BudgetAPI().akbank_statement_sum)


@_APP.route("/api/akbank_statement_actual_save", methods=["POST"])
def _api_akbank_statement_actual_save():
    entries = request.get_json()
    BudgetAPI.save_akbank_statement_actuals(entries["statement"])
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@_APP.route("/api/bank_account_balances")
def _api_bank_account_balances():
    return jsonify(BankAccountBalanceAPI().result)
