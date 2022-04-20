""" Main module """
import sys
import datetime
from gui.prime import Prime
from gui.prime_singleton import PrimeSingleton
from model import payment
from model.activity import Activity
from util import backup, date_time
import config
from update.update_facade import UpdateFacadeFactory

""" TODO #152
ilk geliştirme
    yeni ana sayfa ekranı (prime)
        menü template bul
        sayfayı hazırla
        hemen web servisi başlatıp sayfayı göster
        menü çalışıyor olsun
    mevcut TK ekranlarını buradan çağırabiliyor ol
    mevcut web ekranlarını buradan çağırabiliyor ol
yeni ekranlar
    activity_list
    activity_split
    activity
    asset_list
    asset
    cash_movement
    collection
    credit_card_statement
    invest
    invoce_list
    invoice
    pay_income_tax
    pay_vat
    payment_list
    payment
final
    gui klasörünü sil
    pull request
vazgeçersen
    pywebview uninstall
    branch sil
"""

def startup():
    """ Main startup function """
    config.read_constants()
    backup.clear_old_backups()

    if "-test" in sys.argv:
        config.test_mode()

    payment.generate_high_time_recurrences()

    if config.CONSTANTS["UPDATE_ON_STARTUP"]:
        UpdateFacadeFactory.get_instance().execute()

    add_activity = all([
        date_time.is_working_day(datetime.datetime.now()),
        not Activity.has_activity_for_today()
    ])

    prime = Prime(add_activity=add_activity)
    PrimeSingleton.set(prime)
    prime.start()

if __name__ == "__main__":
    startup()
