from analysis.functions.ltv import LTV_improved
from data.interim.all_tickets import tix_prep
from data.interim.donors import donor_copy
from data.functions.data_import import donor_data_import
from data.functions.date_conversions import date_conv
from user_inputs import last_day_of_last_fy, first_day_of_first_fy

from datetime import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

##################
# Tix Formatting

clx = tix_prep('Clx')
pop = tix_prep('Pops')
chbr = tix_prep('Chamber')
con = tix_prep('Connections')
fam = tix_prep('Family')
org = tix_prep('Organ')
spc = tix_prep('Specials')
smr = tix_prep('Summer')


tix_copy = pd.concat([clx,pop,chbr,con,fam,org,spc], ignore_index=True)
dir(tix_copy)
tix_to_manip = tix_copy.copy()

def fy_check(month_number):
    if month_number < 7:
        return 0
    else:
        return 1


tix_to_manip['year'] = [i.timetuple().tm_year + fy_check(i.timetuple().tm_mon)\
            for i in tix_to_manip['performance_date']]

is_not_nan = pd.notna(tix_to_manip['customer_id'])
tix_to_manip = tix_to_manip[is_not_nan]


###################
# Donor Formatting

donor_to_manip = donor_copy.copy()

donor_to_manip['year'] = [i.timetuple().tm_year + fy_check(i.timetuple().tm_mon)\
            for i in donor_to_manip['transaction_date']]

donor_to_manip.drop(['transaction_date','transaction_type'], inplace=True, axis=1)
donor_to_manip = donor_to_manip.groupby(['year','customer_id']).sum().reset_index()


################
# List Creation - Box Circle
donor_copy2 = donor_data_import()
# Split at the space because of weird date formatting in some years
donor_copy2['transaction_date'] = donor_copy2['trn_dt'].str.split(" ").str[0]
# Convert transaction_date
donor_copy2['transaction_date'] = date_conv(donor_copy['transaction_date'])

# Include only donor data within the required time frame
# Create list checking if row contains correct fy
donor_date_filter2 = (donor_copy2['transaction_date'] <= last_day_of_last_fy) &\
    (donor_copy2['transaction_date'] >= first_day_of_first_fy)

donor_copy2 = donor_copy2.loc[donor_date_filter2]

# create a new column for transaction type
donor_copy2 = donor_copy2.assign(transaction_type='donation')
donor_for_list = donor_copy2.copy()


box_circle_list = donor_for_list[donor_for_list['campaign'].str.contains("Box Circle")].reset_index()
box_circle_list = box_circle_list.summary_cust_id
box_circle_list = set(box_circle_list)


###########################
# Combine tix and donors:
donor_to_manip = donor_to_manip[['year', 'customer_id', 'transaction_amount']]
tix_to_manip = tix_to_manip[['year', 'customer_id', 'transaction_amount']]
combined_df = pd.concat([tix_to_manip, donor_to_manip])
combined_df = combined_df.rename({"year": "fy"}, axis='columns')


##########################
LTV_improved(combined_df, box_circle_list)