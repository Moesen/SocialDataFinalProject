import pandas as pd
import os
import argparse

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
    
    ac_data = filter(lambda x: "ac" in x.lower(), energy_data)
    pcc_data = filter(lambda x: "pcc" in x.lower(), energy_data)
    
    print(ac_data, pcc_data, sep="\n")