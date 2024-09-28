from datetime import datetime, time
import pytest
from extractor import extractor


@pytest.fixture
def mock_html(tmp_path):
    html_content = """
    <div class="panel panel-success">
        <div class="timeline-wrapper">
            <div class="timeline-date clearfix">25/09/2024</div>
            <div class="timeline-item clearfix"><div class="time">18:00</div></div>
            <div class="timeline-item clearfix"><div class="time">09:00</div></div>
        </div>
    </div>
    """
    file_path = tmp_path / "test.html"
    file_path.write_text(html_content)
    return file_path


def test_extractor(mock_html):
    checks = extractor(mock_html)
    assert len(checks) == 1
    assert checks[0].date == datetime(2024, 9, 25)
    assert checks[0].check_in == time(9, 0)
    assert checks[0].check_out == time(18, 0)


def test_extractor_invalid_date_format(tmp_path):
    html_content = """
    <div class="panel panel-success">
        <div class="timeline-wrapper">
            <div class="timeline-date clearfix">25-09-2024</div>
            <div class="timeline-item clearfix"><div class="time">1811:00</div></div>
            <div class="timeline-item clearfix"><div class="time">09:00</div></div>
        </div>
    </div>
    """
    file_path = tmp_path / "test.html"
    file_path.write_text(html_content)

    with pytest.raises(
        ValueError, match="time data '1811:00' does not match format '%H:%M'"
    ):
        extractor(file_path)
