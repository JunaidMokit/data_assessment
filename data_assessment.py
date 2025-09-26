# data_assessment.py
# ----------------------------------------------------
# Data Assessment & Profitability Analysis
# ----------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ----------------------------------------------------
# 1. Load data
# ----------------------------------------------------
file_path = "Assessment Data - data.csv"  # <-- replace with your file path
df = pd.read_csv(file_path)

print("Dataset loaded successfully.")
print(f"Shape: {df.shape}")
print("Columns:", df.columns.tolist())
print("\nPreview:")
print(df.head())

# ----------------------------------------------------
# 2. Data Cleaning & Preparation
# ----------------------------------------------------

# Strip whitespace from object columns
for c in df.select_dtypes(include=["object"]).columns:
    df[c] = df[c].astype(str).str.strip().replace({"nan": np.nan})

# Parse date columns
for col in ["open_time", "close_time"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

# Ensure profit column is numeric
df["profit"] = pd.to_numeric(df["profit"], errors="coerce")

# Drop rows with missing login or profit
rows_before = len(df)
df = df.dropna(subset=["login", "profit"])
rows_after = len(df)
print(f"\nDropped {rows_before - rows_after} rows with missing login/profit.")

# Drop duplicates
dupes = df.duplicated().sum()
df = df.drop_duplicates()
print(f"Dropped {dupes} duplicate rows.")

# ----------------------------------------------------
# 3. Exploratory Data Analysis (EDA)
# ----------------------------------------------------
print("\nData Summary:")
print(df.describe(include="all").T)

print("\nMissing values per column:")
print(df.isna().sum())

# Distribution of profit per trade
plt.figure(figsize=(8, 4))
plt.hist(df["profit"].dropna(), bins=80, edgecolor="black")
plt.title("Distribution of Profit per Trade")
plt.xlabel("Profit")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("profit_distribution.png")
plt.close()

# ----------------------------------------------------
# 4. Profitability Analysis
# ----------------------------------------------------
profit_per_login = (
    df.groupby("login")["profit"]
    .agg(total_profit="sum", n_trades="count", avg_profit="mean")
    .reset_index()
    .sort_values("total_profit", ascending=False)
)

# Save results
profit_per_login.to_csv("profit_per_login.csv", index=False)

# Top and bottom logins
top10 = profit_per_login.head(10)
bottom10 = profit_per_login.tail(10).sort_values("total_profit")

print("\nTop 10 logins by total profit:")
print(top10)

print("\nBottom 10 logins by total profit:")
print(bottom10)

# ----------------------------------------------------
# 5. Visualizations
# ----------------------------------------------------
# Top 10 logins bar chart
plt.figure(figsize=(10, 5))
plt.bar(top10["login"].astype(str), top10["total_profit"], color="green")
plt.title("Top 10 Logins by Cumulative Profit")
plt.xlabel("Login")
plt.ylabel("Total Profit")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("top10_logins.png")
plt.close()

# Bottom 10 logins bar chart
plt.figure(figsize=(10, 5))
plt.bar(bottom10["login"].astype(str), bottom10["total_profit"], color="red")
plt.title("Bottom 10 Logins by Cumulative Profit")
plt.xlabel("Login")
plt.ylabel("Total Profit")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("bottom10_logins.png")
plt.close()

# ----------------------------------------------------
# 6. Report Export
# ----------------------------------------------------
report = f"""
# Data Assessment Report

**Rows after cleaning:** {len(df)}  
**Columns:** {df.shape[1]}  

## Profitability Insights
- Unique logins: {profit_per_login['login'].nunique()}
- Top login: {top10.iloc[0]['login']} with total profit {top10.iloc[0]['total_profit']:.2f}
- Bottom login: {bottom10.iloc[-1]['login']} with total profit {bottom10.iloc[-1]['total_profit']:.2f}

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
"""

with open("data_assessment_report.md", "w") as f:
    f.write(report)

print("\nAnalysis complete. Files generated:")
print("- profit_distribution.png")
print("- top10_logins.png")
print("- bottom10_logins.png")
print("- profit_per_login.csv")
print("- data_assessment_report.md")
