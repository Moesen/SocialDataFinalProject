import argparse
import os
from functools import reduce
from country_list import countries_for_language
import pycountry_convert as pc

import numpy as np
import pandas as pd
from country_list import countries_for_language


def is_dir(path: str) -> str:
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)


def interpolate_data(out_path: str, df_name: str):
    df = pd.read_csv(os.path.join(out_path, f"{df_name}_joined.csv"), index_col=0)

    print(f"Interpolating data (linear)")

    # Get shapes
    N = df.shape[0]
    cols_to_interp = df.columns[2:]

    # Replace strings with nan
    df.replace("nan", np.nan, inplace=True)

    # Force columns to be numeric (non entity columns)
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col])

    # Make pseudo-dataset for interpolating mask
    df_interp_mask = df.copy()
    df_interp_mask[cols_to_interp] = df_interp_mask[cols_to_interp] * 0
    df_interp_mask.replace(np.nan, 0, inplace=True)

    # Go through each row - for missing years add rows and interpolate if possible
    for i in range(1, N):
        year_diff = df.Year[i] - df.Year[i - 1]
        if (year_diff > 1) & (df.Entity[i] == df.Entity[i - 1]):
            new_rows = np.array(
                [
                    [df.Entity[i]] * (year_diff - 1),
                    np.arange(df.Year[i - 1] + 1, df.Year[i]),
                ]
            ).T

            new_mask = np.array(
                [
                    [df.Entity[i]] * (year_diff - 1),
                    np.arange(df.Year[i - 1] + 1, df.Year[i]),
                ]
            ).T

            for col in cols_to_interp:
                if (np.isnan(df.loc[i, col]) == False) & (
                    np.isnan(df.loc[i - 1, col]) == False
                ):
                    new_rows = np.concatenate(
                        [
                            new_rows,
                            np.linspace(
                                df.loc[i - 1, col], df.loc[i, col], year_diff + 1
                            )[1:-1].reshape((year_diff - 1, 1)),
                        ],
                        axis=1,
                    )
                    new_mask = np.concatenate(
                        [
                            new_mask,
                            np.repeat(1, year_diff - 1).reshape((year_diff - 1, 1)),
                        ],
                        axis=1,
                    )
                else:
                    new_rows = np.concatenate(
                        [
                            new_rows,
                            np.array(np.repeat(np.nan, year_diff - 1)).reshape(
                                (year_diff - 1, 1)
                            ),
                        ],
                        axis=1,
                    )
                    new_mask = np.concatenate(
                        [
                            new_mask,
                            np.repeat(0, year_diff - 1).reshape((year_diff - 1, 1)),
                        ],
                        axis=1,
                    )

            new_rows = pd.DataFrame(new_rows, columns=df.columns)
            new_rows.replace("nan", np.nan, inplace=True)
            for col in new_rows.columns[1:]:
                new_rows[col] = pd.to_numeric(new_rows[col])

            new_mask = pd.DataFrame(new_mask, columns=df.columns)
            for col in new_mask.columns[1:]:
                new_mask[col] = pd.to_numeric(new_mask[col])

            df = (
                pd.concat([df.iloc[:i], new_rows, df.iloc[i:]], axis=0)
                .reset_index()
                .drop(columns="index")
            )
            df_interp_mask = (
                pd.concat(
                    [df_interp_mask.iloc[:i], new_mask, df_interp_mask.iloc[i:]], axis=0
                )
                .reset_index()
                .drop(columns="index")
            )
            N = N + year_diff - 1

    # Go through each column and interpolate values if possible
    for col in cols_to_interp:
        for i in range(N - 2):
            if not np.isnan(df.loc[i, col]):
                indx_old_non_nan = i
                while (df.Entity[i + 1] == df.Entity[i]) & (
                    np.isnan(df.loc[i + 1, col])
                ):
                    i = i + 1
                    if i == N - 1:
                        break
                if i == N - 1:
                    break
                if (df.Entity[i + 1] == df.Entity[i]) & (
                    indx_old_non_nan != i
                ):  # Non nan value followed by x nan values then non nan value (interpolation possible)
                    i = i + 1
                    df.loc[(indx_old_non_nan + 1) : (i - 1), col] = np.linspace(
                        df.loc[indx_old_non_nan, col],
                        df.loc[i, col],
                        i - indx_old_non_nan + 1,
                    )[1:-1]
                    df_interp_mask.loc[
                        (indx_old_non_nan + 1) : (i - 1), col
                    ] = np.repeat(1, i - indx_old_non_nan - 1)
                else:
                    i = i + 1
                    continue

    print(f"Saving to csv in {out_path + f'/{df_name}_interpolated.csv'}")
    print(f"Saving to csv in {out_path + f'/{df_name}_interpolated_mask.csv'}")
    
    df.to_csv(os.path.join(out_path, f"{df_name}_interpolated.csv"))
    df_interp_mask.to_csv(os.path.join(out_path, f"{df_name}_interpolated_mask.csv"))


def extrapolate_data(out_path: str, x_extrap: int, df_name: str):
    df = pd.read_csv(os.path.join(out_path, f"{df_name}_interpolated.csv"), index_col=0)
    df_extrap_mask = pd.read_csv(
        os.path.join(out_path, f"{df_name}_interpolated_mask.csv"), index_col=0
    )

    print(f"Extrapolating data (max {x_extrap} years)")

    # Get shapes
    N = df.shape[0]
    cols_to_extrap = df.columns[2:]

    if x_extrap >= 1:
        for col in cols_to_extrap:
            for i in range(1, N):
                if (
                    np.isnan(df.loc[i - 1, col])
                    & (not np.isnan(df.loc[i, col]))
                    & (df.loc[i - 1, "Entity"] == df.loc[i, "Entity"])
                ):
                    m = 1
                    if i - m - 1 >= 0:
                        while (
                            np.isnan(df.loc[i - m - 1, col])
                            & (df.loc[i - m - 1, "Entity"] == df.loc[i, "Entity"])
                            & (m + 1 <= x_extrap)
                        ):  # Go back a max of x_extrap years
                            m = m + 1
                            if i - m == 0:
                                break

                    df.loc[i - m : i - 1, col] = np.repeat(df.loc[i, col], m)
                    df_extrap_mask.loc[i - m : i - 1, col] = np.repeat(2, m)

            i = 0
            while i < N - 1:
                if (
                    np.isnan(df.loc[i + 1, col])
                    & (not np.isnan(df.loc[i, col]))
                    & (df.loc[i + 1, "Entity"] == df.loc[i, "Entity"])
                ):
                    m = 1
                    if i + m + 1 <= N - 1:
                        while (
                            np.isnan(df.loc[i + m + 1, col])
                            & (df.loc[i + m + 1, "Entity"] == df.loc[i, "Entity"])
                            & (m + 1 <= x_extrap)
                        ):  # Go forward a max of x_extrap years
                            m = m + 1
                            if i + m == N - 1:
                                break
                    df.loc[i + 1 : i + m, col] = np.repeat(df.loc[i, col], m)
                    df_extrap_mask.loc[i + 1 : i + m, col] = np.repeat(2, m)
                    i += m + 1
                else:
                    i += 1

    print(
        f"Saving to csv in {out_path + f'/{df_name}_extrapolated_' + str(x_extrap) + '.csv'}"
    )
    print(
        f"Saving to csv in {out_path + f'/{df_name}_extrapolated_mask_' + str(x_extrap) + '.csv'}"
    )

    df.to_csv(
        os.path.join(out_path, f"{df_name}_extrapolated_" + str(x_extrap) + ".csv")
    )
    df_extrap_mask.to_csv(
        os.path.join(out_path, f"{df_name}_extrapolated_mask_" + str(x_extrap) + ".csv")
    )


def split_data_country_area(out_path: str, processed_path: str, x_extrap, df_name: str):
    df = pd.read_csv(
        os.path.join(out_path, f"{df_name}_extrapolated_" + str(x_extrap) + ".csv"),
        index_col=0,
    )
    df_mask = pd.read_csv(
        os.path.join(
            out_path, f"{df_name}_extrapolated_mask_" + str(x_extrap) + ".csv"
        ),
        index_col=0,
    )

    print(f"Splitting data into countries and areas")

    entities = pd.Series(df.Entity.unique(), dtype="string")
    entities.replace({"&": "and"}, inplace=True, regex=True)
    countries = pd.Series(np.array(countries_for_language("en"))[:, 1], dtype="string")
    countries.replace({"&": "and"}, inplace=True, regex=True)
    countries.replace({"Congo - Brazzaville": "Congo"}, inplace=True, regex=True)
    countries.replace(
        {"Congo - Kinshasa": "Democratic Republic of Congo"}, inplace=True, regex=True
    )
    countries.replace({"Côte": "Cote"}, inplace=True, regex=True)
    countries.replace({"Curaçao": "Curacao"}, inplace=True, regex=True)
    countries.replace({"Czechoslovakia": "Czechia"}, inplace=True, regex=True)
    countries.replace({"Faroe Islands": "Faeroe Islands"}, inplace=True, regex=True)
    countries.replace({"Hong Kong SAR China": "Hong Kong"}, inplace=True, regex=True)
    # countries.replace({"Micronesia":"Micronesia (country)"},inplace=True, regex=True)
    countries.replace({"Macao SAR China": "Macao"}, inplace=True, regex=True)
    countries.replace({"Myanmar \(Burma\)": "Myanmar"}, inplace=True, regex=True)
    countries.replace(
        {"Palestinian Territories": "Palestine"}, inplace=True, regex=True
    )
    countries.replace(
        {"São Tomé and Príncipe": "Sao Tome and Principe"}, inplace=True, regex=True
    )
    countries.replace({"St\.": "Saint"}, inplace=True, regex=True)
    countries.replace(
        {"Saint Vincent and Grenadines": "Saint Vincent and the Grenadines"},
        inplace=True,
        regex=True,
    )
    countries.replace(
        {"Saint Martin": "Saint Martin (French part)"}, inplace=True, regex=True
    )
    countries.replace({"Timor-Leste": "Timor"}, inplace=True, regex=True)
    countries.replace(
        {"Saint Barthélemy": "Saint Barthelemy"}, inplace=True, regex=True
    )
    countries.replace(
        {"U\.S\. Virgin Islands": "United States Virgin Islands"},
        inplace=True,
        regex=True,
    )
    countries.replace({"Vatican City": "Vatican"}, inplace=True, regex=True)
    # countries.replace({"Wallis and Futuna":"Wallis and Futuna Islands"},inplace=True, regex=True)

    idx_country = []
    for ent in entities:
        if any(ent == country for country in countries):
            idx_country.append(True)
        else:
            idx_country.append(False)
    map_country = dict(zip(entities, idx_country))

    df_ent = df.Entity.astype("string").replace({"&": "and"}, regex=True)

    df_country = (
        df.iloc[np.array(df_ent.map(map_country))].reset_index().drop(columns="index")
    )
    df_area = (
        df.iloc[np.array(df_ent.map(map_country) == False)]
        .reset_index()
        .drop(columns="index")
    )
    df_mask_country = (
        df_mask.iloc[np.array(df_ent.map(map_country))]
        .reset_index()
        .drop(columns="index")
    )
    df_mask_area = (
        df_mask.iloc[np.array(df_ent.map(map_country) == False)]
        .reset_index()
        .drop(columns="index")
    )

    # Add continent info and remove countries with no continent info
    countries_code = pd.Series(np.array(countries_for_language('en'))[:,0],dtype="string")
    df_country['Continent'] = np.nan
    for indx, ent in enumerate(df_country['Entity']):
        try:
            cont = pc.convert_continent_code_to_continent_name(
            pc.country_alpha2_to_continent_code(countries_code.iloc[list(countries).index(ent)]))
            df_country.loc[indx,'Continent'] = cont
        except:
            continue;

    cols = df_country.columns[[0,-1]+list(np.arange(1,len(df_country.columns)-1,1))]
    df_country = df_country[cols]
    df_country = df_country[df_country['Continent'].notna()]

    print(
        f"Saving to csv in {processed_path + f'/{df_name}_extrapolated_' + str(x_extrap) + '_country.csv'}"
    )
    print(
        f"Saving to csv in {processed_path + f'/{df_name}_extrapolated_mask_' + str(x_extrap) + '_country.csv'}"
    )
    print(
        f"Saving to csv in {processed_path + f'/{df_name}_extrapolated_' + str(x_extrap) + '_area.csv'}"
    )
    print(
        f"Saving to csv in {processed_path + f'/{df_name}_extrapolated_mask_' + str(x_extrap) + '_area.csv'}"
    )

    df_country.to_csv(
        os.path.join(
            processed_path, f"{df_name}_extrapolated_" + str(x_extrap) + "_country.csv"
        )
    )
    df_mask_country.to_csv(
        os.path.join(
            processed_path, f"{df_name}_extrapolated_mask_" + str(x_extrap) + "_country.csv"
        )
    )
    df_area.to_csv(
        os.path.join(processed_path, f"{df_name}_extrapolated_" + str(x_extrap) + "_area.csv")
    )
    df_mask_area.to_csv(
        os.path.join(
            processed_path, f"{df_name}_extrapolated_mask_" + str(x_extrap) + "_area.csv"
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merging data from raw folder")
    parser.add_argument("--input_path", type=is_dir)
    parser.add_argument("--output_path", type=is_dir)
    parser.add_argument("--processed_path", type=is_dir)
    parser.add_argument("--x_extrap", type=int)
    parser.add_argument("--df_name", type=str)
    args = parser.parse_args()

    in_path, out_path, processed_path, x_extrap, df_name = args.input_path, args.output_path, args.processed_path, args.x_extrap, args.df_name
    interpolate_data(out_path, df_name)
    extrapolate_data(out_path, x_extrap, df_name)
    split_data_country_area(out_path, processed_path, x_extrap, df_name)


