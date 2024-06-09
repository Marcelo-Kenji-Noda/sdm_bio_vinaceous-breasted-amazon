import os
import tomllib
from datetime import datetime
from pathlib import Path

import geopandas as gpd
import pandas as pd
from sdm_bio.utils import geoframe_to_pandas, pandas_to_geoframe, plot_points
from shapely.geometry import Point


def thin_points(points, min_distance):
    thinned_points = []
    for point in points:
        if all(
            point.distance(other_point) >= min_distance
            for other_point in thinned_points
        ):
            thinned_points.append(point)
    return thinned_points


def thin_occurences(
    presence_data: gpd.GeoDataFrame, min_distance=1000, target_default_value=1
):
    wgs84 = "EPSG:4326"
    utm = "EPSG:32633"  # UTM zone 33N as an example

    presence_data = presence_data.to_crs(utm)

    if isinstance(presence_data.geometry.iloc[0], tuple):
        presence_data["geometry"] = presence_data.apply(
            lambda row: Point(row.geometry), axis=1
        )

    points = list(presence_data.geometry)

    # Define minimum distance (in the same units as the projected CRS)

    # Apply the thinning algorithm
    thinned_points = thin_points(points, min_distance)

    # Convert thinned points back to a GeoDataFrame
    thinned_data = gpd.GeoDataFrame(geometry=thinned_points, crs=utm)
    # Reproject thinned points back to WGS84
    thinned_data = thinned_data.to_crs(wgs84)
    thinned_data["target"] = target_default_value
    return geoframe_to_pandas(thinned_data)


if __name__ == "__main__":
    HOME = os.path.dirname(os.path.realpath(__file__))
    # Construct the path to the config file
    with open(os.path.join(HOME, "config.toml"), "rb") as f:
        config = tomllib.load(f)

    if config["general"]["stages"]["thinning"]:
        if config["general"]["force_use_date"]:
            current_date = config["general"]["date"]
        else:
            current_date = datetime.now().strftime("%d-%m-%Y")

        df = pd.read_parquet(
            os.path.join(
                config["general"]["output_path"],
                current_date,
                config["pre_process"]["files"]["occurence"],
            )
        )

        df_geo = pandas_to_geoframe(df)
        thinned_data_pd = thin_occurences(
            presence_data=df_geo, min_distance=config["thinning"]["min_distance"]
        )
        output_path = Path(
            os.path.join(
                config["general"]["output_path"],
                current_date,
                f"INPUT/occurences_filtered_{config['thinning']['min_distance']}_m.parquet",
            )
        )
        thinned_data_pd.to_parquet(
            os.path.join(
                config["general"]["output_path"],
                current_date,
                config["thinning"]["file_thinned_data"].format(
                    str(config["thinning"]["min_distance"])
                ),
            )
        )
        print(f"[SUCCESS] FILE CREATED: {output_path.as_posix()}")
