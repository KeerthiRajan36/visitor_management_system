import re
from datetime import time


def validate_phone(phone: str):

    pattern = r"^[6-9]\d{9}$"

    return re.match(
        pattern,
        phone
    ) is not None


def validate_checkout(
        check_in: time,
        check_out: time
):

    if check_in is None or check_out is None:
        return True

    return check_out > check_in