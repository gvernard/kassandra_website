import argparse
import sys
import os
import numpy as np
import pandas as pd

MY_IPS = ['C1_School closing',
          'C2_Workplace closing',
          'C3_Cancel public events',
          'C4_Restrictions on gatherings',
          'C5_Close public transport',
          'C6_Stay at home requirements',
          'C7_Restrictions on internal movement',
          'C8_International travel controls',
          'H1_Public information campaigns',
          'H2_Testing policy',
          'H3_Contact tracing',
          'H6_Facial Coverings']


def manipulate_latest_oxford(path_to_ips_file):
    # Read file in DataFrame
    latest_df = pd.read_csv(path_to_ips_file,
                            parse_dates=['Date'],
                            encoding="ISO-8859-1",
                            dtype={"RegionName": str,
                                   "RegionCode": str},
                            error_bad_lines=False)

    # Restrict data to selected columns 
    latest_df = latest_df[MY_IPS + ['CountryName','RegionName','Date','ConfirmedCases']]
    
    # Create unique GeoID
    # GeoID is CountryName__RegionName
    # np.where usage: if A then B else C
    latest_df["GeoID"] = np.where(latest_df["RegionName"].isnull(),
                                  latest_df["CountryName"] + '__',
                                  latest_df["CountryName"] + '__' + latest_df["RegionName"])
    
    # Fill any missing IPs by assuming they are the same as previous day
    for ip_col in MY_IPS:
        latest_df.update(latest_df.groupby('GeoID')[ip_col].ffill().fillna(0))

    # Add new cases column and fill it
    latest_df['NewCases'] = latest_df.groupby('GeoID').ConfirmedCases.diff().fillna(0)

    # Remove last entry that is for some reason always zero.
    latest_df = latest_df.groupby("GeoID",as_index=False).apply(lambda x: x.iloc[:-1])
    
    latest_df = latest_df.drop(['CountryName','RegionName','ConfirmedCases'],axis=1)
    latest_df.to_csv('latest_df.csv',index=False)       
    #return latest_df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--interventions_plan",
                        dest="ip_file",
                        type=str,
                        required=True,
                        help="The path to an intervention plan .csv file")
    args = parser.parse_args()
    manipulate_latest_oxford(args.ip_file)
    print("Done!")
