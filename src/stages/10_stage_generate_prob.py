import glob
import os
import tomllib
from datetime import datetime

import contextily as ctx
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import rasterio
import rasterio.mask
from matplotlib.colors import Normalize
from PIL import Image
from rasterio.plot import show

if __name__ == "__main__":
    HOME = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(HOME, "config.toml"), "rb") as f:
        config = tomllib.load(f)
    if config["general"]["force_use_date"]:
        current_date = config["general"]["date"]
    else:
        current_date = datetime.now().strftime("%d-%m-%Y")
    # Directories and file paths
    models_directory = f"C:/Users/kenji/dev/sdm_bio_vinaceous-breasted-amazon/data/{current_date}/MODELS"
    output_directory = f"C:/Users/kenji/dev/sdm_bio_vinaceous-breasted-amazon/data/{current_date}/REPORT/PROBS"
    combined_output_path = f"C:/Users/kenji/dev/sdm_bio_vinaceous-breasted-amazon/data/{current_date}/REPORT/PROBS"
    shapefile_path = os.path.join(
        config["general"]["input_path"], config["crop_files"]["shape_file"]
    )
    occurrences_file = os.path.join(
        config["general"]["output_path"],
        current_date,
        config["pre_process"]["files"]["occurence"],
    )

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if not os.path.exists(combined_output_path):
        os.makedirs(combined_output_path)

    # Read the occurrences data
    occurrences_df = pd.read_parquet(occurrences_file)

    # Read the shapefile
    shapefile = gpd.read_file(shapefile_path)

    # Function to plot and save each probability map with occurrences
    def plot_probability_map(
        model_name, tif_file_path, occurrences_df, shapefile, output_path
    ):
        with rasterio.open(tif_file_path) as src:
            # Mask the tif file using the shapefile
            shapes = [
                feature["geometry"]
                for feature in shapefile.__geo_interface__["features"]
            ]
            out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
            out_meta = src.meta.copy()
            out_meta.update(
                {
                    "driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform,
                }
            )

            fig, ax = plt.subplots(figsize=(10, 10))

            # Plot the masked probability map with a color scale
            img = ax.imshow(
                out_image[0],
                cmap="viridis",
                norm=Normalize(vmin=0, vmax=1),
                extent=rasterio.plot.plotting_extent(src, transform=out_transform),
            )
            cbar = fig.colorbar(img, ax=ax, orientation="vertical")
            cbar.set_label("Probability")

            # Filter and plot occurrences points inside the shapefile
            points_within_shapefile = gpd.GeoDataFrame(
                occurrences_df,
                geometry=gpd.points_from_xy(occurrences_df.lon, occurrences_df.lat),
                crs=shapefile.crs,
            )
            points_within_shapefile = gpd.sjoin(
                points_within_shapefile, shapefile, op="within"
            )
            ax.scatter(
                points_within_shapefile.geometry.x,
                points_within_shapefile.geometry.y,
                c="red",
                s=5,
                label="Occurrences",
            )

            # Set the plot limits to match the masked tif dimensions
            bounds = src.bounds
            ax.set_xlim(bounds.left, bounds.right)
            ax.set_ylim(bounds.bottom, bounds.top)

            # Add basemap
            ctx.add_basemap(
                ax, crs=src.crs, source=ctx.providers.CartoDB.Positron, alpha=0.05
            )

            # Add title and legend
            ax.set_title(f"{model_name} Probability Map")
            ax.legend()

            # Save the plot as a PNG file
            plt.savefig(output_path, bbox_inches="tight", pad_inches=0.1)
            plt.close(fig)

    # Traverse through each subfolder in the MODELS directory and plot probability maps
    png_files = []
    for model_folder in os.listdir(models_directory):
        model_path = os.path.join(models_directory, model_folder)
        if os.path.isdir(model_path):
            tif_file_path = os.path.join(model_path, "IMAGES", "probability_1.tif")
            if os.path.exists(tif_file_path):
                base_name = os.path.basename(model_path)
                output_png_path = os.path.join(
                    output_directory, f"{base_name}_probability_map.png"
                )
                plot_probability_map(
                    base_name, tif_file_path, occurrences_df, shapefile, output_png_path
                )
                png_files.append(output_png_path)

    # Combine all PNG files into a single PDF file
    if png_files:
        images = [Image.open(png_file) for png_file in png_files]
        combined_pdf_path = os.path.join(
            combined_output_path, "combined_probability_maps.pdf"
        )
        images[0].save(combined_pdf_path, save_all=True, append_images=images[1:])
        print("PDF report saved at:", combined_pdf_path)
    else:
        print("No PNG files to combine.")

    print("Processing complete. Files saved at:", combined_output_path)
