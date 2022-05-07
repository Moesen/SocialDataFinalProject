import argparse
import os

import numpy as np
import pandas as pd


def is_dir(path: str) -> str:
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)


def load_data_and_preprocess(path: str):
    df_social = pd.read_csv(path + "/socio_extrapolated_5_country.csv", index_col=0)
    df_energy = pd.read_csv(path + "/pcc_energy_extrapolated_5_country.csv", index_col=0)

    # Make sure both energy and social data keys (entity, year) are present in both datasets. Otherwise drop those records
    temp1 = list(zip(df_energy[["Entity","Year"]].value_counts().reset_index().drop(columns=0)['Entity'],
                    df_energy[["Entity","Year"]].value_counts().reset_index().drop(columns=0)['Year']))
    temp2 = list(zip(df_social[["Entity","Year"]].value_counts().reset_index().drop(columns=0)['Entity'],
                    df_social[["Entity","Year"]].value_counts().reset_index().drop(columns=0)['Year']))
    exclude_records1 = list(set(temp2) - set(temp1))
    exclude_records = list(set(temp1) - set(temp2))

    # Comprehensive list of keys from both datasets, that is not a part the intersection
    exclude_records.extend(exclude_records1)

    # Extract keys
    list_energy = list(zip(df_energy['Entity'],df_energy['Year']))
    list_social = list(zip(df_social['Entity'],df_social['Year']))

    # Get list of all keys, that should not be excluded
    list_in_energy = [x not in exclude_records for x in list_energy]
    list_in_social = [x not in exclude_records for x in list_social]

    # Drop unwanted records and sort remaining data (so energy and social data align in index)
    df_energy = df_energy.iloc[list_in_energy,].reset_index().drop(columns='index')
    df_social = df_social.iloc[list_in_social,].reset_index().drop(columns='index')
    df_energy = df_energy.sort_values(['Entity','Year']).reset_index().drop(columns='index')
    df_social = df_social.sort_values(['Entity','Year']).reset_index().drop(columns='index')

    # Extract records, where we have zero nan values (combined between the two datasets) - only for columns of interest
    df_energy_sub = df_energy.iloc[:,[5,6]]
    df_social_sub = df_social.iloc[:,[0,1,2,5,6,8,9,10,12,13,14]]

    energy_non_nan_indx = df_energy_sub.isna().sum(axis=1)==0
    social_non_nan_indx = df_social_sub.isna().sum(axis=1)==0

    indx_non_nan = energy_non_nan_indx & social_non_nan_indx

    df_energy_sub = df_energy_sub.iloc[np.array(indx_non_nan),].reset_index().drop(columns='index')
    df_social_sub = df_social_sub.iloc[np.array(indx_non_nan),].reset_index().drop(columns='index')

    # Due to numerical instability with too large values, we will work with log(population)
    df_social_sub.iloc[:,4] = df_social_sub.iloc[:,4]/1e6

    # define target variable
    df_social_sub['y'] = df_energy_sub['Low-carbon energy per capita (kWh)']/df_energy_sub['Energy per capita (kWh)']

    # Save data
    df_social_sub.to_csv(os.path.join(path, f"ml_processed_data.csv"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess ml data")
    parser.add_argument("--path", type=is_dir)
    args = parser.parse_args()

    path= args.path
    load_data_and_preprocess(path)
