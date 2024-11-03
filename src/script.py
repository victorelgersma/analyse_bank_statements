
from pathlib import Path
import pandas as pd
# ANSI escape codes for colors
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"


# revolut
# euro account
rev_euro_df = pd.read_csv('../data/rev/eur/oct.csv')
# pound account
rev_gbp_df = pd.read_csv('../data/rev/gbp/oct.csv')

# dollar account
rev_usd_df = pd.read_csv('../data/rev/usd/oct.csv')

# santander current account
san = pd.read_html(Path('../data/san/current/oct.html'))[0] 

# santander savings account

san = pd.read_html(Path('../data/san/saver/oct.html'))[0] 

rev_columns=["Amount", "Description", "Completed Date"]
san_columns=["Debit/Credit", "Date"]

print("\nRevolut:\n")
print("\ndata structure")
print(rev_euro_df.info()) 

# print(rev_df)
print('info:\n')
# check column names

print("\nEuro:\n")
print(rev_euro_df[rev_columns]) 

print("\nGBP:\n")

print(rev_gbp_df[rev_columns]) 
print("\nUSD:\n")
print(rev_usd_df[rev_columns]) 

print("\n--------------------------------------------------------\n")
print(f"{RED} santander {RESET}")
print("\n--------------------------------------------------------\n")
print(san.info())
print("\nTransactions\n")

print(san)


