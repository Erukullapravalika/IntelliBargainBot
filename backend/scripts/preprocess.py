import os
import pandas as pd

# ==============================
# PATH SETUP
# ==============================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")
OUTPUT_PATH = os.path.join(DATA_PATH, "processed")

os.makedirs(OUTPUT_PATH, exist_ok=True)

# ==============================
# LOAD DATA
# ==============================
file_path = os.path.join(DATA_PATH, "Online_Retail.csv")
df = pd.read_csv(file_path, encoding="ISO-8859-1")

print("Original shape:", df.shape)

# ==============================
# BASIC CLEANING
# ==============================

# Remove missing customer IDs (important for RFM)
df = df.dropna(subset=["CustomerID"])

# Remove cancelled orders (InvoiceNo starting with 'C')
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# Remove negative or zero quantities
df = df[df["Quantity"] > 0]

# Remove negative prices
df = df[df["UnitPrice"] > 0]

# Convert date
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Create revenue (REAL feature)
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

print("After cleaning:", df.shape)

# ==============================
# SAVE CLEAN DATA
# ==============================

output_file = os.path.join(OUTPUT_PATH, "retail_clean.csv")
df.to_csv(output_file, index=False)

print("Cleaned data saved at:", output_file)

# ==============================
# VALIDATION
# ==============================

print("\nSample:\n", df.head())