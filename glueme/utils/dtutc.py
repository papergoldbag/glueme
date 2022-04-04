from datetime import datetime

import pytz


def dt_to_utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=None).astimezone(pytz.UTC).replace(tzinfo=None)


def utc_to_local(utc_dt: datetime, to_timezone: pytz.timezone) -> datetime:
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(to_timezone)
