import chardet
from pathlib import Path
import pandas as pd

MONTH = 'oct'
BALANCE = 0

# ANSI escape codes for colors
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"


print("\n--------------------------------------------------------\n")
print(f"{BLUE} REVOLUT  - TRANSACTIONS {RESET}")
print("\n--------------------------------------------------------\n")

def parse_rev(path):
    return pd.read_csv(path)

paths = ['../data/rev/eur/oct.csv', '../data/rev/gbp/oct.csv', '../data/rev/usd/oct.csv']
# euro account

rev_columns=["Amount", "Description", "Completed Date", "Currency"]

def analyze(path, columns):
    df = parse_rev(path)
    print(df.dtypes)
    print(df[rev_columns])
    print("sum", df["Amount"].sum())

for path in paths:
    analyze(path, rev_columns)

# columns


print("\n--------------------------------------------------------\n")
print(f"{RED} SANTANDER - TRANSACTIONS {RESET}")
print("\n--------------------------------------------------------\n")

# detect encoding

san_current_file_path='../data/san/current/oct.html' 

def get_encoding(path):
    with open(path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
        print(f"Detected encoding: {encoding}")
    return encoding


def parse_san(path):
    # TODO - add doctest with dummy data
    encoding = get_encoding(path)
    encoding = get_encoding(path)
    df = pd.read_html(Path(path), encoding=encoding, header =3)[0]
    cols = ["Date", "Description", "Money in", "Money Out"]
    # turn into booleans
    df['Money in'] = df['Money in'].str.replace('£', '').str.replace(',', '').astype(float)
    df['Money Out'] = df['Money Out'].str.replace('£', '').str.replace(',', '').astype(float)
    # Replace NaNs with 0
    df['Money in'] = df['Money in'].fillna(0)
    df['Money Out'] = df['Money Out'].fillna(0)
    return df[cols]

# santander current account
san_current = parse_san('../data/san/current/oct.html')
# santander savings account
san_savings = parse_san('../data/san/saver/oct.html')

san_columns=["Debit/Credit", "Date"]

print("\nCurrent Account\n")
print(san_current.dtypes)
print(san_current)

print("total money out", san_current["Money Out"].sum())
print("total money in", san_current["Money in"].sum())
print("sum", - san_current["Money Out"].sum() + san_current["Money in"].sum())
print("\nSavings Account\n")
print(san_savings)
print("sum", - san_savings["Money Out"].sum() + san_savings["Money in"].sum())



