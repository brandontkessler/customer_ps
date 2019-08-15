import os
import pandas as pd

pop_subs = pd.read_csv(os.getcwd() + '/data/raw/pop20_subs.csv')
pop_tix = pd.read_csv(os.getcwd() + '/data/raw/Pops20.csv', skiprows=3)


filtered_subs = pop_subs.loc[pop_subs.season == 'PS 19-20 Pops CYO 4']
filtered_subs['foo'] = 1
filtered_subs = filtered_subs[['customer_no', 'foo']]

filtered_tix = pop_tix[['perf_dt','customer_no','attended']].drop_duplicates()


combined = pd.merge(filtered_tix, filtered_subs, how='left', on='customer_no')

combined = combined.loc[combined.foo.notna()]

combined['attended'] = combined['attended'].fillna(value='No_Attend')

combined = combined.groupby(['perf_dt','attended']).count().reset_index()[['perf_dt','attended','foo']]

############
# Write to excel
with pd.ExcelWriter('pops_cyo4_concerts.xlsx') as writer:
    pd.DataFrame(combined).to_excel(writer,
                                      engine='xlsxwriter', 
                                      index=False)