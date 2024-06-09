import glob
import os
import tomllib
from datetime import datetime

import contextily as ctx
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize
from PIL import Image
from rasterio.plot import plotting_extent
from rasterio.warp import Resampling, calculate_default_transform, reproject

if __name__ == "__main__":
    HOME = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(HOME, "config.toml"), "rb") as f:
        config = tomllib.load(f)
    if config["general"]["force_use_date"]:
        current_date = config["general"]["date"]
    else:
        current_date = datetime.now().strftime("%d-%m-%Y")

    # Step 1: Read the .tif files
    input_directory = f"C:/Users/kenji/dev/sdm_bio_vinaceous-breasted-amazon/data/{current_date}/INPUT/TIFF"
    output_directory = f"C:/Users/kenji/dev/sdm_bio_vinaceous-breasted-amazon/data/{current_date}/IMAGES"
    combined_output_path = f"C:/Users/kenji/dev/sdm_bio_vinaceous-breasted-amazon/data/{current_date}/IMAGES"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if not os.path.exists(combined_output_path):
        os.makedirs(combined_output_path)

    # Step 2 & 3: Reproject, plot and save each file as .png
    tif_files = glob.glob(os.path.join(input_directory, "*.tif"))
    png_files = []

    for tif_file in tif_files:
        with rasterio.open(tif_file) as src:
            fig, ax = plt.subplots(figsize=(10, 10))

            # Calculate the transform and dimensions for the destination array
            transform, width, height = calculate_default_transform(
                src.crs, "EPSG:3857", src.width, src.height, *src.bounds
            )

            # Create the destination array in memory with float type
            destination = np.empty((height, width), dtype=np.float32)

            # Reproject the source image to the destination array
            reproject(
                source=rasterio.band(src, 1),
                destination=destination,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs="EPSG:3857",
                resampling=Resampling.nearest,
            )

            # Mask nodata values
            if src.nodata is not None:
                destination[destination == src.nodata] = np.nan
                minimum = destination.min()
                if minimum < 200:
                    destination[destination == minimum] = np.nan
            else:
                print(f"{tif_file} Is None")

            # Plot the reprojected image
            extent = plotting_extent(src)
            im = ax.imshow(
                destination,
                extent=extent,
                cmap="viridis",
                alpha=0.6,
                norm=Normalize(
                    vmin=np.nanmin(destination), vmax=np.nanmax(destination)
                ),
            )
            ctx.add_basemap(
                ax, crs="EPSG:3857", source=ctx.providers.CartoDB.Positron, alpha=0.05
            )

            # Set title and axis labels
            base_name = os.path.basename(tif_file).replace(".tif", "")
            ax.set_title(base_name)
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")

            # Add a colorbar
            cbar = plt.colorbar(
                im, ax=ax, orientation="vertical", fraction=0.036, pad=0.04
            )
            cbar.set_label("Pixel Value")

            # Save the plot as a .png file
            png_file_path = os.path.join(output_directory, base_name + ".png")
            plt.savefig(png_file_path, bbox_inches="tight", pad_inches=0.1)
            png_files.append(png_file_path)
            plt.close(fig)

    # Step 4: Combine all .png files into a single PDF file
    images = [Image.open(png_file) for png_file in png_files]

    # Save as a PDF
    combined_pdf_path = os.path.join(combined_output_path, "combined_output.pdf")
    images[0].save(combined_pdf_path, save_all=True, append_images=images[1:])

    # Save as a single PNG (stacked vertically)
    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)
    combined_image = Image.new("RGB", (max_width, total_height))

    y_offset = 0
    for img in images:
        combined_image.paste(img, (0, y_offset))
        y_offset += img.height

    combined_png_path = os.path.join(combined_output_path, "combined_output.png")
    combined_image.save(combined_png_path)

    print("Processing complete. Files saved at:", combined_output_path)
