import uuid


def get_guid() -> str:
    return uuid.uuid4().hex