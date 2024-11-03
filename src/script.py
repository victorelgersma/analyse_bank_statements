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

san_paths=['../data/san/current/oct.html', '../data/san/saver/oct.html' ]
rev_paths = ['../data/rev/eur/oct.csv', '../data/rev/gbp/oct.csv', '../data/rev/usd/oct.csv']

def title(account_name, color):
    print("\n" + "-" * 56)
    print(f"{color} {account_name.upper()}  - TRANSACTIONS {RESET}")
    print("\n" + "-" * 56 +"\n")


def analyze_rev(path):
    REV_COLUMNS=["Amount", "Description", "Completed Date", "Currency"]
    df = pd.read_csv(path)
    print(df.dtypes)
    print(df[REV_COLUMNS])
    print("profit", round(df["Amount"].sum(), 2))


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

def clean_san_df(df):
    df = clean_currency_columns(df)
    df["Amount"] = - df["Money Out"] + df["Money in"]
    return df

def analyze_san(path):
    SAN_COLUMNS=["Date", "Description", "Amount"]
    # clean
    df = get_df_san(path)
    df = clean_san_df(df)
    print(df.dtypes)
    print(df[SAN_COLUMNS])
    print("total money out", df["Money Out"].sum())
    print("total money in", df["Money in"].sum())
    print("sum", - df["Money Out"].sum() + df["Money in"].sum())

title("Revolut", BLUE)

for path in rev_paths:
    print('\n')
    analyze_rev(path)

title("Santander", RED)

for statement in san_paths:
    print('\n')
    analyze_san(statement)





