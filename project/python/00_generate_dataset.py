"""
00_generate_dataset.py
-----------------------
Generates a synthetic "Superstore-style" sales dataset that mimics a real
messy business export: missing values, duplicate rows, inconsistent text
casing, stray whitespace, a few outliers, and mixed date formats.

This raw file is the single source of truth used by every other task in the
project (Excel dashboard, SQL practice DB, Python EDA, Power BI dashboard).

Run: python3 00_generate_dataset.py
Output: ../data/sales_data_raw.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(42)

N = 2000  # number of order line items

regions = ["North", "South", "East", "West"]
categories = {
    "Furniture": ["Chair", "Desk", "Bookcase", "Table Lamp"],
    "Technology": ["Laptop", "Monitor", "Printer", "Wireless Mouse"],
    "Office Supplies": ["Paper", "Binder", "Stapler", "Pens (Box)"],
}
ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]

customers = pd.DataFrame({
    "CustomerID": [f"CUST-{i:04d}" for i in range(1, 201)],
    "CustomerName": [f"Customer {i}" for i in range(1, 201)],
    "Region": rng.choice(regions, 200),
})

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for i in range(1, N + 1):
    cust = customers.sample(1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
    category = rng.choice(list(categories.keys()))
    product = rng.choice(categories[category])
    quantity = int(rng.integers(1, 12))
    unit_price = round(float(rng.uniform(5, 1200)), 2)
    discount = float(rng.choice([0, 0, 0, 0.1, 0.15, 0.2, 0.3], p=[0.45, 0.1, 0.1, 0.15, 0.1, 0.05, 0.05]))
    sales = round(quantity * unit_price * (1 - discount), 2)
    cost_ratio = float(rng.uniform(0.5, 0.85))
    profit = round(sales - (quantity * unit_price * cost_ratio), 2)
    order_date = start_date + timedelta(days=int(rng.integers(0, date_range_days)))
    ship_days = int(rng.integers(1, 8))
    ship_date = order_date + timedelta(days=ship_days)

    rows.append({
        "OrderID": f"ORD-{10000 + i}",
        "OrderDate": order_date,
        "ShipDate": ship_date,
        "ShipMode": rng.choice(ship_modes),
        "CustomerID": cust["CustomerID"],
        "CustomerName": cust["CustomerName"],
        "Region": cust["Region"],
        "Category": category,
        "Product": product,
        "Quantity": quantity,
        "UnitPrice": unit_price,
        "Discount": discount,
        "Sales": sales,
        "Profit": profit,
    })

df = pd.DataFrame(rows)

# ---------------------------------------------------------------------------
# Deliberately dirty the data so the cleaning task has real work to do
# ---------------------------------------------------------------------------

# 1) Missing values scattered across several columns
for col, frac in [("Quantity", 0.02), ("UnitPrice", 0.015), ("Discount", 0.03),
                   ("Region", 0.01), ("ShipMode", 0.02), ("Profit", 0.01)]:
    idx = df.sample(frac=frac, random_state=1).index
    df.loc[idx, col] = np.nan

# 2) Duplicate rows (simulating a double export)
dupes = df.sample(25, random_state=2)
df = pd.concat([df, dupes], ignore_index=True)

# 3) Inconsistent text casing / stray whitespace
df["Region"] = df["Region"].apply(
    lambda x: x.lower() if isinstance(x, str) and rng.random() < 0.15 else x
)
df["CustomerName"] = df["CustomerName"].apply(
    lambda x: f"  {x}  " if isinstance(x, str) and rng.random() < 0.1 else x
)
df["Category"] = df["Category"].apply(
    lambda x: x.upper() if isinstance(x, str) and rng.random() < 0.1 else x
)

# 4) A handful of extreme outliers in Sales / Quantity
outlier_idx = df.sample(6, random_state=3).index
df.loc[outlier_idx[:3], "Quantity"] = rng.integers(150, 300, 3)
df.loc[outlier_idx[3:], "Sales"] = df.loc[outlier_idx[3:], "Sales"] * rng.uniform(15, 25, 3)

# 5) Mixed date formats written as text for a subset of rows
def messy_date(d):
    if pd.isna(d):
        return d
    if rng.random() < 0.2:
        return d.strftime("%d/%m/%Y")
    return d.strftime("%Y-%m-%d")

df["OrderDate"] = df["OrderDate"].apply(messy_date)
df["ShipDate"] = df["ShipDate"].dt.strftime("%Y-%m-%d")

# 6) A few negative / zero quantities (data entry errors)
neg_idx = df.sample(4, random_state=4).index
df.loc[neg_idx, "Quantity"] = -abs(df.loc[neg_idx, "Quantity"].fillna(1))

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
data_dir = BASE_DIR / "data"
data_dir.mkdir(parents=True, exist_ok=True)
out_path = data_dir / "sales_data_raw.csv"

df.to_csv(out_path, index=False)
print(f"Wrote {len(df)} rows to {out_path}")
print(df.isna().sum())
