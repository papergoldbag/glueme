from datetime import datetime

import pytz


def dt_to_utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=None).astimezone(pytz.UTC).replace(tzinfo=None)


