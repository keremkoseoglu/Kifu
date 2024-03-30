""" Text toolkit"""

_TR_ARRAY = list("ğĞıİöÖüÜşŞçÇ")
_EN_ARRAY = list("gGiIoOuUsScC")


def replace_turkish_chars(tr_text) -> str:
    """Replaces Turkish characters"""
    result = tr_text

    for turkce, ingilizce in zip(_TR_ARRAY, _EN_ARRAY):
        result = result.replace(turkce, ingilizce)

    return result
