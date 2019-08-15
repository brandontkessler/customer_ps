from data.interim.all_tickets import tix_prep
from data.interim.donors import donor_copy

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

is_last_5years = donor_to_manip['transaction_date'] >= dt(2014, 7, 1)
donor_to_manip = donor_to_manip[is_last_5years]

donor_to_manip['year'] = [i.timetuple().tm_year + fy_check(i.timetuple().tm_mon)\
            for i in donor_to_manip['transaction_date']]

donor_to_manip.drop(['transaction_date','transaction_type'], inplace=True, axis=1)
donor_to_manip = donor_to_manip.groupby(['year','customer_id']).sum().reset_index()


#################
# List Building

is_sub_or_flex = ['sub', 'flex']
subs = tix_to_manip.loc[tix_to_manip['transaction_type'].isin(is_sub_or_flex)]

is_single_or_discount = ['single', 'discount']
single = tix_to_manip.loc[tix_to_manip['transaction_type'].isin(is_single_or_discount)]
comp = tix_to_manip.loc[tix_to_manip['transaction_type'] == 'comp']

filtered_subs = subs[['year','customer_id']].drop_duplicates()
filtered_single = single[['year','customer_id']].drop_duplicates()
filtered_comp = comp[['year','customer_id']].drop_duplicates()

# Check if singles are also subs in that same year.
filtered_single = pd.merge(filtered_single, filtered_subs, 
                           on=['year', 'customer_id'], how='left',
                           indicator='subscriber')
filtered_single = filtered_single[filtered_single['subscriber'] == 'left_only']
filtered_single.drop('subscriber', inplace=True, axis=1)

# Check if comps are also subs or singles in that same year.
filtered_comp = pd.merge(filtered_comp, filtered_subs,
                         on=['year','customer_id'], how='left',
                         indicator='subscriber')
filtered_comp = pd.merge(filtered_comp, filtered_single,
                         on=['year','customer_id'], how='left',
                         indicator='single')
filtered_comp = filtered_comp[filtered_comp['subscriber'] == 'left_only']
filtered_comp = filtered_comp[filtered_comp['single'] == 'left_only']
filtered_comp.drop(['subscriber', 'single'], inplace=True, axis=1)


filtered_no_attendee = pd.merge(donor_to_manip, filtered_subs,
                             on=['year','customer_id'], how='left',
                             indicator='sub')
filtered_no_attendee = pd.merge(filtered_no_attendee, filtered_single,
                             on=['year','customer_id'], how='left',
                             indicator='single')
filtered_no_attendee = pd.merge(filtered_no_attendee, filtered_comp,
                             on=['year','customer_id'], how='left',
                             indicator='comp')
filtered_no_attendee = filtered_no_attendee[filtered_no_attendee['sub'] == 'left_only']
filtered_no_attendee = filtered_no_attendee[filtered_no_attendee['single'] == 'left_only']
filtered_no_attendee = filtered_no_attendee[filtered_no_attendee['comp'] == 'left_only']
filtered_no_attendee.drop(['sub', 'single', 'comp'], inplace=True, axis=1)

#######################
# Merge with donation data

final_subs = pd.merge(filtered_subs, donor_to_manip, on=['year','customer_id'],
                      how='left')
final_subs['trn_type'] = 'subscriber'

final_single = pd.merge(filtered_single, donor_to_manip, on=['year','customer_id'],
                      how='left')
final_single['trn_type'] = 'single'

final_comp = pd.merge(filtered_comp, donor_to_manip, on=['year','customer_id'],
                      how='left')
final_comp['trn_type'] = 'comp'

final_no_attendee = filtered_no_attendee.copy()
final_no_attendee['trn_type'] = 'no_attendee'


###############
# Combined
final_combo = pd.concat([final_subs,final_single,final_comp,final_no_attendee])
final_combo = final_combo.groupby(['trn_type', 'year']).agg({
                'customer_id': {
                    'customer_count': 'count',
                },
                'transaction_amount': {
                    'donor_count': 'count',
                    'donation_amount': 'sum'
                }
            })
final_combo.columns = [x[1] for x in final_combo.columns.ravel()]
final_combo = final_combo.reset_index()
final_combo['donation_amount_per_customer'] = final_combo['donation_amount'] /\
    final_combo['customer_count']
final_combo['donation_amount_per_donating_customer'] =\
    final_combo['donation_amount'] / final_combo['donor_count']


############
# Write to excel
with pd.ExcelWriter('five_year_analysis.xlsx') as writer:
    pd.DataFrame(final_combo).to_excel(writer,
                                      engine='xlsxwriter', 
                                      index=False)

# Plots
# customers
final_combo.groupby(['trn_type','year'])['customer_count'].sum().unstack().plot(kind='bar',stacked=False, figsize=(10,5))
plt.title('Number of Customers')
plt.xticks(rotation=0)
plt.show()

# donors
final_combo.groupby(['trn_type','year'])['donor_count'].sum().unstack().plot(kind='bar',stacked=False, figsize=(10,5))
plt.title('Number of Donors')
plt.xticks(rotation=0)
plt.show()

# donation_amount
final_combo.groupby(['trn_type','year'])['donation_amount'].sum().unstack().plot(kind='bar',stacked=False, figsize=(10,5))
plt.title('Total Donation $')
plt.xticks(rotation=0)
plt.ylim(0,10000000)
plt.show()

# donation_amount_per customer
final_combo.groupby(['trn_type','year'])['donation_amount_per_customer'].sum().unstack().plot(kind='bar',stacked=False, figsize=(10,5))
plt.title('Total Donation $ per Customer')
plt.xticks(rotation=0)
plt.ylim(0,8000)
plt.show()

# donation_amount_per donor customer
final_combo.groupby(['trn_type','year'])['donation_amount_per_donating_customer'].sum().unstack().plot(kind='bar',stacked=False, figsize=(10,5))
plt.title('Total Donation $ per Donating Customer')
plt.xticks(rotation=0)
plt.ylim(0,20000)
plt.show()





