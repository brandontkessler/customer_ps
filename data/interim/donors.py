from user_inputs import last_day_of_last_fy, first_day_of_first_fy
from data.functions.date_conversions import date_conv
from data.functions.data_import import donor_data_import

donor_copy = donor_data_import()

date_to_use = 'trn_dt'
new_date_column = 'transaction_date'

# Split at the space because of weird date formatting in some years
donor_copy[new_date_column] = donor_copy[date_to_use].str.split(" ").str[0]
# Convert transaction_date
donor_copy[new_date_column] = date_conv(donor_copy[new_date_column])

# Include only donor data within the required time frame
# Create list checking if row contains correct fy
donor_date_filter = (donor_copy[new_date_column] <= last_day_of_last_fy) &\
    (donor_copy[new_date_column] >= first_day_of_first_fy)

donor_copy = donor_copy.loc[donor_date_filter]

# create a new column for transaction type
donor_copy = donor_copy.assign(transaction_type='donation')

# Exclude unnecessary columns
donor_cols = ['summary_cust_id', new_date_column, 'transaction_type', 
              'gift_plus_pledge', 'campaign', 'fund_desc']
donor_copy = donor_copy.loc[:, donor_cols]
donor_copy.columns = ["customer_id", new_date_column, "transaction_type", 
              "transaction_amount", 'campaign', 'fund_desc']