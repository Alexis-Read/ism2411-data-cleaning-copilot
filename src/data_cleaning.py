"""
Purpose:
    This script loads the raw sales dataset, performs essential data cleaning
    steps to prepare it for analysis, and writes the cleaned output to the
    processed data folder.
"""

import pandas as pd

# 1. What: Load the raw dataset
#    Why: All cleaning steps must start with importing the original data.
raw_path = "data/raw/sales_data_raw.csv"
df = pd.read_csv(raw_path)
print(df.columns)

# 2. What: Standardize column names
#    Why: Consistent lowercase + underscores makes analysis easier and avoids errors.
df.columns = df.columns.str.strip()
df.columns = df.columns.str.lower().str.replace(" ", "_")

# 3. What: Strip whitespace from product/category names
#    Why: Leading/trailing spaces cause duplicate categories or products to appear.
if "product" in df.columns:
    df["product"] = df["product"].str.strip()

if "category" in df.columns:
    df["category"] = df["category"].str.strip()

# 4. What: Handle missing prices and quantities
#    Why: Missing numeric values break calculations — we choose to drop them.
df = df.dropna(subset=["price", "qty"])
df["qty"] = pd.to_numeric(df["qty"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# 5. What: Remove rows with invalid negative values
#    Why: Negative quantities or negative prices are data-entry mistakes.
df = df[(df["qty"] >= 0) & (df["price"] >= 0)]

# 6. What: Write cleaned dataset to processed folder
#    Why: Save the new, cleaned version for future analysis steps.
processed_path = "data/processed/sales_data_clean.csv"
df.to_csv(processed_path, index=False)

print("Data cleaning complete. Cleaned file saved to:", processed_path)
