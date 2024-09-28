# Lets Work Hours Balance Calculator

A Python script that organizes your worked hours for the month and helps you keep track of your hours balance.

## Features

- **Calculate Working Hours**: Automatically calculates the total working hours for the month based on check-in and check-out times.
- **Overtime Calculation**: Identifies and calculates any overtime hours worked.
- **Negative Time Tracking**: Keeps track of any negative time when working hours fall short of the standard work journey.
- **Flexible Input**: Allows the user to set parameters such as interval time, work journey, maximum hour bank, and last month's overtime directly from the command line.
- **Output Report**: Generates a structured JSON report summarizing the monthly work hours, overtime, negative time, and checks.

## Installation

To run this project, ensure you have Python installed on your system. This script also requires the `BeautifulSoup` library for HTML parsing.

You can install the necessary library using pip:

```bash
pip install beautifulsoup4
```

## Usage

Run the script via the command line and pass the required parameters:

```bash
python extractor.py --interval_time HH:MM --work_journey HH:MM --max_hour_bank HH:MM --last_month_overtime HH:MM
```

### Parameters

- `--interval_time`: The break interval time (e.g., `01:00` for one hour).
- `--work_journey`: The standard work journey duration (e.g., `08:48`).
- `--max_hour_bank`: The maximum allowed hour bank (e.g., `10:40`).
- `--last_month_overtime`: The overtime carried over from the last month (e.g., `10:40`).

### Example

```bash
python extractor.py --interval_time 01:00 --work_journey 08:48 --max_hour_bank 10:40 --last_month_overtime 10:40
```

### Output

The script generates an `output.json` file containing:

```json
{
    "vars": {
        "interval_time": "01:00:00",
        "work_journey": "08:48:00",
        "max_hour_bank": "10:40:00"
    },
    "report": {
        "month_work": {
            "month": "September 2024",
            "total_working_hours": "194h46m",
            "overtime": "19h46m",
            "last_month_overtime": "10:40:00",
            "negative_time": "01h00m",
            "total_hour_balance": "30h26m",
            "this_month_hour_to_charge": "18h46m",
            "checks": [
                {
                    "date": "2024-09-27T00:00:00",
                    "weekday": "Friday",
                    "check_in": "09:09:00",
                    "check_out": "22:03:00",
                    "working_hours": "11:54:00",
                    "negative_time": "00:00:00"
                },
                // ... more check-in/check-out records
            ]
        }
    }
}
```

## Contributing

If you would like to contribute to this project, feel free to fork the repository and submit a pull request. Any contributions are welcome!