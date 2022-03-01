""" Façade update module """
from update import crypto_update, currency_update, stock_update
from util import backup

class UpdateFacade():
    """ Façade update class """
    def __init__(self):
        self._executed = False

    def execute(self):
        """ Executes all updates """
        if self._executed:
            return

        backup.execute()
        currency_update.execute(run_backup=False)
        stock_update.execute(run_backup=False)
        crypto_update.execute(run_backup=False)
        # Commodities are not updated because it is slow.
        # Update commodities via menu if needed

        self._executed = True


class UpdateFacadeFactory():
    """ Façade update factory class """
    _SINGLETON: UpdateFacade = None

    @staticmethod
    def get_instance() -> UpdateFacade:
        """ Singleton design pattern """
        if UpdateFacadeFactory._SINGLETON is None:
            UpdateFacadeFactory._SINGLETON = UpdateFacade()
        return UpdateFacadeFactory._SINGLETON
