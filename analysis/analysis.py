import pandas as pd

# Load dataset
df = pd.read_csv("data/retail sales.csv", encoding="cp1252")

print("ORIGINAL DATASET SHAPE:")
print(df.shape)

# Convert date columns into datetime format
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Check missing values
print("\nMISSING VALUES:")
print(df.isnull().sum())

# Check duplicate records
print("\nDUPLICATE RECORDS:")
print(df.duplicated().sum())

# Remove duplicate records
df = df.drop_duplicates()

# Check final dataset
print("\nCLEANED DATASET SHAPE:")
print(df.shape)

print("\nUPDATED DATA TYPES:")
print(df.dtypes)

# Save cleaned dataset
df.to_csv("data/cleaned_retail_sales.csv", index=False)

print("\nData cleaning completed successfully!")

