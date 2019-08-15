import numpy as np
from user_inputs import first_day_of_first_fy, last_day_of_last_fy
from data.functions.date_conversions import date_conv
from data.functions.data_import import ticketing_data_import

def tix_prep(series):
    tix_copy = ticketing_data_import(series)
    
    # Convert perf_dt
    tix_copy['perf_dt'] = date_conv(tix_copy['perf_dt'])
    
    # Include only ticketing data within the required time frame
    # Create list checking if row contains correct fy
    tix_date_filter = (tix_copy['perf_dt'] <= last_day_of_last_fy) &\
        (tix_copy['perf_dt'] >= first_day_of_first_fy)
    
    tix_copy = tix_copy.loc[tix_date_filter]
    
    # Adjust transaction types to match subscription, flex, single, or comp
    matching_price_types = {
                'Single ': 'single',
                'Subscription': 'sub',
                'Comp': 'comp',
                'Flex': 'flex',
                'Discount': 'discount'
            }

    tix_copy['price_type_group'] = tix_copy['price_type_group'].map(matching_price_types)
    
    # Exclude unnecessary columns
    tix_cols = ['summary_cust_id', 'perf_dt', 'price_type_group', 'paid_amt', 'attended']
    tix_copy = tix_copy.loc[:, tix_cols]
    tix_copy.columns = ["customer_id", "performance_date", "transaction_type", 
                  "transaction_amount", "attended"]

    return tix_copy

