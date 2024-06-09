import os
import tomllib
from datetime import datetime
from pathlib import Path

import pandas as pd


def generate_occurrence_dataset(configs: dict):
    if configs["general"]["force_use_date"]:
        current_date = configs["general"]["date"]
    else:
        current_date = datetime.now().strftime("%d-%m-%Y")
    # Reading the raw file and saving it as a treated parquet file
    gbif_parquet_path = os.path.join(
        configs["general"]["output_path"],
        current_date,
        configs["pre_process"]["files"]["gbif_parquet"],
    )

    pd.read_csv(
        os.path.join(
            configs["general"]["input_path"],
            configs["pre_process"]["load"]["file_occurence_unprocessed"],
        ),
        sep="\t",
    ).reset_index().to_parquet(gbif_parquet_path)

    occurrence_species_data = (
        pd.read_parquet(
            gbif_parquet_path,
        )[configs["pre_process"]["load"]["columns"]]
        .dropna()
        .astype(configs["pre_process"]["load"]["dtype"])
        .reset_index(drop=True)
    )
    occurrence_species_data["eventDate"] = pd.to_datetime(
        occurrence_species_data["eventDate"], errors="coerce", utc=True
    )  # Converting to datetime

    # Applying initial filters and rules
    occurrence_species_data = (
        occurrence_species_data.loc[
            (occurrence_species_data["countryCode"] == "BR")  # Filter BR
            & (~occurrence_species_data["eventDate"].isna())  # Remove data without date
            & (
                ~occurrence_species_data["stateProvince"].isna()
            )  # Remove data without state province
            & (
                occurrence_species_data["eventDate"].dt.year >= 2000
            )  # Remove data with date previous to 2020
        ]
        .fillna({"individualCount": 1})  # Set default count to 1
        .dropna(
            subset=["decimalLatitude", "decimalLongitude"]
        )  # Remove data without latitude or longitude
        .replace(
            {"stateProvince": configs["pre_process"]["state_encoding"]}
        )  # Correct the state encoding
    )

    # Filtering for records where the year is after 2020

    occurrence_species_data.rename(
        columns=configs["pre_process"]["load"]["columns_rename"], inplace=True
    )
    occurrence_species_data.loc[:, "target"] = 1

    # Saving the treated data and occurrence data

    occurrence_species_data.to_parquet(
        os.path.join(
            configs["general"]["output_path"],
            current_date,
            configs["pre_process"]["files"]["file_occurence_processed"],
        ),
        index=False,
    )
    occurrence = occurrence_species_data[["lat", "lon", "target"]]
    output_path = Path(
        os.path.join(
            configs["general"]["output_path"],
            current_date,
            configs["pre_process"]["files"]["occurence"],
        )
    )
    occurrence.to_parquet(output_path, index=False)
    print(f"[SUCCESS] FILE CREATED: {output_path.as_posix()}")


if __name__ == "__main__":
    HOME = os.path.dirname(os.path.realpath(__file__))
    # Construct the path to the config file
    with open(os.path.join(HOME, "config.toml"), "rb") as f:
        config = tomllib.load(f)
    if config["general"]["stages"]["pre_process"]:
        generate_occurrence_dataset(config)
