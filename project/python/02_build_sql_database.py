"""
02_build_sql_database.py
--------------------------
Loads the cleaned dataset into a SQLite database with a normalized-ish
schema (customers / products / orders) so the SQL task exercises real
JOINs instead of one flat table.

Run: python3 02_build_sql_database.py
Output: ../data/sales_data.db
"""

import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_PATH = BASE_DIR / "data" / "sales_data_cleaned.csv"
DB_PATH = BASE_DIR / "data" / "sales_data.db"

df = pd.read_csv(CLEAN_PATH, parse_dates=["OrderDate", "ShipDate"])

# --- Build dimension tables -------------------------------------------------
customers = (
    df[["CustomerID", "CustomerName", "Region"]]
    .drop_duplicates(subset="CustomerID")
    .reset_index(drop=True)
)

products = (
    df[["Product", "Category"]]
    .drop_duplicates()
    .reset_index(drop=True)
)
products.insert(0, "ProductID", ["P-" + str(i + 1).zfill(3) for i in range(len(products))])

df = df.merge(products, on=["Product", "Category"], how="left")

orders = df[[
    "OrderID", "CustomerID", "ProductID", "OrderDate", "ShipDate", "ShipMode",
    "Quantity", "UnitPrice", "Discount", "Sales", "Profit", "ShippingDays", "ProfitMargin"
]].copy()

# --- Write to SQLite ---------------------------------------------------------
conn = sqlite3.connect(DB_PATH)
customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)

conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(CustomerID)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_product ON orders(ProductID)")
conn.commit()

print("Tables created:")
for t in ["customers", "products", "orders"]:
    n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  {t}: {n} rows")

conn.close()
print(f"\nDatabase written -> {DB_PATH}")
