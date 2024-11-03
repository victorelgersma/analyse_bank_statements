import chardet
from pathlib import Path
import pandas as pd

MONTH = 'oct'

# ANSI escape codes for colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"


print("\n--------------------------------------------------------\n")
print(f"{BLUE} REVOLUT  - TRANSACTIONS {RESET}")
print("\n--------------------------------------------------------\n")

def parse_rev(path):
    return pd.read_csv(path)

# euro account
rev_euro_df = parse_rev('../data/rev/eur/oct.csv')
# pound account
rev_gbp_df = parse_rev('../data/rev/gbp/oct.csv')

# dollar account
rev_usd_df = parse_rev('../data/rev/usd/oct.csv')


# columns
rev_columns=["Amount", "Description", "Completed Date"]


print("\nEuro Account\n")
print(rev_euro_df[rev_columns]) 
print("\nGBP Account\n")
print(rev_gbp_df[rev_columns]) 
print("\nUSD Account\n")
print(rev_usd_df[rev_columns]) 

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
    encoding = get_encoding(path)
    df = pd.read_html(Path(path), encoding=encoding, header =3)[0]
    cols = ["Date", "Description", "Money in", "Money Out"]
    return df[cols]
# santander current account
san_current = parse_san('../data/san/current/oct.html')
# santander savings account
san_savings = parse_san('../data/san/saver/oct.html')

san_columns=["Debit/Credit", "Date"]

print("\nCurrent Account\n")
print(san_current)

print("\nSavings Account\n")
print(san_savings)

