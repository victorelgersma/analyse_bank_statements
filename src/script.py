
from pathlib import Path
import pandas as pd
# ANSI escape codes for colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"


print("\n--------------------------------------------------------\n")
print(f"{BLUE} REVOLUT {RESET}")
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


print("\nEuro:\n")
print(rev_euro_df[rev_columns]) 
print("\nGBP:\n")
print(rev_gbp_df[rev_columns]) 
print("\nUSD:\n")
print(rev_usd_df[rev_columns]) 

print("\n--------------------------------------------------------\n")
print(f"{RED} santander {RESET}")
print("\n--------------------------------------------------------\n")

def parse_san(path):
    return pd.read_html(Path(path), header =3)[0]
# santander current account
san_current = parse_san('../data/san/current/oct.html')
# santander savings account
san_savings = parse_san('../data/san/saver/oct.html')

san_columns=["Debit/Credit", "Date"]

print("\nTransactions - Current Account\n")
print(san_current)

print("\nTransactions - Savings Account\n")
print(san_savings)

