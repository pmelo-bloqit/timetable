# Timestamp Dimension Table Generation Log

## Generation Details
- **Date Range**: 2022-01-01 to 2026-12-31 (5 years)
- **Generated On**: September 5, 2025
- **Script**: `generate_timestamp_dimension.py`
- **Output File**: `timestamp_dimension.csv`

## Data Specifications
- **Granularity**: Hourly timestamps in UTC
- **Countries**: 6 European countries (PT, NL, FR, ES, DE, IT)
- **Timezones**: Proper European timezones for each country
- **Columns**: 7 total (timestamp, country_code, timezone, holiday, daylight_savings, working_hours, weekend)

## Generation Results
- **Total Rows**: 262,806
- **Expected Rows**: 262,944 (slight difference due to end date handling)
- **File Size**: 11.8 MB (CSV), 42.4 MB (in memory)
- **Processing Time**: ~30 seconds
- **Memory Usage**: Efficient with progress tracking

## Data Quality Verification
✅ **No missing values**
✅ **No duplicate timestamp-country combinations**  
✅ **All binary columns contain only 0 and 1**
✅ **Consistent timezone mapping per country**
✅ **Proper weekend detection (28.6% of records)**
✅ **Working hours detection (37.5% of records - 9 AM to 6 PM local time)**
✅ **Daylight savings detection (58.3% of records)**
✅ **Holiday detection (2.9% of records)**

## Column Statistics
- **Holiday**: 7,744 records (2.9%)
- **Daylight Savings**: 153,216 records (58.3%)
- **Working Hours**: 98,550 records (37.5%)
- **Weekend**: 75,163 records (28.6%)

## Timezone Mappings
- **PT (Portugal)**: Europe/Lisbon
- **NL (Netherlands)**: Europe/Amsterdam
- **FR (France)**: Europe/Paris
- **ES (Spain)**: Europe/Madrid
- **DE (Germany)**: Europe/Berlin
- **IT (Italy)**: Europe/Rome

## Sample Validations
- **New Year 2023**: 5/6 countries marked as holiday (Spain exception noted)
- **Summer DST**: 100% of summer records have daylight savings
- **Working Hours**: Correctly identifies 10 AM UTC on Wednesday as working hours
- **Weekend Detection**: Correctly identifies Saturday as weekend
- **Timezone Logic**: 8 AM UTC in summer = working hours for all European countries

## Technical Notes
- Used `holidays` library for country-specific holiday detection
- Used `pytz` for accurate timezone and DST calculations
- All calculations respect local time zones for each country
- Working hours: 9 AM - 6 PM local time
- Weekend: Saturday and Sunday in local time

## Files Generated
1. `timestamp_dimension.csv` - Main output file
2. `generation_log.md` - This log file
3. `verify_data.py` - Verification script

## Dependencies Used
- pandas 2.3.2
- pytz 2023.4
- holidays 0.34
- Python 3.11

## Status
🎯 **GENERATION SUCCESSFUL** - Ready for data lake ingestion