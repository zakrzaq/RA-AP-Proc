from datetime import date, datetime


def today_ymd(sep="/"):
    today = date.today()
    return today.strftime(f"%Y{sep}%m{sep}%d")


def today_dmy(sep="/"):
    today = date.today()
    return today.strftime(f"%d{sep}%m{sep}%Y")


def today_mdy(sep="/"):
    today = date.today()
    return today.strftime(f"%m{sep}%d{sep}%Y")


def mif_date():
    now = datetime.now()
    return now.strftime("%m%d%Y_%H%M%S")
