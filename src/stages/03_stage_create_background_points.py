import os
import tomllib
from datetime import datetime

import pandas as pd
from sdm_bio.sdm import SDM

if __name__ == "__main__":
    HOME = os.path.dirname(os.path.realpath(__file__))
    # Construct the path to the config file
    with open(os.path.join(HOME, "config.toml"), "rb") as f:
        config = tomllib.load(f)
    if config["general"]["stages"]["background"]:
        if config["general"]["force_use_date"]:
            current_date = config["general"]["date"]
        else:
            current_date = datetime.now().strftime("%d-%m-%Y")

        if config["general"]["stages"]["thinning"]:
            file_name = config["thinning"]["file_thinned_data"].format(
                config["thinning"]["min_distance"]
            )
        else:
            file_name = config["pre_process"]["files"]["occurence"]

        data = pd.read_parquet(
            os.path.join(
                config["general"]["output_path"],
                current_date + "/",
                file_name,
            )
        )
        sdm_model = SDM(data)

        sdm_model.generate_features_dataframe(
            data_path=config["general"]["output_path"],
            raster_file_path=[
                os.path.join(config["general"]["input_path"], file)
                for file in config["background"]["raster_file_path"]
            ],
            raster_file_cols=config["background"]["raster_file_cols"],
            n_random_points=config["background"]["n_random_points"],
            random_points=config["background"]["random_points"],
            spacing=config["background"]["spacing"],
            use_convex_polygon=config["background"]["use_convex_polygon"],
            features_path=config["background"]["features_path"],
        )
        print(f"[SUCCESS] GENERATE BACKGROUND POINTS STAGE")
