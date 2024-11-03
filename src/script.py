"""
Note: this does not take into account the money moved into my vanguard account
"""

import chardet
from pathlib import Path
import pandas as pd

MONTH = 'oct'

# ANSI escape codes for colors
RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"

EUR_TO_GBP = 0.8
USD_TO_GBP = 0.6

# Relevant columns

vanguard_transaction = pd.DataFrame({
    'Date': ['2024-11-03'],  
    'Description': ['Added to Vanguard account'],
    'Amount': [250],
    'Currency': ['GBP'],
    'Account': ['Vanguard']
})

san_paths=['../data/san/current/oct.html', '../data/san/saver/oct.html' ]
rev_paths = ['../data/rev/eur/oct.csv', '../data/rev/gbp/oct.csv', '../data/rev/usd/oct.csv']

def hor_rule():
    print("\n" + "-" * 56)

def detect_currency(df):
    """Detects the currency of transactions in a DataFrame based on the 'Currency' column.
       If multiple currencies are present, it returns 'Mixed Currencies'."""
    currencies = df['Currency'].unique()
    if len(currencies) == 1:
        return currencies[0]
    return "Mixed Currencies"

def title(account_name, color):
    hor_rule()
    print(f"{color} {account_name.upper()}  - TRANSACTIONS {RESET}")
    hor_rule()

def pretty_print_profit(profit, currency):
    hor_rule()
    print(f"profit: \t  {profit}  {currency}")

def analyze_rev(path):
    REV_COLUMNS=["Amount", "Description", "Completed Date", "Currency"]
    df = pd.read_csv(path)
    print('\n')
    print("data types:")
    hor_rule()
    print(df.dtypes)
    print('\n')
    print("transactions:")
    hor_rule()
    print(df[REV_COLUMNS], "\n")
    pretty_print_profit(f"{round(df['Amount'].sum(), 2)}", detect_currency(df))
    

def get_encoding(path):
    with open(path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
        print(f"Detected encoding: {encoding}")
    return encoding

def clean_currency_columns(df):
    # numbers should be floats
    df['Money in'] = df['Money in'].str.replace('£', '').str.replace(',', '').astype(float)
    df['Money Out'] = df['Money Out'].str.replace('£', '').str.replace(',', '').astype(float)
    # Replace NaNs with 0
    df['Money in'] = df['Money in'].fillna(0)
    df['Money Out'] = df['Money Out'].fillna(0)
    return df

def get_df_san(path):
    SAN_COLUMNS=["Date", "Description", "Money Out", "Money in"]
    """return a df with the header containing the right titles"""
    encoding = get_encoding(path)
    df = pd.read_html(Path(path), encoding=encoding, header =3)[0]
    return df[SAN_COLUMNS]

def clean_san(df):
    df = clean_currency_columns(df)
    df["Amount"] = - df["Money Out"] + df["Money in"]
    return df

def analyze_san(path):
    SAN_COLUMNS=["Date", "Description", "Amount"]
    df = get_df_san(path)
    df = clean_san(df)
    print(df.dtypes)
    print(df[SAN_COLUMNS])
    pretty_print_profit(str(round(df["Amount"].sum(),2)), "GBP")

title("Revolut", BLUE)

for index, path in enumerate(rev_paths):
    print(f"\n \t\tStatement {index+1}\n")
    analyze_rev(path)

title("Santander", RED)

for statement in san_paths:
    print('\n')
    analyze_san(statement)





