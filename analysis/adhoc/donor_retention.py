import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from data.interim.donors import donor_copy
from user_inputs import fy_start, first_day_of_first_fy


# Create substring of campaign column to determine fiscal year
donor_copy = donor_copy.reset_index(drop=True)
donor_copy.fy = donor_copy.campaign.str[3:8]

# Identify which 'fys' don't start with an integer, these we can remove
# Also, identify the years that are outside of the range in question
filter_fys = {fy: False for fy in donor_copy.fy.drop_duplicates()}
for fy,boo in filter_fys.items():
    try:
        int(fy[0])
        if (int(fy[3:]) > 9) & (int(fy[3:]) < 20):
            filter_fys[fy] = True
        else:
            continue
    except:
        continue

# Map the fy column to identify rows to remove then remove them
donor_copy['keep'] = donor_copy['fy'].map(filter_fys)
donor_df = donor_copy.loc[donor_copy.keep]
donor_df.drop(columns=['transaction_date', 'keep', 'transaction_type'], inplace=True)

# identify subscription add ons and create new column, drop fund_desc
add_on = 'PS Indiv Subscription Add On'
donor_df['sub_add_on'] = np.where(donor_df['fund_desc'] == add_on, True, False)

donor_df.drop(columns='fund_desc', inplace=True)
tmp_fy_col = donor_df.fy.str.slice(3).astype('int32')
donor_df.fy = tmp_fy_col

# Build dataframes to run through retention function
donors_retained_df = donor_df[['customer_id','fy']].drop_duplicates()


# Function to calculate retention
def calc_retention(df):
    """
    This function will calculate the number of retained customers across a
    given time frame.

    The dataframe must contain ONLY two columns.

    The first column is the category to retain (ie. customer number or $).
    The second column is the fiscal year.
    """

    # Built a dictionary for each fiscal year acting as the keys and a list
    # of all customers as the value for each key.
    fy_build = {fy:[] for fy in df['fy'].drop_duplicates()}

    for index,row in df.iterrows():
        fy_build[row[1]].append(row[0])


    # Loop through fy_build and check how many customers are retained from the
    # previous year and how many are new.

    retention_dict = {
        'retained': {fy: 0 for fy in df['fy'].drop_duplicates()},
        'new': {fy: 0 for fy in df['fy'].drop_duplicates()},
        'total': {fy: 0 for fy in df['fy'].drop_duplicates()}
    }

    for k,v in fy_build.items():
        if k == 10:
            total_donors = len(v)
            retention_dict['total'][k] += total_donors
            continue

        total_donors = len(v)
        retained_donors = len(set(v) & set(fy_build[k-1]))
        new_donors = total_donors - retained_donors

        retention_dict['total'][k] += total_donors
        retention_dict['retained'][k] += retained_donors
        retention_dict['new'][k] += new_donors

    return retention_dict



retention_dict = pd.DataFrame(calc_retention(donors_retained_df))

retention_dict.loc[10]

attrition = {index: 0 for index,row in retention_dict.iterrows()}
for index,row in retention_dict.iterrows():
    if index == 10:
        continue
    lapsed = retention_dict.loc[index - 1]['total'] - row['retained']
    percent_lapsed = lapsed / retention_dict.loc[index - 1]['total']
    attrition[index] = percent_lapsed

# Retention stacked bar plot
sns.set()
ax = retention_dict[['retained','new']].plot(kind='bar', stacked=True)
ax.set_title("Retention Graph YoY")


# Attrition over time graph
attrition_lists = sorted(attrition.items())[1:]
att_fy, att_val = zip(*attrition_lists)
plt.plot(att_fy, att_val)
plt.title("Percentage Attrition over time")
plt.show()
