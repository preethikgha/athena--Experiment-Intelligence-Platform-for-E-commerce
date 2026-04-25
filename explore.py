import pandas as pd

df = pd.read_csv("events.csv")

print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nEvent types:")
print(df["event"].value_counts())
print("\nMissing values:")
print(df.isnull().sum())
