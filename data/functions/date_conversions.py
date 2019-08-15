import pandas as pd


def date_conv(s):
    dates = {date:pd.to_datetime(date) for date in s.unique()}
    return s.map(dates)
