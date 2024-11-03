
import pandas as pd

rev_euro_df = pd.read_csv('../data/rev/eur/oct.csv')
rev_gbp_df = pd.read_csv('../data/rev/gbp/oct.csv')
rev_usd_df = pd.read_csv('../data/rev/usd/oct.csv')

rev_columns=["Amount", "Description", "Completed Date"]

print("Revolut:\n")
print("data structure")
print(rev_euro_df.info()) 

# print(rev_df)
print('info:\n')
# check column names



print("Euro:\n")
print(rev_euro_df[rev_columns]) 

print("GBP:\n")

print(rev_gbp_df[rev_columns]) 
print("USD:\n")
print(rev_usd_df[rev_columns]) 
