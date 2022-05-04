""" Amount utilities """

def get_formatted_amount(amount: float) -> str:
    """ Returns a formatted amount """
    return "{:0,.2f}".format(amount) #pylint: disable=C0209
