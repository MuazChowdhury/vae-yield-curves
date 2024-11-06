import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

def get_swap_rates(swaps_df, maturity_dict):
    """
    This function takes a raw dataframe of bloomberg swap rates data and a dictionary of the {ticker: maturity} key-value pairs needed.
    This function returns a dataframe with only column of dates and all swap rates for each given maturity
    """
    df = swaps_df.copy()
    cols = list(maturity_dict.keys())
    curr_idx = df.columns.get_loc(cols[0] + ' Curncy')
    res_df = pd.DataFrame({'dates': df.iloc[:, curr_idx - 1],
                            maturity_dict[cols[0]]: df.loc[:, cols[0] + ' Curncy']})
    filter_dates = set(df.iloc[:, 0])

    for i in range(2, df.shape[1], 2):
        col = df.columns[i]
        filter_dates = set(filter_dates).intersection(df.loc[:, col])

    for i, _ in enumerate(cols):
        if i == 0:
            continue
        curr_idx = df.columns.get_loc(cols[i] + ' Curncy')
        df2 = pd.DataFrame({f'dates{i}': df.iloc[:, curr_idx - 1], maturity_dict[cols[i]]: df.loc[:, cols[i] + ' Curncy']})
        common_dates = set(filter_dates).intersection(set(df2[f'dates{i}']))
        filtered_df2 = df2[df2[f'dates{i}'].isin(common_dates)].reset_index().drop(columns=['index', f'dates{i}'])
        res_df = pd.merge(res_df, filtered_df2, left_index=True, right_index=True)
    
    return res_df

# The following dictionaries are the mappings of ticker to its corresponding maturity 

# Term structures for the full set of maturities (for GBP)
# Note: tickers 'BPSWSC', 'BPSWSD' do not exist in the data so they have been removed from ts_full
gbp_ts_full = {'BPSWS1Z': '1W', 'BPSWS2Z': '2W', 'BPSWSA': '1M',
'BPSWSB': '2M', 'BPSWSE': '5M', 'BPSWSF': '6M', 'BPSWSG': '7M', 'BPSWSH': '8M', 
'BPSWSI': '9M', 'BPSWSJ': '10M', 'BPSWSK': '11M', 'BPSWS1': '1Y', 'BPSWS1F': '1.5Y',
'BPSWS2': '2Y', 'BPSWS3': '3Y', 'BPSWS4': '4Y', 'BPSWS5': '5Y', 'BPSWS6': '6Y', 'BPSWS7': '7Y', 
'BPSWS8': '8Y', 'BPSWS9': '9Y', 'BPSWS10': '10Y', 'BPSWS12': '12Y', 'BPSWS15': '15Y', 'BPSWS20': '20Y', 
'BPSWS25': '25Y', 'BPSWS30': '30Y', 'BPSWS40': '40Y', 'BPSWS50': '50Y'}

# Term structures starting at 2 years (i.e. no short end of curve) (for GBP)
gbp_ts_long = {'BPSWS2': '2Y', 'BPSWS3': '3Y', 'BPSWS4': '4Y',
'BPSWS5': '5Y', 'BPSWS6': '6Y', 'BPSWS7': '7Y', 'BPSWS8': '8Y', 'BPSWS9': '9Y',
'BPSWS10': '10Y', 'BPSWS12': '12Y', 'BPSWS15': '15Y', 'BPSWS20': '20Y', 'BPSWS25': '25Y',
'BPSWS30': '30Y', 'BPSWS40': '40Y', 'BPSWS50': '50Y'}

# Term structures for the maturities used in the paper (7 maturities) (for GBP)
gbp_ts_7_mat = {'BPSWS2': '2Y', 'BPSWS3': '3Y',
                'BPSWS5': '5Y', 'BPSWS10': '10Y', 
                'BPSWS15': '15Y', 'BPSWS20': '20Y', 'BPSWS30': '30Y'}

# EUR
eur_ts_full = {'EESWE1Z': '1W', 'EESWE2Z': '2W', 'EESWEA': '1M',
'EESWEB': '2M', 'EESWEC': '3M', 'EESWED': '4M', 'EESWEE': '5M', 'EESWEF': '6M', 
'EESWEG': '7M', 'EESWEH': '8M', 'EESWEI': '9M', 'EESWEJ': '10M', 'EESWEK': '11M',
'EESWE1': '1Y', 'EESWE1F': '1.5Y', 'EESWE2': '2Y', 'EESWE3': '3Y', 'EESWE4': '4Y',
'EESWE5': '5Y', 'EESWE6': '6Y', 'EESWE7': '7Y', 'EESWE8': '8Y', 'EESWE9': '9Y',
'EESWE10': '10Y', 'EESWE12': '12Y', 'EESWE15': '15Y', 'EESWE20': '20Y', 'EESWE25': '25Y',
'EESWE30': '30Y', 'EESWE40': '40Y', 'EESWE50': '50Y'}

eur_ts_long = {'EESWE2': '2Y', 'EESWE3': '3Y', 'EESWE4': '4Y',
'EESWE5': '5Y', 'EESWE6': '6Y', 'EESWE7': '7Y', 'EESWE8': '8Y', 'EESWE9': '9Y',
'EESWE10': '10Y', 'EESWE12': '12Y', 'EESWE15': '15Y', 'EESWE20': '20Y', 'EESWE25': '25Y',
'EESWE30': '30Y', 'EESWE40': '40Y', 'EESWE50': '50Y'}

eur_ts_7_mat = {'EESWE2': '2Y', 'EESWE3': '3Y','EESWE5': '5Y', 'EESWE10': '10Y', 
                'EESWE15': '15Y', 'EESWE20': '20Y', 'EESWE30': '30Y'}

# USD
usd_ts_full = {'USOSFR1Z': '1W', 'USOSFR2Z': '2W', 'USOSFR3Z': '3W', 'USOSFRA': '1M',
'USOSFRB': '2M', 'USOSFRC': '3M', 'USOSFRD': '4M', 'USOSFRE': '5M', 'USOSFRF': '6M', 
'USOSFRG': '7M', 'USOSFRH': '8M', 'USOSFRI': '9M', 'USOSFRJ': '10M', 'USOSFRK': '11M',
'USOSFR1': '1Y', 'USOSFR1F': '1.5Y', 'USOSFR2': '2Y', 'USOSFR3': '3Y', 'USOSFR4': '4Y',
'USOSFR5': '5Y', 'USOSFR6': '6Y', 'USOSFR7': '7Y', 'USOSFR8': '8Y', 'USOSFR9': '9Y',
'USOSFR10': '10Y', 'USOSFR12': '12Y', 'USOSFR15': '15Y', 'USOSFR20': '20Y', 'USOSFR25': '25Y',
'USOSFR30': '30Y', 'USOSFR40': '40Y', 'USOSFR50': '50Y'}

usd_ts_long = {'USOSFR2': '2Y', 'USOSFR3': '3Y', 'USOSFR4': '4Y',
'USOSFR5': '5Y', 'USOSFR6': '6Y', 'USOSFR7': '7Y', 'USOSFR8': '8Y', 'USOSFR9': '9Y',
'USOSFR10': '10Y', 'USOSFR12': '12Y', 'USOSFR15': '15Y', 'USOSFR20': '20Y', 'USOSFR25': '25Y',
'USOSFR30': '30Y', 'USOSFR40': '40Y', 'USOSFR50': '50Y'}

usd_ts_7_mat = {'USOSFR2': '2Y', 'USOSFR3': '3Y', 'USOSFR5': '5Y', 'USOSFR10': '10Y',
                'USOSFR15': '15Y', 'USOSFR20': '20Y', 'USOSFR30': '30Y'}