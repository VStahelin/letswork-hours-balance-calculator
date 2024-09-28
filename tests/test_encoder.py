import pytest
from datetime import datetime, time, timedelta

from extractor import encoder


def test_encoder_time():
    assert encoder(time(10, 30)) == "10h30m"


def test_encoder_datetime():
    dt = datetime(2024, 9, 28)
    assert encoder(dt) == "28/09/2024"


def test_encoder_timedelta():
    td = timedelta(hours=2, minutes=15)
    assert encoder(td) == "02h15m"


def test_encoder_invalid_type():
    with pytest.raises(TypeError):
        encoder({"invalid": "object"})
