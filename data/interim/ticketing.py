import numpy as np
from user_inputs import first_day_of_first_fy, last_day_of_last_fy, series
from data.functions.date_conversions import date_conv
from data.functions.data_import import ticketing_data_import


tix_copy = ticketing_data_import(series)

real_customer = tix_copy['summary_cust_id'] > 0

# Remove non-real customers
tix_copy = tix_copy[real_customer]

# Convert order_dt
tix_copy['order_dt'] = date_conv(tix_copy['order_dt'])

# Include only ticketing data within the required time frame
# Create list checking if row contains correct fy
tix_date_filter = (tix_copy['order_dt'] <= last_day_of_last_fy) &\
    (tix_copy['order_dt'] >= first_day_of_first_fy)

tix_copy = tix_copy.loc[tix_date_filter]

# Adjust transaction types to match subscription, flex, single, or comp
current_price_types = tix_copy.price_type_group.unique()
matching_price_types = np.array(["sub","flex","single","comp","single","single"])
price_type_dict = dict(zip(current_price_types, matching_price_types))

tix_copy['price_type_group'] = tix_copy['price_type_group'].map(price_type_dict)

# Exclude unnecessary columns
tix_cols = ['summary_cust_id', 'order_dt', 'price_type_group', 'paid_amt', 'attended']
tix_copy = tix_copy.loc[:, tix_cols]
tix_copy.columns = ["customer_id", "transaction_date", "transaction_type", 
              "transaction_amount", "attended"]

# Exclude repeat columns (These would appear if one person bought multiple
# tickets to the same concert. We want to isolate one customer per concert)
tix_copy = tix_copy.drop_duplicates()