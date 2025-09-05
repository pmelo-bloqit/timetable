# Timestamp Dimension Table Generator

This project generates a comprehensive timestamp dimension table for data lake analytics.

## Features

The generated table includes:
- **Timestamp**: Hourly timestamps in UTC (24 per day)
- **Country Code**: PT, NL, FR, ES, DE, IT (Portugal, Netherlands, France, Spain, Germany, Italy)
- **Timezone**: Corresponding timezone for each country
- **Holiday**: Binary indicator for national holidays
- **Daylight Savings**: Binary indicator for daylight saving time periods
- **Working Hours**: Binary indicator for business hours (9 AM - 6 PM local time)
- **Weekend**: Binary indicator for weekends

## Setup

1. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Run the generator:
   ```bash
   poetry run python generate_timestamp_dimension.py
   ```

## Output

The script generates a CSV file `timestamp_dimension.csv` with all combinations of timestamps and countries for the year 2024.

## Customization

You can modify the date range by editing the `generate_dimension_table()` function call in the main function:

```python
df = generate_dimension_table(start_date='2023-01-01', end_date='2025-12-31')
```
