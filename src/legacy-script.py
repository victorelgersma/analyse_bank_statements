
# LEGACY - I will keep this around because there were some good ideas in here
# the use of ipynb pretty much makes this pointless

from datetime import datetime
import chardet
from pathlib import Path
import pandas as pd

date = datetime(2024, 10, 1)
month_abbr =date.strftime('%b').lower() # 'oct'

pd.set_option('display.max_rows', None)
EUR_TO_GBP = 0.84
USD_TO_GBP = 0.77

# Columns of cleaned df:
COLUMNS=["Amount", "Description", "Date", "Currency"]

san_paths = [f'../data/san/current/{month_abbr}.html', f'../data/san/saver/{month_abbr}.html']
rev_paths = [f'../data/rev/eur/{month_abbr}.csv', f'../data/rev/gbp/{month_abbr}.csv', f'../data/rev/usd/{month_abbr}.csv']


# Printing functions
def hor_rule():
    print("-" * 56)

def display_profit(profit, currency):
    hor_rule()
    print(f"\tprofit: \t\t\t  {profit}  {currency}")
    print("\n")
    print("\n")

def get_currency(df):
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
    df["Currency"] = "GBP"
    return df

def get_profit(df):
    return round(df["Amount"].sum(),2)


def clean_rev(df):
    df["Date"] = df["Completed Date"]
    return df


def process(dfs, df, name):
    " Once the data frame is in the right format, this is the handler function"
    profit = get_profit(df)
    currency = get_currency(df)
    account_summary_list.append([name, profit, currency])
    print(name)
    hor_rule()
    df = df[COLUMNS]
    print(df)
    dfs.append(df)
    display_profit(str(profit), currency)

def get_combined_df(dfs, axis=0):
    """
    Combines a list of DataFrames along the specified axis.
    
    Parameters:
    dfs (list of pd.DataFrame): The DataFrames to combine.
    axis (int): The axis to concatenate along (0 for rows, 1 for columns).
    
    Returns:
    pd.DataFrame: The combined DataFrame.
    """
    return pd.concat(dfs, axis=axis)

account_summary_list = []
dfs = []
print('\n')
for index, path in enumerate(rev_paths):
    df = pd.read_csv(path)
    df = clean_rev(df)
    print(df)
    name = f"Revolut Statement {index +1}"
    process(dfs, df, name)


print("Santander")


for index, path in enumerate(san_paths):
    df = clean_san(get_df_san(path))
    print(df)
    name = f"Santander Statement {index +1}"
    process(dfs, df, name)
account_summary_list.append(["Vanguard", 250, "GBP"])

df = pd.DataFrame(account_summary_list, columns=["Account", "Profit", "Currency"])



# TODO - reset indexes for these
# TODO - add column for account name to keep track of this
# Do all subsequent analysis on the combined data frame
print("Combined DF (all transactions)")
combined_df = get_combined_df(dfs)

# fix times to be same format
combined_df['Date'] = pd.to_datetime(combined_df['Date'], errors='coerce', dayfirst=True)

print(combined_df)

def add_gbp_column(df):
    """
    Add a 'Profit (GBP)' column to the DataFrame by converting the 'Profit' column based on 'Currency'.

    Parameters:
    df (pd.DataFrame): DataFrame with 'Profit' and 'Currency' columns.

    Returns:
    pd.DataFrame: DataFrame with a new 'Profit (GBP)' column.
    """
    # Define a conversion function for each row
    def convert_to_gbp(row):
        if row['Currency'] == 'EUR':
            return row['Profit'] * EUR_TO_GBP
        elif row['Currency'] == 'USD':
            return row['Profit'] * USD_TO_GBP
        return row['Profit']  # GBP remains the same
    
    # Apply conversion function to create 'Profit (GBP)' column
    df['Profit (GBP)'] = df.apply(convert_to_gbp, axis=1)
    return df

df = add_gbp_column(df)
print(df)

total_profit = round(df["Profit (GBP)"].sum(), 2)
print("\n TOTAL PROFIT: \n")
print(f"{total_profit} GBP")


