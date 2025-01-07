import argparse
import json
import os
import pandas as pd
from datetime import datetime

SUPPORTED_TYPES = [".csv", ".xls", ".xlsx"]

def normalize_time(time_str):
    return datetime.strptime(time_str, "%H:%M:%S").strftime("%H:%M:%S")

def main(source_data_path: str, output_dir: str) -> None:
    files = os.listdir(source_data_path)

    players_data = []

    for file in files:
        file_path = os.path.join(source_data_path, file)

        if not file.lower().endswith(tuple(SUPPORTED_TYPES)):
            continue

        df = pd.read_csv(file_path)
        df = df[["UTC TIME", "LATITUDE", "LONGITUDE"]]
        df["UTC TIME"] = df["UTC TIME"].apply(normalize_time)

        # [REMOVE] specific for test data
        df["INDEX"] = file.split("_")[1]

        players_data.append(df)


    combined_df = pd.concat(players_data, ignore_index=True)
    combined_df = combined_df.sort_values(by="UTC TIME", ascending=True)

    json_data = {}
    for index, row in combined_df.iterrows():
        current_time = row["UTC TIME"]
        if not json_data.get(current_time):
            json_data[current_time] = []

        item = {
            "player": row["INDEX"],
            "lat": row["LATITUDE"],
            "lon": row["LONGITUDE"]
        }

        json_data[current_time].append(item)

    with open(f'{output_dir}/result.json', 'w') as fp:
        json.dump(json_data, fp)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--source-data', type=str, required=True)
    parser.add_argument('--output-dir', type=str, required=True)
    args = parser.parse_args()
    main(
        source_data_path=args.source_data,
        output_dir=args.output_dir,
    )
