#!/usr/bin/env python3
"""
Generate timestamp dimension table for data lake.

This script creates a comprehensive timestamp dimension table with:
- Hourly timestamps in UTC
- Country codes and timezones
- Holiday indicators
- Daylight savings indicators  
- Working hours indicators
- Weekend indicators
"""

import pandas as pd
import pytz
from datetime import datetime, timedelta
import holidays
from typing import Dict, List


# Country configurations
COUNTRIES = {
    'PT': {'name': 'Portugal', 'timezone': 'Europe/Lisbon'},
    'NL': {'name': 'Netherlands', 'timezone': 'Europe/Amsterdam'}, 
    'FR': {'name': 'France', 'timezone': 'Europe/Paris'},
    'ES': {'name': 'Spain', 'timezone': 'Europe/Madrid'},
    'DE': {'name': 'Germany', 'timezone': 'Europe/Berlin'},
    'IT': {'name': 'Italy', 'timezone': 'Europe/Rome'}
}

# Working hours (9 AM to 6 PM local time)
WORKING_HOUR_START = 9
WORKING_HOUR_END = 18


def generate_hourly_timestamps(start_date: str, end_date: str) -> List[datetime]:
    """Generate hourly timestamps in UTC between start and end dates."""
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    timestamps = []
    current = start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    while current <= end:
        timestamps.append(current)
        current += timedelta(hours=1)
    
    return timestamps


def is_working_hour(utc_timestamp: datetime, timezone_str: str) -> bool:
    """Check if timestamp falls within working hours (9-18) in local timezone."""
    tz = pytz.timezone(timezone_str)
    local_time = utc_timestamp.replace(tzinfo=pytz.UTC).astimezone(tz)
    return WORKING_HOUR_START <= local_time.hour < WORKING_HOUR_END


def is_weekend(utc_timestamp: datetime, timezone_str: str) -> bool:
    """Check if timestamp falls on weekend in local timezone."""
    tz = pytz.timezone(timezone_str)
    local_time = utc_timestamp.replace(tzinfo=pytz.UTC).astimezone(tz)
    return local_time.weekday() >= 5  # Saturday=5, Sunday=6


def is_holiday(utc_timestamp: datetime, country_code: str, timezone_str: str) -> bool:
    """Check if timestamp falls on a holiday in the given country."""
    tz = pytz.timezone(timezone_str)
    local_time = utc_timestamp.replace(tzinfo=pytz.UTC).astimezone(tz)
    local_date = local_time.date()
    
    # Get holidays for the country
    country_holidays = holidays.country_holidays(country_code, years=local_date.year)
    return local_date in country_holidays


def is_daylight_saving(utc_timestamp: datetime, timezone_str: str) -> bool:
    """Check if timestamp is during daylight saving time."""
    tz = pytz.timezone(timezone_str)
    local_time = utc_timestamp.replace(tzinfo=pytz.UTC).astimezone(tz)
    return bool(local_time.dst())


def generate_dimension_table(start_date: str = '2022-01-01', end_date: str = '2026-12-31') -> pd.DataFrame:
    """Generate the complete timestamp dimension table."""
    
    print(f"Generating timestamp dimension table from {start_date} to {end_date}...")
    
    # Generate all hourly timestamps
    timestamps = generate_hourly_timestamps(start_date, end_date)
    
    # Create list to store all rows
    rows = []
    
    total_combinations = len(timestamps) * len(COUNTRIES)
    processed = 0
    
    for timestamp in timestamps:
        for country_code, country_info in COUNTRIES.items():
            timezone_str = country_info['timezone']
            
            row = {
                'timestamp': timestamp,
                'country_code': country_code,
                'timezone': timezone_str,
                'holiday': int(is_holiday(timestamp, country_code, timezone_str)),
                'daylight_savings': int(is_daylight_saving(timestamp, timezone_str)),
                'working_hours': int(is_working_hour(timestamp, timezone_str)),
                'weekend': int(is_weekend(timestamp, timezone_str))
            }
            
            rows.append(row)
            processed += 1
            
            if processed % 10000 == 0:
                print(f"Processed {processed:,} / {total_combinations:,} combinations ({processed/total_combinations*100:.1f}%)")
    
    # Create DataFrame
    df = pd.DataFrame(rows)
    
    # Sort by timestamp and country_code
    df = df.sort_values(['timestamp', 'country_code']).reset_index(drop=True)
    
    print(f"Generated {len(df):,} rows")
    return df


def main():
    """Main function to generate and save the dimension table."""
    
    # Generate the dimension table
    df = generate_dimension_table()
    
    # Display sample data
    print("\nSample data:")
    print(df.head(10))
    
    print(f"\nData summary:")
    print(f"Total rows: {len(df):,}")
    print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"Countries: {', '.join(sorted(df['country_code'].unique()))}")
    
    # Show some statistics
    print(f"\nStatistics:")
    print(f"Holiday records: {df['holiday'].sum():,} ({df['holiday'].mean()*100:.1f}%)")
    print(f"Daylight savings records: {df['daylight_savings'].sum():,} ({df['daylight_savings'].mean()*100:.1f}%)")
    print(f"Working hours records: {df['working_hours'].sum():,} ({df['working_hours'].mean()*100:.1f}%)")
    print(f"Weekend records: {df['weekend'].sum():,} ({df['weekend'].mean()*100:.1f}%)")
    
    # Save to CSV
    output_file = 'timestamp_dimension.csv'
    df.to_csv(output_file, index=False)
    print(f"\nDimension table saved to: {output_file}")


if __name__ == "__main__":
    main()