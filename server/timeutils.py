from datetime import datetime
import time

import pytz


def get_datetimenow_with_server_timezone():
    """Get `datetime.now()` with matching timezone.

    As `.now()` is taken from system clock, we need to add system timezone
    before we can any operations on it.

    """
    dt_no_tz = datetime.now()
    tz = pytz.timezone(time.tzname[0])
    dt_w_tz = dt_no_tz.replace(tzinfo=tz)
    return dt_w_tz