import argparse
import os
from functools import reduce

import pandas as pd


def is_dir(path: str) -> str:
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merging data from raw folder")
    parser.add_argument("--input_path", type=is_dir)
    parser.add_argument("--output_path", type=is_dir)
    args = parser.parse_args()

    in_path, out_path = args.input_path, args.output_path
    energy_data = [x for x in os.listdir(os.path.join(in_path, "EnergyData"))]

    ac_paths = list(filter(lambda x: "ac" in x.lower(), energy_data))
    pcc_paths = list(filter(lambda x: "pcc" in x.lower(), energy_data))

    print(f"Merging ac_dfs ({len(ac_paths)})")
    ac_dfs = [
        pd.read_csv(os.path.join(in_path, "EnergyData", filename))
        for filename in ac_paths
    ]
    for df in ac_dfs:
        df.drop("Code", inplace=True, axis=1)
    ac_final = reduce(
        lambda left, right: pd.merge(left, right, on=["Entity", "Year"], how="outer"),
        ac_dfs,
    )

    print(f"Merging pcc_dfs ({len(pcc_paths)})")
    pcc_dfs = [
        pd.read_csv(os.path.join(in_path, "EnergyData", filename))
        for filename in pcc_paths
    ]
    for df in pcc_dfs:
        df.drop("Code", inplace=True, axis=1)
    pcc_final = reduce(
        lambda left, right: pd.merge(left, right, on=["Entity", "Year"], how="outer"),
        pcc_dfs,
    )

    print(f"Saving to csv in {out_path=}")
    ac_final.to_csv(os.path.join(out_path, "ac_energy_joined.csv"))
    pcc_final.to_csv(os.path.join(out_path, "pcc_energy_joined.csv"))
