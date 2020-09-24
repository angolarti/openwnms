import time
from ipaddress import ip_address


def convert_int_to_time(time_int: int) -> str:
    return time.strftime('%H:%M:%S', time.gmtime(time_int))


def is_ip_address(ip_addr: str) -> bool:
    try:
        return ip_address(ip_addr) is not None
    except ValueError:
        return False


def convert_units(num: int):
    """
    this function will convert bytes to MB.... GB... etc
    """
    step_unit = 1024.0  # 1024 bad the size

    for unit in ['KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.2f %s" % (num, unit)
        num /= step_unit
