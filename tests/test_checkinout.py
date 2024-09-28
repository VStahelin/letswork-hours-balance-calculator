from datetime import datetime, time, timedelta

from constants import WORK_JOURNEY
from extractor import CheckInOut


def test_check_in_out_working_hours():
    check = CheckInOut(
        date=datetime.today(), check_in=time(9, 0), check_out=time(18, 0)
    )
    assert check.working_hours == timedelta(hours=8)


def test_check_in_out_negative_time():
    # WORK_JOURNEY is 8h48m
    # INTERVAL_TIME is 1h

    check = CheckInOut(
        date=datetime.today(), check_in=time(10, 0), check_out=time(19, 0)
    )
    assert check.negative_time == timedelta(minutes=48)


def test_check_in_out_no_check_in_out():
    check = CheckInOut(date=datetime.today())
    assert check.working_hours == timedelta(0)
    assert check.negative_time == timedelta(
        hours=WORK_JOURNEY.hour, minutes=WORK_JOURNEY.minute
    )
