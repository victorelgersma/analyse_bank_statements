
import pandas as pd

rev_euro_df = pd.read_csv('../data/rev/eur/oct.csv')
rev_gbp_df = pd.read_csv('../data/rev/gbp/oct.csv')
rev_usd_df = pd.read_csv('../data/rev/usd/oct.csv')
san = pd.read_csv('../data/san/oct.csv', sep=';', encoding='ISO-8859-1') # maybe I should add the transactions in savings account

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

print("\nSantander \n")
print(san.info())
print("\nTransactions\n")
print(san[san_columns])
