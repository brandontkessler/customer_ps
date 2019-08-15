import numpy as np

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