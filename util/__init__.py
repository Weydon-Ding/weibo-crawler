import datetime


def is_date(since_date):
    """判断日期格式是否为 %Y-%m-%d"""
    try:
        datetime.strptime(since_date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_datetime(since_date):
    """判断日期格式是否为 %Y-%m-%dT%H:%M:%S"""
    try:
        datetime.strptime(since_date, "%Y-%m-%dT%H:%M:%S")
        return True
    except ValueError:
        return False
