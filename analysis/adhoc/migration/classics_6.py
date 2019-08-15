import os
import pandas as pd

clx_subs_19 = pd.read_csv(os.getcwd() + '/data/raw/clx19_subs.csv')
clx_subs_20 = pd.read_csv(os.getcwd() + '/data/raw/clx20_subs.csv')


sixes = ['Clx Thu Romantic 6', 'Clx Fri Romantic 6', 'Clx Sat Romantic 6', 
 'Clx Thu Escapes 6', 'Clx Fri Escapes 6', 'Clx Sat Escapes 6',
 'Clx Sat Escapes Peel 4', 'Clx Fri Escapes Peel 4',
 'Clx Thu Escapes Peel 4', 'Clx Fri Romantic Peel 5', 'Clx Sat Romantic Peel 5', 
 'Clx Thu Romantic Peel 5']

def includer(val):
    return True if val in sixes else False

clx_subs_19['sixes'] = clx_subs_19.season.apply(includer)

clx_sixes_19 = clx_subs_19.loc[clx_subs_19['sixes']]

unique_customers = clx_sixes_19.customer_no.unique()


def sub_6_in_19(val):
    return True if val in unique_customers else False

clx_subs_20_filtered = clx_subs_20.loc[clx_subs_20.customer_no.apply(sub_6_in_19)]


migration_summary = pd.DataFrame(clx_subs_20_filtered.season.value_counts())


to_append = pd.DataFrame(data=[len(unique_customers) - sum(migration_summary.season)], 
                               index=['lapsed'], columns=['season'])

migration_summary = migration_summary.append(to_append)

migration_summary.rename(columns={'season': 'count'}, inplace=True)

migration_summary['percentage'] = migration_summary['count'] /\
     sum(migration_summary['count'])
     

############
# Write to excel
with pd.ExcelWriter('clx6_fy19_migration.xlsx') as writer:
    pd.DataFrame(migration_summary).to_excel(writer,
                                      engine='xlsxwriter', 
                                      index=True)