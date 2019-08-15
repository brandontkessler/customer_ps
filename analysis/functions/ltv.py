import numpy as np

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