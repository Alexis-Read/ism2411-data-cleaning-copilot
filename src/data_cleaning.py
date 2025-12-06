"""
Purpose:
    This script loads the raw sales dataset, performs essential data cleaning
    steps to prepare it for analysis, and writes the cleaned output to the
    processed data folder.
"""

import pandas as pd
# This function loads a CSV file from a given file path.
# Copilot suggested the structure, and I modified it to include a print statement so I can confirm which file is being loaded.
def load_data(file_path):
    print("Loading:", file_path)
    df = pd.read_csv(file_path)
    return df

# 1. What: Load the raw dataset
#    Why: All cleaning steps must start with importing the original data.
raw_path = "data/raw/sales_data_raw.csv"
df = pd.read_csv(raw_path)
print(df.columns)

# 2. What: Standardize column names
#    Why: Consistent lowercase + underscores makes analysis easier and avoids errors.
# This function standardizes column names by stripping whitespace,
# lowercasing all letters, and replacing spaces with underscores.
# Copilot generated most of this, and I adjusted the transformations.
def clean_column_names(df):
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df

df = clean_column_names(df)
print("Cleaned columns:", df.columns)

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
# This function handles missing numeric values in price and qty.
# Copilot suggested the structure; I changed it to coerce and drop rows with NaN.
def handle_missing_values(df):
    df["qty"] = pd.to_numeric(df["qty"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["qty", "price"])
    return df

# This function removes rows with invalid negative price or quantity values.
# Copilot suggested filtering logic; I modified it to check both columns together.
def remove_invalid_rows(df):
    df = df[(df["qty"] >= 0) & (df["price"] >= 0)]
    return df

if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())