from datetime import datetime, time, timedelta
from dataclasses import dataclass
import json
from bs4 import BeautifulSoup
import argparse


def encoder(obj):
    if isinstance(obj, (datetime, time)):
        return obj.isoformat()
    elif isinstance(obj, timedelta):
        total_minutes = int(obj.total_seconds() / 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02}h{minutes:02}m"

    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


@dataclass
class CheckInOut:
    date: datetime = None
    check_in: time = None
    check_out: time = None

    @property
    def working_hours(self):
        if self.check_in and self.check_out:
            wh = (
                datetime.combine(datetime.today(), self.check_out)
                - datetime.combine(datetime.today(), self.check_in)
                - timedelta(hours=INTERVAL_TIME.hour, minutes=INTERVAL_TIME.minute)
            )
            return wh
        return timedelta(0)

    @property
    def negative_time(self):
        if self.working_hours < timedelta(
            hours=WORK_JOURNEY.hour, minutes=WORK_JOURNEY.minute
        ):
            return (
                timedelta(hours=WORK_JOURNEY.hour, minutes=WORK_JOURNEY.minute)
                - self.working_hours
            )
        return timedelta(0)

    def to_dict(self):
        return {
            "date": self.date,
            "weekday": self.date.strftime("%A"),
            "check_in": self.check_in,
            "check_out": self.check_out,
            "working_hours": (datetime.min + self.working_hours).time(),
            "negative_time": (datetime.min + self.negative_time).time(),
        }


@dataclass
class MonthWork:
    month: datetime = None
    checks: list[CheckInOut] = None
    last_month_overtime: time = time(0, 0)

    @property
    def total_working_hours(self):
        total_time = timedelta()
        for check in self.checks:
            total_time += check.working_hours
        return total_time

    @property
    def overtime(self):
        total_time = timedelta()
        for check in self.checks:
            working_hours = check.working_hours
            if working_hours > timedelta(
                hours=WORK_JOURNEY.hour, minutes=WORK_JOURNEY.minute
            ):
                total_time += working_hours - timedelta(
                    hours=WORK_JOURNEY.hour, minutes=WORK_JOURNEY.minute
                )
        return total_time

    @property
    def negative_time(self):
        total_time = timedelta()
        for check in self.checks:
            total_time += check.negative_time
        return total_time

    @property
    def total_hour_balance(self):
        total = self.overtime
        if self.last_month_overtime:
            total += timedelta(
                hours=self.last_month_overtime.hour,
                minutes=self.last_month_overtime.minute,
            )
        return total

    @property
    def this_month_hour_to_charge(self):
        balance = (
            self.total_hour_balance
            - timedelta(hours=MAX_HOUR_BANK.hour, minutes=MAX_HOUR_BANK.minute)
            - self.negative_time
        )
        return balance if balance > timedelta(0) else timedelta(0)

    def to_dict(self):
        return {
            "month": f"{self.month:%B %Y}",
            "total_working_hours": self.total_working_hours,
            "overtime": self.overtime,
            "last_month_overtime": self.last_month_overtime,
            "negative_time": self.negative_time,
            "total_hour_balance": self.total_hour_balance,
            "this_month_hour_to_charge": self.this_month_hour_to_charge,
            "checks": [check.to_dict() for check in self.checks],
        }


def extractor(file_path):
    with open(file_path, "r") as file:
        soup = BeautifulSoup(file, "html.parser")

    div = soup.find("div", class_="panel panel-success")
    timeline_div = div.find("div", class_="timeline-wrapper")

    run = 0
    cycle = 0
    check_in_out = []

    for date_div in timeline_div.find_all("div", class_="timeline-date clearfix"):
        try:
            date_parsed = datetime.strptime(date_div.get_text(strip=True), "%d/%m/%Y")
        except ValueError:
            print(f"Invalid date format: {date_div.get_text(strip=True)}")
            date_parsed = None

        check_in_out.append(CheckInOut(date=date_parsed))

    for time_div in timeline_div.find_all("div", class_="timeline-item clearfix"):
        time_str = time_div.find("div", class_="time").get_text(strip=True)
        if run % 2 == 0:
            check_in_out[cycle].check_out = datetime.strptime(time_str, "%H:%M").time()
        else:
            check_in_out[cycle].check_in = datetime.strptime(time_str, "%H:%M").time()
            cycle += 1
        run += 1

    return check_in_out


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate working hours and balance.")
    parser.add_argument(
        "--interval_time", type=str, default="01:00", help="Interval time (HH:MM)"
    )
    parser.add_argument(
        "--work_journey", type=str, default="08:48", help="Working journey time (HH:MM)"
    )
    parser.add_argument(
        "--max_hour_bank",
        type=str,
        default="10:40",
        help="Maximum hour bank time (HH:MM)",
    )
    parser.add_argument(
        "--last_month_overtime",
        type=str,
        default="10:40",
        help="Last month overtime (HH:MM)",
    )

    args = parser.parse_args()

    INTERVAL_TIME = time.fromisoformat(args.interval_time)
    WORK_JOURNEY = time.fromisoformat(args.work_journey)
    MAX_HOUR_BANK = time.fromisoformat(args.max_hour_bank)
    LAST_MONTH_OVERTIME = time.fromisoformat(args.last_month_overtime)

    checks = extractor("Letswork.html")

    month_work = MonthWork(
        month=datetime.today(),
        checks=checks,
        last_month_overtime=LAST_MONTH_OVERTIME,
    )

    data = {
        "vars": {
            "interval_time": INTERVAL_TIME,
            "work_journey": WORK_JOURNEY,
            "max_hour_bank": MAX_HOUR_BANK,
        },
        "report": {
            "month_work": month_work.to_dict(),
        },
    }

    with open("output.json", "w") as file:
        json.dump(data, file, default=encoder, indent=4)
