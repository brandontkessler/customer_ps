import numpy as np
from data.processed.merged_data import combined_df


unique_patrons = combined_df['customer_id'].unique()
unique_concert_attendee = combined_df[
    (combined_df['transaction_type'] == 'single') | \
    (combined_df['transaction_type'] == 'sub') | \
    (combined_df['transaction_type'] == 'comp') | \
    (combined_df['transaction_type'] == 'flex')]['customer_id'].unique()
unique_donors = combined_df[combined_df['transaction_type'] == 'donation']\
    ['customer_id'].unique()
unique_subscribers = combined_df[combined_df['transaction_type'] == 'sub']\
    ['customer_id'].unique()
unique_flex = combined_df[combined_df['transaction_type'] == 'flex']\
    ['customer_id'].unique()
unique_comp = combined_df[combined_df['transaction_type'] == 'comp']\
    ['customer_id'].unique()

unique_single_paid =\
    combined_df[
        (combined_df['customer_id'].isin(unique_subscribers) == False) &\
        (combined_df['customer_id'].isin(unique_flex) == False) &\
        (combined_df['customer_id'].isin(unique_comp) == False) &\
        (combined_df['customer_id'].isin(unique_concert_attendee))]\
            ['customer_id'].unique()

unique_single_non_sub = combined_df[(combined_df['customer_id']\
                                    .isin(unique_subscribers) == False) &\
                                    (combined_df['customer_id'].isin(unique_concert_attendee))]\
                                    ['customer_id'].unique()
unique_attendee_donated = np.intersect1d(unique_donors, unique_concert_attendee)
unique_subscribers_donated = np.intersect1d(unique_donors, unique_subscribers)
unique_single_non_sub_donated = np.intersect1d(unique_donors, unique_single_non_sub)