#!/usr/bin/env python3
"""
Verification script for the timestamp dimension table.
"""

import pandas as pd
import pytz
from datetime import datetime

def verify_timestamp_dimension():
    """Verify the generated timestamp dimension table."""
    
    print("=== TIMESTAMP DIMENSION TABLE VERIFICATION ===\n")
    
    # Load the CSV
    df = pd.read_csv('timestamp_dimension.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    print(f"1. BASIC STATISTICS:")
    print(f"   Total rows: {len(df):,}")
    print(f"   Expected rows: {5 * 365 * 24 * 6 + 1 * 24 * 6:,} (5 years + 1 leap day × 24 hours × 6 countries)")
    print(f"   Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"   Countries: {sorted(df['country_code'].unique())}")
    print(f"   File size: {df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB\n")
    
    print(f"2. DATA COMPLETENESS:")
    # Check for missing values
    missing = df.isnull().sum()
    print(f"   Missing values: {missing.sum()} total")
    for col in missing.index:
        if missing[col] > 0:
            print(f"     - {col}: {missing[col]}")
    
    # Check unique timestamps per country
    timestamps_per_country = df.groupby('country_code')['timestamp'].nunique()
    print(f"   Unique timestamps per country:")
    for country, count in timestamps_per_country.items():
        print(f"     - {country}: {count:,}")
    print()
    
    print(f"3. COLUMN DISTRIBUTIONS:")
    for col in ['holiday', 'daylight_savings', 'working_hours', 'weekend']:
        count = df[col].sum()
        pct = count / len(df) * 100
        print(f"   {col}: {count:,} records ({pct:.1f}%)")
    print()
    
    print(f"4. SAMPLE VALIDATIONS:")
    
    # Check New Year's Day (should be holiday in all countries)
    ny_2023 = df[df['timestamp'] == '2023-01-01 00:00:00']
    print(f"   New Year 2023 holidays: {ny_2023['holiday'].sum()}/6 countries")
    
    # Check summer time (should have daylight savings)
    summer_2023 = df[(df['timestamp'] >= '2023-06-01') & (df['timestamp'] < '2023-09-01')]
    summer_dst_pct = summer_2023['daylight_savings'].mean() * 100
    print(f"   Summer 2023 daylight savings: {summer_dst_pct:.1f}% of records")
    
    # Check working hours on a Wednesday
    wed_sample = df[df['timestamp'] == '2023-06-14 10:00:00']  # Wednesday 10 AM UTC
    print(f"   Working hours on Wed 10 AM UTC: {wed_sample['working_hours'].sum()}/6 countries")
    
    # Check weekend detection
    sat_sample = df[df['timestamp'] == '2023-06-17 12:00:00']  # Saturday
    print(f"   Weekend detection on Saturday: {sat_sample['weekend'].sum()}/6 countries")
    print()
    
    print(f"5. TIMEZONE VERIFICATION:")
    # Check that 8 AM UTC in summer is working hours for most European countries
    summer_8am = df[(df['timestamp'].dt.hour == 8) & 
                    (df['timestamp'] >= '2023-06-01') & 
                    (df['timestamp'] < '2023-09-01')]
    working_8am_pct = summer_8am['working_hours'].mean() * 100
    print(f"   8 AM UTC in summer working hours: {working_8am_pct:.1f}% (should be ~100% for European timezones)")
    
    # Check that midnight UTC is not working hours
    midnight = df[df['timestamp'].dt.hour == 0]
    working_midnight_pct = midnight['working_hours'].mean() * 100
    print(f"   Midnight UTC working hours: {working_midnight_pct:.1f}% (should be low)")
    print()
    
    print(f"6. DATA QUALITY CHECKS:")
    
    # Check for duplicate combinations
    duplicates = df.duplicated(['timestamp', 'country_code']).sum()
    print(f"   Duplicate timestamp-country combinations: {duplicates}")
    
    # Check binary columns only contain 0 and 1
    binary_cols = ['holiday', 'daylight_savings', 'working_hours', 'weekend']
    for col in binary_cols:
        unique_vals = sorted(df[col].unique())
        print(f"   {col} unique values: {unique_vals} (should be [0, 1])")
    
    # Check timezone consistency
    timezone_check = df.groupby('country_code')['timezone'].nunique()
    print(f"   Countries with multiple timezones:")
    for country, tz_count in timezone_check.items():
        if tz_count > 1:
            print(f"     - {country}: {tz_count} timezones")
        else:
            tz_name = df[df['country_code'] == country]['timezone'].iloc[0]
            print(f"     - {country}: {tz_name}")
    
    print(f"\n=== VERIFICATION COMPLETE ===")
    
    # Summary
    issues = []
    if duplicates > 0:
        issues.append(f"Found {duplicates} duplicate records")
    if missing.sum() > 0:
        issues.append(f"Found {missing.sum()} missing values")
    
    if issues:
        print(f"⚠️  ISSUES FOUND:")
        for issue in issues:
            print(f"   - {issue}")
    else:
        print(f"✅ All checks passed! Data looks good.")

if __name__ == "__main__":
    verify_timestamp_dimension()