# Lets Work Hours Balance Calculator

A Python script that organizes your worked hours for the month and helps you keep track of your hours balance.

## Features

- **Calculate Working Hours**: Automatically calculates the total working hours for the month based on check-in and check-out times.
- **Overtime Calculation**: Identifies and calculates any overtime hours worked, including hours worked on weekends.
- **Negative Time Tracking**: Keeps track of any negative time when working hours fall short of the standard work journey.
- **Flexible Input**: Users can configure parameters such as interval time, work journey, maximum hour bank, and last month's overtime via constants.
- **Weekend Work Calculation**: Automatically calculates hours worked during weekends.
- **Output Report**: Generates a structured JSON report summarizing the monthly work hours, overtime, negative time, and checks.
- **Automated Tests**: Unit tests are included to ensure the integrity of the calculations and functionality.

## Installation

Ensure you have Python installed on your system. The script also requires the `BeautifulSoup` library for HTML parsing.

You can install the required dependencies using pip:

```bash
pip install beautifulsoup4
```

## Usage

1. First, ensure that you have an HTML file containing the check-in and check-out information in the correct format.
2. Run the script, and it will parse the HTML file and calculate your work hours:

```bash
python extractor.py
```

### Constants

These constants are defined in the `constants.py` file:

```python
from datetime import time

INTERVAL_TIME = time.fromisoformat("01:00")
WORK_JOURNEY = time.fromisoformat("08:48")
MAX_HOUR_BANK = time.fromisoformat("10:40")
LAST_MONTH_OVERTIME = time.fromisoformat("10:40")
WEEKEND_DAYS = [5, 6]
```

- **`INTERVAL_TIME`**: The break interval time (e.g., `01:00` for one hour).
- **`WORK_JOURNEY`**: The standard work journey duration (e.g., `08:48`).
- **`MAX_HOUR_BANK`**: The maximum allowed hour bank (e.g., `10:40`).
- **`LAST_MONTH_OVERTIME`**: The overtime carried over from the last month (e.g., `10:40`).
- **`WEEKEND_DAYS`**: Days considered as weekends (e.g., `[5, 6]` for Saturday and Sunday).

These constants can be adjusted to fit your work schedule by modifying the `constants.py` file.

### Output

The script generates a `report.json` file containing:

```json
{
    "vars": {
        "interval_time": "01h00m",
        "work_journey": "08h48m",
        "max_hour_bank": "10h40m",
        "last_month_overtime": "10h40m",
        "weekend_days": [
            5,
            6
        ]
    },
    "report": {
        "month_work": {
            "current_month": "September 2024",
            "working_hours": "200h15m",
            "current_overtime": "25h15m",
            "weekend_worked_hours": "05h29m",
            "negative_time": "01h00m",
            "last_month_overtime": "10h40m",
            "bank_hour_balance": "35h55m",
            "this_month_hour_to_charge": "24h15m",
            "checks": [
                {
                    "date": "28/09/2024",
                    "weekday_day": "Saturday",
                    "check_in": "08h56m",
                    "check_out": "14h25m",
                    "working_hours": "05h29m",
                    "negative_time": "00h00m"
                },
                {
                    "date": "27/09/2024",
                    "weekday_day": "Friday",
                    "check_in": "09h09m",
                    "check_out": "22h03m",
                    "working_hours": "11h54m",
                    "negative_time": "00h00m"
                },
                {
                    "date": "26/09/2024",
                    "weekday_day": "Thursday",
                    "check_in": "09h03m",
                    "check_out": "19h00m",
                    "working_hours": "08h57m",
                    "negative_time": "00h00m"
                }
                // more check-in/check-out records
            ]
        }
    }
}
```

## Running Tests

To ensure the accuracy of the calculations, automated tests are available. You can run the tests located in the `tests` directory using `pytest`:

```bash
pytest tests/
```

These tests validate the working hours, overtime, negative time calculations, and more.

## Contributing

If you want to contribute to this project, feel free to fork the repository and submit a pull request. Any improvements, bug fixes, or feature suggestions are welcome!
