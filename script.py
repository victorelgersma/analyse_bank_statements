
import pandas as pd

rev_df = pd.read_csv('transactions/rev/eur/oct.csv')

# print(rev_df)
print('shape: ' + str(rev_df.shape))
print('info:\n')
print(rev_df.info())
print(rev_df.head())
