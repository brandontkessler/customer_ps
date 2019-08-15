#### OBJECTIVE
# Determine number of concert purchases prior to first donation
# Determine number of concert purchases prior to first subscription

# Steps/Sections:
#   Section1 - global
#   *) Imports
#   *) User Inputs
#   *) Reusable Functions
#
#   Section2 - setup
#   1) Bring in Ticketing Data
#   2) Format Ticketing Data
#   3) Bring in Donor Data
#   4) Format Donor Data
#   5) Merge Ticketing and Donor Data
#
#   Section3 - analysis
#   1) Exploratory / Filtered List Creation
#   2) Number of Single Concerts Before Subscription
#   3) Number of Concerts Before First Donation
#   4) Number of Concerts Before First Donation for Subs
#   5) Number of Concerts Before First Donation for Singles
#   6) Number of Concerts by Singles that Never Sub
#   6) Lapsed Subscribers that Continue to Attend/Donate
#   *) LTV of Classics Customers
#
#   Concerts Before First Donation is shortened to "cbfd" in code

# Req Format:
#   customer_id, transaction_date, transaction_type, transaction_amount
#
#   From Ticketing:
#       summary_cust_id, order_dt, price_type_group, paid_amt
#
#   From Donors:
#       summary_cust_id, trn_dt, < new column >, gift_plus_pledge
#
# Description:
#   The data from ticketing and donors will rename the columns to match the
#   required format. The < new column > in donors will be filled with data
#   to match "donation" in order to separate from the ticketing types from
#   the ticketing data.
#
#   We use trn_dt instead of cont_dt because we are interested in the trigger
#   point of when the person makes the decision to make the donation, not 
#   necessarily when the donation impacts the financials. Therefore we care
#   about when the commitment is made.
########

###############################################################################
# SECTION 1

#### * Imports
import pandas as pd
import numpy as np
import datetime as dt
########

#### * User Inputs
first_day_of_first_fy = dt.datetime(2008, 7, 1)
last_day_of_last_fy = dt.datetime(2018, 6, 30)
fy_start = 2009
########

#### * Reusable Functions
# Convert column of dates to a datetime date
def date_conv(s):
    dates = {date:pd.to_datetime(date) for date in s.unique()}
    return s.map(dates)


def concerts_before_subscription(df, filter_list):
    """This function counts. Pass in the dataframe, pass in the list to filter,
    the dataframe to only include those
    
    Example: We can pass in our dataframe, with a list of only subs, to see
    the number of concerts singles attend before making their first 
    subscription
    
    Returns: The number of concert attendances before subscription attendance
    """
    
    # Filter non-subscribers from the dataframe provided as well
    df = df[df['customer_id'].isin(filter_list)]
    
    # Creating an array of arrays of length two
    # The first val of array represents tickets purchased before subscription
    # The second val represents a boolean that prevents the loop from adding more
    # once a person subscribes
    counting_array = np.zeros(2, dtype=int)
    resulting_array = np.tile(counting_array, (len(filter_list), 1))
    
    # Zips into a dictionary
    resulting_dictionary = dict(zip(filter_list, resulting_array))
    
    for customer, _, trn_type, _2, _3 in df.itertuples(index=False):
        
        # Check if customer has purchased a ticket AND stop has been verified
        if resulting_dictionary[customer][0] > 0 & resulting_dictionary[customer][1] >= 1:
            continue
        
        # Check if sale type is a non-sub ticket
        if trn_type == 'single' or trn_type == 'comp' or trn_type == 'flex':
            resulting_dictionary[customer][0] += 1
        elif trn_type == "sub":
            resulting_dictionary[customer][1] = 1
        elif trn_type == "donation":
            continue
        else:
            print("error")

    
    # Check total concerts attended by all patrons prior to their first subscription
    total_concerts_before_sub = 0
    for k, v in resulting_dictionary.items():
        total_concerts_before_sub += v[0]

    # average number of concerts attended before first subscription
    avg_concerts_before_sub =\
        total_concerts_before_sub / len(resulting_dictionary)

    return avg_concerts_before_sub


def concerts_before_donation_counter(df, filter_list):
    """This function counts. Pass in the dataframe, pass in the list to filter,
    the dataframe to only include those
    
    Example: We can pass in our dataframe, with a list of only subs, to see
    the number of concerts subscribers attend before making their first 
    donation
    
    Returns: A list containing avg concert count in the 0 index and the 
    average donation amount for the initial donation in the 1 index.
    """

    
    # Filter non-subscribers from the dataframe provided as well
    df = df[df['customer_id'].isin(filter_list)]
    
    # Creating an array of arrays of length two
    # The first val of array represents tickets purchased before subscription
    # The second val represents a boolean that prevents the loop from adding more
    # once a person subscribes
    counting_array = np.zeros(2, dtype=int)
    resulting_array = np.tile(counting_array, (len(filter_list), 1))
    
    # Zips into a dictionary
    resulting_dictionary = dict(zip(filter_list, resulting_array))
    
    for customer, _, trn_type, trn_amt, _2 in df.itertuples(index=False):
        
        # Check if customer has purchased a ticket AND stop has been verified
        if resulting_dictionary[customer][0] > 0 & resulting_dictionary[customer][1] >= 1:
            continue
        
        # Count transactions before first donation, fill donation w/ trn_amt
        if trn_type == 'single' or trn_type == 'comp' or trn_type == 'flex' or\
                trn_type == 'sub':
            resulting_dictionary[customer][0] += 1
        elif trn_type == "donation":
            if resulting_dictionary[customer][1] < 1:
                resulting_dictionary[customer][1] = trn_amt
        else:
            print("error")

    
    # Init the concert counter and the checker amount
    concerts = 0
    checker = 0
    
    # Count total concert, count total checkers
    for k, v in resulting_dictionary.items():
        concerts += v[0]
        checker += v[1]


    avg_concerts = concerts / len(resulting_dictionary)
    avg_checker = checker / len(resulting_dictionary)

    return [avg_concerts, avg_checker]


def total_concerts_filtered(df, filter_list):
    """This function counts. Pass in the dataframe, pass in the list to filter,
    the dataframe to only include those
    
    Example: We can pass in our dataframe, with a list of only subs, to see
    the number of concerts singles attend in total
    
    Returns: The number of concert attendances
    """
    
    # Filter from the dataframe provided
    df = df[df['customer_id'].isin(filter_list)]
    
    return int(len(df))


def LTV_basic(df, filter_list):
    """This function calculates lifetime value in a basic way.
    
    Here, we simply sum the total transaction amount divided by the total 
    unique customers. We use this across a ten year period to describe our
    basic lifetime value.
    
    Pass in the dataframe, pass in the list to filter,
    the dataframe to only include those
    
    Example: We can pass in our dataframe, with a list of only subs, to see
    the LTV of that group
    
    Returns: The total spend per customer in the 10 year period
    """
    
    # Filter from the dataframe provided
    df = df[df['customer_id'].isin(filter_list)]
    
    ltv = sum(df['transaction_amount']) / len(df['customer_id'].unique())
    
    return ltv


def LTV_improved(df, filter_list):
    """This function calculates lifetime value in an improved way.
    
    This calculates the many pieces that go into calculating lifetime value
    for each individual customer and then as a whole.
    
    It allows us to filter by specific lists of customers as well.
    
    Example: We can pass in our dataframe, with a list of only subs, to see
    the LTV of that group
    
    Returns: A dictionary containing: average transaction value, average
        frequency of transactions per year, average customer value, 
        average lifespan, and lifetime value
    """
    
    # Filter from the dataframe provided
    df = df[df['customer_id'].isin(filter_list)]
    
    # Initialize the resulting dictionary
    res_dict = dict(avg_transaction_value=0, avg_frequency_rate=0, 
                    avg_customer_value=0, avg_lifespan=0, ltv=0)

    # Build the dataframe that contains the calculations for each customer
    df_res = df.groupby(['customer_id']).agg(
            {'transaction_amount': ['mean','count'], 'fy': 'nunique'})
    df_res.columns = ['average_transaction_amt','count_of_transactions','count_of_fy']
    df_res['freq'] = df_res['count_of_transactions'] / df_res['count_of_fy']
    df_res['customer_value'] = df_res['freq'] * df_res['average_transaction_amt']
    
    # Transaction value calc
    avg_transaction = np.mean(df_res['average_transaction_amt'])
    
    # Transaction Frequency Rate (per year)
    frequency = np.mean(df_res['freq'])
    # NOTE: frequency of purchase spreads subscription purchases across the 
    #   actual concerts themselves and are not counted as one bulk purchase.
    
    # Customer Value
    customer_val = np.mean(df_res['customer_value'])
    
    # Lifespan calc
    lifespan = sum(df_res['count_of_fy']) / len(df_res)
    
    #ltv
    ltv = lifespan * customer_val
    
    res_dict['avg_transaction_value'] = avg_transaction
    res_dict['avg_frequency_rate'] = frequency
    res_dict['avg_customer_value'] = customer_val
    res_dict['avg_lifespan'] = lifespan
    res_dict['ltv'] = ltv

    return res_dict

########

###############################################################################
# SECTION 2

#### 1) Bring in Ticketing Data
path = "../../data/ticketing/"

tix_raw = pd.concat([
    pd.read_csv(path + "Clx18.csv", skiprows=3),
    pd.read_csv(path + "Clx17.csv", skiprows=3),
    pd.read_csv(path + "Clx16.csv", skiprows=3),
    pd.read_csv(path + "Clx15.csv", skiprows=3),
    pd.read_csv(path + "Clx14.csv", skiprows=3),
    pd.read_csv(path + "Clx13.csv", skiprows=3),
    pd.read_csv(path + "Clx12.csv", skiprows=3),
    pd.read_csv(path + "Clx11.csv", skiprows=3),
    pd.read_csv(path + "Clx10.csv", skiprows=3),
    pd.read_csv(path + "Clx09.csv", skiprows=3)
], ignore_index=True)

tix_copy = tix_raw.copy() # make a copy of raw data
########



#### 2) Format Ticketing Data
# Check if ticket was sold
sold_ticket = tix_copy['summary_cust_id'] > 0

# Remove unsold tickets
tix_copy = tix_copy[sold_ticket]

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
tix_cols = ['summary_cust_id', 'order_dt', 'price_type_group', 'paid_amt']
tix_copy = tix_copy.loc[:, tix_cols]
tix_copy.columns = ["customer_id", "transaction_date", "transaction_type", 
              "transaction_amount"]

# Exclude repeat columns (These would appear if one person bought multiple
# tickets to the same concert. We want to isolate one customer per concert)
tix_copy = tix_copy.drop_duplicates()
########



#### 3) Bring in Donor Data
d_path = "../../data/donors/"

donor_raw = pd.read_csv(d_path + "donors_fy08-fy19.csv", encoding='ISO-8859-1')

donor_copy = donor_raw.copy() # Copy raw donor data
########



#### 4) Format Donor Data
# Split at the space because of weird date formatting in some years
donor_copy['transaction_date'] = donor_copy['trn_dt'].str.split(" ").str[0]
# Convert transaction_date
donor_copy['transaction_date'] = date_conv(donor_copy['transaction_date'])

# Include only donor data within the required time frame
# Create list checking if row contains correct fy
donor_date_filter = (donor_copy['transaction_date'] <= last_day_of_last_fy) &\
    (donor_copy['transaction_date'] >= first_day_of_first_fy)

donor_copy = donor_copy.loc[donor_date_filter]

# create a new column for transaction type
donor_copy = donor_copy.assign(transaction_type='donation')

# Exclude unnecessary columns
donor_cols = ['summary_cust_id', 'transaction_date', 'transaction_type', 
              'gift_plus_pledge']
donor_copy = donor_copy.loc[:, donor_cols]
donor_copy.columns = ["customer_id", "transaction_date", "transaction_type", 
              "transaction_amount"]
########



#### 5) Merge Ticketing and Donor Data
# merge
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
########


###############################################################################
# SECTION 3

#### 1) Exploratory/List Creation

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

# First package is fixed

# First package is flex


########


#### 2) Number of Single Concerts Before Subscription
# Note: Only includes patrons that purchased a subscription
res_concerts_b4_subscribing = concerts_before_subscription(combined_df, unique_subscribers)
########



#### 3) Number of Concerts Before First Donation
# Note: Only includes patrons that made a donation and attended at least one concert
ret_cbfd_all = concerts_before_donation_counter(combined_df, unique_attendee_donated)
res_avg_concerts_cbfd_all = ret_cbfd_all[0]
res_avg_first_donation_cbfd_all = ret_cbfd_all[1]
########



#### 4) Number of Concerts Before First Donation for Subs
# Note: Only includes patrons that purchased a subscription and made a donation
ret_cbfd_sub = concerts_before_donation_counter(combined_df, unique_subscribers_donated)
res_avg_concerts_cbfd_sub = ret_cbfd_sub[0]
res_avg_first_donation_cbfd_sub = ret_cbfd_sub[1]
########



#### 5) Number of Concerts Before First Donation for Singles
# Note: Only includes patrons that never subscribed and made a donation and attended
#   at least one concert
ret_cbfd_sgl = concerts_before_donation_counter(combined_df, unique_single_non_sub_donated)
res_avg_concerts_cbfd_sgl = ret_cbfd_sgl[0]
res_avg_first_donation_cbfd_sgl = ret_cbfd_sgl[1]
######## 


#### 6) Number of Concerts Attended by Singles that Don't Sub
res_avg_concerts_non_subs =\
    total_concerts_filtered(combined_df, unique_single_non_sub)\
    / len(unique_single_non_sub)
########
    
    
#### 7) Number of Concerts Attended by Singles PAID (non sub,flex,comp)
res_avg_concert_paid_singles_only =\
    total_concerts_filtered(combined_df, unique_single_paid)\
    / len(unique_single_paid)
########
    

#### 8) Lifetime Value Basic
ltv_basic = LTV_basic(combined_df, unique_concert_attendee)
ltv_basic_subs = LTV_basic(combined_df, unique_subscribers)
########



#### 9) Lifetime Value Improved
ltv_improved = LTV_improved(combined_df, unique_concert_attendee)
ltv_improved_single = LTV_improved(combined_df, unique_single_non_sub)
ltv_improved_subs = LTV_improved(combined_df, unique_subscribers)
########









