"""
01_data_cleaning_and_eda.py
----------------------------
Data Analyst Task 3 & 4: Python for Data Analysis + Data Cleaning & EDA.

Covers, in order:
  - Loading a raw CSV
  - Data cleaning (missing values, duplicates, inconsistent text, bad dates,
    negative quantities, outliers)
  - Data validation
  - KPI calculation (pandas / numpy)
  - Descriptive statistics (mean, median, mode, std dev)
  - Correlation analysis
  - Trend analysis
  - Matplotlib visualizations saved as PNGs

Run: python3 01_data_cleaning_and_eda.py
Outputs:
  ../data/sales_data_cleaned.csv
  ../visuals/*.png
  prints a KPI + stats summary to stdout (also captured into eda/eda_report.md)
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

from pathlib import Path

pd.set_option("display.width", 120)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / "data" / "sales_data_raw.csv"
CLEAN_PATH = BASE_DIR / "data" / "sales_data_cleaned.csv"
VIZ_DIR = BASE_DIR / "visuals"
VIZ_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. LOAD
# ---------------------------------------------------------------------------
df = pd.read_csv(RAW_PATH)
print("=" * 70)
print("RAW DATA SHAPE:", df.shape)
print(df.dtypes)

# ---------------------------------------------------------------------------
# 2. DATA CLEANING
# ---------------------------------------------------------------------------

# 2a. Remove exact duplicate rows
before = len(df)
df = df.drop_duplicates()
print(f"\nRemoved {before - len(df)} duplicate rows")

# 2b. Standardize text columns: strip whitespace, fix casing
text_cols = ["CustomerName", "Region", "Category", "Product", "ShipMode"]
for col in text_cols:
    df[col] = df[col].astype(str).str.strip()
df["Region"] = df["Region"].str.title()
df["Category"] = df["Category"].str.title()
df.loc[df["Region"] == "Nan", "Region"] = np.nan

# 2c. Parse mixed-format dates (YYYY-MM-DD and DD/MM/YYYY both present)
def parse_mixed_date(value):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return pd.to_datetime(value, format=fmt)
        except (ValueError, TypeError):
            continue
    return pd.NaT

df["OrderDate"] = df["OrderDate"].apply(parse_mixed_date)
df["ShipDate"] = pd.to_datetime(df["ShipDate"], errors="coerce")

# 2d. Handle missing values
#   - Numeric: impute with the median of that Category (more robust than a
#     single global mean, and keeps the fix business-explainable)
for col in ["Quantity", "UnitPrice", "Discount", "Profit"]:
    df[col] = df.groupby("Category")[col].transform(lambda s: s.fillna(s.median()))
#   - Region / ShipMode: impute with the column mode (most frequent value)
for col in ["Region", "ShipMode"]:
    df[col] = df[col].fillna(df[col].mode().iloc[0])

# 2e. Fix invalid values: negative or zero quantities are data-entry errors
invalid_qty = (df["Quantity"] <= 0).sum()
df["Quantity"] = df["Quantity"].abs().replace(0, 1)
print(f"Fixed {invalid_qty} rows with non-positive Quantity")

# 2f. Outlier detection using the IQR method (flag, don't silently drop —
#     keep an explicit column so the business can decide what to do with them)
def iqr_bounds(series, k=1.5):
    q1, q3 = series.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr

low, high = iqr_bounds(df["Sales"])
df["Sales_Outlier"] = ~df["Sales"].between(low, high)
low_q, high_q = iqr_bounds(df["Quantity"])
df["Quantity_Outlier"] = ~df["Quantity"].between(low_q, high_q)
n_outliers = int(df["Sales_Outlier"].sum() + df["Quantity_Outlier"].sum())
print(f"Flagged {n_outliers} outlier values in Sales/Quantity (IQR method, k=1.5)")

# 2g. Data validation: rebuild Sales from Quantity/UnitPrice/Discount where the
#     stored Sales value is wildly inconsistent with its inputs (data integrity check)
expected_sales = (df["Quantity"] * df["UnitPrice"] * (1 - df["Discount"])).round(2)
mismatch = (df["Sales"] - expected_sales).abs() > (0.25 * expected_sales.clip(lower=1))
print(f"Sales values inconsistent with Qty*Price*(1-Discount): {mismatch.sum()} rows (kept, flagged)")
df["Sales_Validation_Flag"] = mismatch

# 2h. Derived columns useful for reporting
df["OrderMonth"] = df["OrderDate"].dt.to_period("M").astype(str)
df["ShippingDays"] = (df["ShipDate"] - df["OrderDate"]).dt.days
df["ProfitMargin"] = (df["Profit"] / df["Sales"]).round(4)

df.to_csv(CLEAN_PATH, index=False)
print(f"\nCleaned dataset saved -> {CLEAN_PATH}  (shape={df.shape})")

# ---------------------------------------------------------------------------
# 3. KPI CALCULATION
# ---------------------------------------------------------------------------
kpis = {
    "Total Revenue": df["Sales"].sum(),
    "Total Profit": df["Profit"].sum(),
    "Overall Profit Margin %": 100 * df["Profit"].sum() / df["Sales"].sum(),
    "Total Orders": df["OrderID"].nunique(),
    "Total Units Sold": df["Quantity"].sum(),
    "Average Order Value": df.groupby("OrderID")["Sales"].sum().mean(),
    "Average Discount %": 100 * df["Discount"].mean(),
    "Average Shipping Days": df["ShippingDays"].mean(),
}
print("\n" + "=" * 70)
print("KPI SUMMARY")
for k, v in kpis.items():
    print(f"  {k:<28}: {v:,.2f}")

# ---------------------------------------------------------------------------
# 4. DESCRIPTIVE STATISTICS
# ---------------------------------------------------------------------------
stats = df[["Sales", "Profit", "Quantity", "Discount"]].agg(["mean", "median", "std"])
mode_row = df[["Sales", "Profit", "Quantity", "Discount"]].mode().iloc[0]
print("\nDESCRIPTIVE STATISTICS")
print(stats)
print("\nMode:\n", mode_row)

# ---------------------------------------------------------------------------
# 5. CORRELATION
# ---------------------------------------------------------------------------
corr = df[["Sales", "Profit", "Quantity", "Discount", "UnitPrice"]].corr()
print("\nCORRELATION MATRIX")
print(corr.round(3))

# ---------------------------------------------------------------------------
# 6. TREND / BREAKDOWN ANALYSIS
# ---------------------------------------------------------------------------
monthly = df.groupby("OrderMonth")["Sales"].sum().sort_index()
by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
top_products = df.groupby("Product")["Sales"].sum().sort_values(ascending=False).head(10)

# ---------------------------------------------------------------------------
# 7. VISUALIZATIONS
# ---------------------------------------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

# Monthly sales trend
fig, ax = plt.subplots(figsize=(9, 4.5))
monthly.plot(kind="line", marker="o", ax=ax, color="#2563eb")
ax.set_title("Monthly Sales Trend")
ax.set_ylabel("Sales ($)")
ax.set_xlabel("Month")
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/01_monthly_sales_trend.png", dpi=150)
plt.close()

# Sales by region
fig, ax = plt.subplots(figsize=(6, 4.5))
by_region.plot(kind="bar", ax=ax, color="#16a34a")
ax.set_title("Total Sales by Region")
ax.set_ylabel("Sales ($)")
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/02_sales_by_region.png", dpi=150)
plt.close()

# Sales by category (pie)
fig, ax = plt.subplots(figsize=(6, 6))
by_category.plot(kind="pie", ax=ax, autopct="%1.1f%%", ylabel="", colors=["#2563eb", "#16a34a", "#f59e0b"])
ax.set_title("Sales Share by Category")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/03_sales_by_category.png", dpi=150)
plt.close()

# Top 10 products
fig, ax = plt.subplots(figsize=(8, 5))
top_products.sort_values().plot(kind="barh", ax=ax, color="#7c3aed")
ax.set_title("Top 10 Products by Sales")
ax.set_xlabel("Sales ($)")
ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/04_top_products.png", dpi=150)
plt.close()

# Correlation heatmap
fig, ax = plt.subplots(figsize=(5.5, 5))
im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=45, ha="right")
ax.set_yticklabels(corr.columns)
for i in range(len(corr.columns)):
    for j in range(len(corr.columns)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
ax.set_title("Correlation Matrix")
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/05_correlation_heatmap.png", dpi=150)
plt.close()

# Sales distribution / outliers (boxplot)
fig, ax = plt.subplots(figsize=(6, 4.5))
ax.boxplot(df["Sales"], orientation="horizontal")
ax.set_title("Sales Distribution & Outliers")
ax.set_xlabel("Sales ($)")
plt.tight_layout()
plt.savefig(f"{VIZ_DIR}/06_sales_outliers_boxplot.png", dpi=150)
plt.close()

print(f"\n6 chart(s) saved to {VIZ_DIR}/")
print("\nDONE.")
