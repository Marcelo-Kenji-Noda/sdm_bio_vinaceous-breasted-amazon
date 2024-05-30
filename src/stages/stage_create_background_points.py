import os
import tomllib

import pandas as pd
from sdm_bio.sdm import SDM

if __name__ == "__main__":
    HOME = os.path.dirname(os.path.realpath(__file__))
    # Construct the path to the config file
    with open(os.path.join(HOME, "config.toml"), "rb") as f:
        config = tomllib.load(f)

    data = pd.read_parquet(
        os.path.join(
            config["pre_process"]["files"]["dirs_generated_files"],
            config["general"]["date"] + "/",
            config["pre_process"]["files"]["occurence"],
        )
    )
    sdm_model = SDM(data)

    sdm_model.generate_features_dataframe(
        data_path=config["general"]["output_path"],
        raster_file_path=config["background"]["raster_file_path"],
        raster_file_cols=config["background"]["raster_file_cols"],
        n_random_points=config["background"]["n_random_points"],
    )
