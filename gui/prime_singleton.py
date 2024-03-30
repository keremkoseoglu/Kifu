""" Singleton prime instance """

class PrimeSingleton:
    """ Singleton primary window instance """
    _PRIME = None

    @staticmethod
    def get():
        """ Returns singleton instance """
        return PrimeSingleton._PRIME

    @staticmethod
    def set(prime):
        """ Sets singleton instance """
        PrimeSingleton._PRIME = prime
