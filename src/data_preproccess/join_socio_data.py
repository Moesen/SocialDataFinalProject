import argparse
import os
from functools import reduce

import numpy as np
import pandas as pd
from country_list import countries_for_language


def is_dir(path: str) -> str:
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)


def load_data_and_merge(in_path: str, out_path: str):
    socio_data = [x for x in os.listdir(os.path.join(in_path, "Socio_eco_data"))]

    print(f"Merging socio_dfs ({len(socio_data)})")
    socio_dfs = [
        pd.read_csv(os.path.join(in_path, "Socio_eco_data", filename))
        for filename in socio_data
    ]

    for df in socio_dfs:
        if "Code" in df.columns:
            df.drop("Code", inplace=True, axis=1)
        for col in df.columns:
            if "annotations" in col:
                df.drop(col, inplace=True, axis=1)
    socio_data_final = reduce(
        lambda left, right: pd.merge(left, right, on=["Entity", "Year"], how="outer"),
        socio_dfs,
    )

    socio_data_final = (
        socio_data_final.sort_values(["Entity", "Year"])
        .reset_index()
        .drop(columns="index")
    )

    return socio_data_final


def preprocces_data(out_path: str, df: pd.DataFrame):

    print(f"Preprocessing data (Column renaming and extraction)")

    cols = list(df.columns)
    for indx, col in enumerate(cols):
        if "Literacy" in col:
            cols[indx] = "Literacy_Rate"
        elif "military_" in col:
            cols[indx] = "Military_Spendings"
        elif "Mortality rate, under-5" in col:
            cols[indx] = "Child_Mortality_Rate"
            df.loc[:, col] = (1.0 * df.loc[:, col]) / 1000.0
        elif "Human Dev" in col:
            cols[indx] = "HDI"
        elif "obesity" in col:
            cols[indx] = "Obesity_Rate"
        elif "Access to basic drinking water" == col:
            cols[indx] = "Basic_Drinking_Water_Rate"
        elif "Access to basic sanitation services" == col:
            cols[indx] = "Basic_Sanitation_Services_Rate"
        elif "GDP" == col:
            cols[indx] = "GDP"
        elif "GDP per" in col:
            cols[indx] = "GDP_Per_Capita"
        elif "Life expec" in col:
            cols[indx] = "Life_Expectancy"
        elif "Entity" in col:
            cols[indx] = "Entity"
        elif "Year" in col:
            cols[indx] = "Year"
        else:
            cols[indx] = "to_drop"
            df.drop(columns=col, inplace=True)

    df.columns = [col for col in cols if "to_drop" not in col]

    df["HDI"] = pd.to_numeric(df["HDI"])
    for indx in range(len(df["HDI"])):
        if df.loc[indx, "HDI"] > 1:
            df.loc[indx, "HDI"] = df.loc[indx, "HDI"] / 1000

    print(f"Removing all rows with year prior to 1965")
    df["Year"] = pd.to_numeric(df["Year"])
    df = df[df.Year >= 1965].reset_index().drop(columns="index")

    print(f"Saving to csv in {out_path + '/socio_joined.csv'}")

    df.to_csv(os.path.join(out_path, "socio_joined.csv"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merging data from raw folder")
    parser.add_argument("--input_path", type=is_dir)
    parser.add_argument("--output_path", type=is_dir)
    args = parser.parse_args()

    in_path, out_path = args.input_path, args.output_path
    df = load_data_and_merge(in_path, out_path)
    preprocces_data(out_path, df)
