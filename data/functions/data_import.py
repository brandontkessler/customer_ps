import pandas as pd
from user_inputs import first_day_of_first_fy, last_day_of_last_fy


# Identify fiscal years for ticketing data pull
fy_start = first_day_of_first_fy.year + 1
fy_end = last_day_of_last_fy.year
fiscal_years = [str(fy)[2:4] for fy in range(fy_start, fy_end + 1)]

# Identify path from cwd to raw data files
path = "data/raw/"


def ticketing_data_import(file_name, path=path):
    """Ticketing files are named with the type of concert (ie. Clx, Summer,
    Pops, Specials, etc.) followed by the last two digits of the fiscal year (
    19, 18, 17, etc.)
    
    Input:
        file_name: The type of concert. Accepted types include: Clx, Pops,
        Summer, Chamber, Connections, Family, Organ, Specials
    """
    
    accepted_file_names = ["Clx", "Pops", "Summer", "Chamber", "Connections",
                            "Family", "Organ", "Specials"]
    
    if file_name not in accepted_file_names:
        raise ValueError('file_name must be of accepted file types: ', 
                         accepted_file_names)
    
    files = [pd.read_csv(path + file_name + fy + ".csv", skiprows=3) for fy in fiscal_years]
    tix_raw = pd.concat(files, ignore_index=True)
    
    return tix_raw


def donor_data_import(path=path):
    donor_raw = pd.read_csv(path + "donors_fy08-fy19.csv", encoding='ISO-8859-1')
    return donor_raw

