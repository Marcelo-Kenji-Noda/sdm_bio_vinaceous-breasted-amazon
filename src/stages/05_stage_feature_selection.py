import json
import os
import tomllib
from datetime import datetime

import pandas as pd


def correlation(dataset: pd.DataFrame, threshold: float = 0.7):
    col_corr = set()
    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > threshold:
                colname = corr_matrix.columns[i]
                col_corr.add(colname)
    return col_corr


if __name__ == "__main__":
    HOME = os.path.dirname(os.path.realpath(__file__))
    # Construct the path to the config file
    with open(os.path.join(HOME, "config.toml"), "rb") as f:
        config = tomllib.load(f)
    if config["general"]["stages"]["feature_selection"]:
        if config["general"]["force_use_date"]:
            current_date = config["general"]["date"]
        else:
            current_date = datetime.now().strftime("%d-%m-%Y")
        info = {}
        df = pd.read_parquet(
            os.path.join(
                config["general"]["output_path"],
                current_date + "/",
                "OUTPUT/features.parquet",
            )
        )
        y = df.pop("target")
        X = df.copy().drop(columns=["lat", "lon"])

        removed_columns = correlation(
            X, threshold=config["feature_selection"]["threshhold"]
        )

        info["removed_columns"] = list(removed_columns)

        X_CP = X.drop(columns=removed_columns)
        X_CP = X_CP.merge(y, left_index=True, right_index=True)
        X_CP.to_parquet(
            os.path.join(
                config["general"]["output_path"],
                current_date + "/",
                "OUTPUT/data.parquet",
            )
        )

        tiff_files = []
        for p, col in zip(
            config["background"]["raster_file_path"],
            config["background"]["raster_file_cols"],
        ):
            if col in X_CP.columns:
                tiff_files.append(p)

        info["tiff_files"] = list(set([os.path.basename(i) for i in tiff_files]))

        json_output = os.path.join(
            config["general"]["output_path"],
            current_date + "/",
            config["feature_selection"]["file_feature_selection_info"],
        )
        with open(json_output, "w") as fp:
            json.dump(info, fp)
        print(f"[SUCCESS] FEATURE SELECTION STAGE")
