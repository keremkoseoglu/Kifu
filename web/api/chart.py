""" Chart helper """
from random import randint

_COLORS = "1234567890ABCDEF"

def _get_random_color() -> str:
    result = "#"
    while len(result) < 7:
        pos = randint(0, len(_COLORS)-1)
        col = _COLORS[pos:pos+1]
        result += col
    return result

def get_pie_dict(entries: [], label_fld: str, val_fld: str) -> dict:
    """ Returns dict for pie chart """
    out = {
        "labels": [],
        "datasets": [
            {
                "data": [],
                "backgroundColor": [],
                "hoverBackgroundColor":[]
            }
        ]
    }

    sorted_entries = sorted(entries, key=lambda x: x[val_fld], reverse=True)

    for entry in sorted_entries:
        out["labels"].append(entry[label_fld])
        out["datasets"][0]["data"].append(entry[val_fld])
        out["datasets"][0]["backgroundColor"].append(_get_random_color())
        out["datasets"][0]["hoverBackgroundColor"].append(_get_random_color())

    return out
