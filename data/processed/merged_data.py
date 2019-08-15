import pandas as pd
from user_inputs import fy_start, first_day_of_first_fy
from data.interim.donors import donor_copy
from data.interim.ticketing import tix_copy

combined_df = pd.concat([tix_copy, donor_copy])

# sort by transaction date
combined_df.sort_values(by='transaction_date', inplace=True)

# Add a fiscal year column
fy = fy_start
for i in range(10):
    combined_df.loc[(combined_df.transaction_date >= first_day_of_first_fy.replace(
                 first_day_of_first_fy.year + i
             )) & (combined_df.transaction_date < first_day_of_first_fy.replace(
                 first_day_of_first_fy.year + i + 1
             )), 'fy'] = fy
    fy += 1