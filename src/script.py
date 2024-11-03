"""
Note: this does not take into account the money moved into my vanguard account
"""

import chardet
from pathlib import Path
import pandas as pd

MONTH = 'oct'

EUR_TO_GBP = 0.8
USD_TO_GBP = 0.6

account_summary_list = []

san_paths=['../data/san/current/oct.html', '../data/san/saver/oct.html' ]
rev_paths = ['../data/rev/eur/oct.csv', '../data/rev/gbp/oct.csv', '../data/rev/usd/oct.csv']

def hor_rule():
    print("-" * 56)

def detect_currency(df):
    """Detects the currency of transactions in a DataFrame based on the 'Currency' column.
       If no currencies are present, it returns 'GBP'.
       If multiple currencies are present, it returns 'Mixed Currencies'."""
    # Get unique currencies in the column
    currencies = df['Currency'].dropna().unique()
    
    # Check for no currencies
    if len(currencies) == 0:
        return "GBP"
    
    # Check for a single unique currency
    if len(currencies) == 1:
        return currencies[0]
    
    # Return mixed if multiple currencies are present
    return "Mixed Currencies"

def title(account_name, color):
    hor_rule()
    print(f"{color} {account_name.upper()}  - TRANSACTIONS {RESET}")
    hor_rule()

def display_profit(profit, currency):
    hor_rule()
    print(f"profit: \t\t\t  {profit}  {currency}")
    print("\n")
    print("\n")


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

SAN_COLUMNS=["Date", "Description", "Amount"]

def display_transactions(df, cols):
    print(df[cols])
    profit = round(df["Amount"].sum(),2)
    display_profit(str(profit), "GBP")

for index, path in enumerate(rev_paths):
    REV_COLUMNS=["Amount", "Description", "Completed Date", "Currency"]
    df = pd.read_csv(path)
    print(f"Revolut Statement {index+1}\n")
    display_transactions(df, REV_COLUMNS)

print("Santander")

for path in san_paths:
    df = get_df_san(path)
    df = clean_san(df)
    print('\n')
    display_transactions(df, SAN_COLUMNS)

import pandas as pd

# Create a DataFrame for a single transaction to Vanguard
vanguard_transaction = pd.DataFrame({
    'Description': ['Added to Vanguard account'],
    'Amount': [250],
    'Currency': ['GBP'],  # Specify GBP since it's in GBP
    'Account': ['Vanguard']
})

display_transactions(vanguard_transaction, ["Description", "Amount", "Currency", "Account"])


