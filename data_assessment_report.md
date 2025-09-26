
# Data Assessment Report

**Rows after cleaning:** 59317  
**Columns:** 14  

## Profitability Insights
- Unique logins: 600
- Top login: 13378390.0 with total profit 53891.98
- Bottom login: 13131614.0 with total profit -9573.61

## Actions Taken
- Cleaned whitespace in object columns
- Parsed datetime columns (open_time, close_time)
- Converted profit column to numeric
- Dropped rows with missing login/profit
- Removed duplicate rows

## Files Generated
- profit_distribution.png
- top10_logins.png
- bottom10_logins.png
- profit_per_login.csv
