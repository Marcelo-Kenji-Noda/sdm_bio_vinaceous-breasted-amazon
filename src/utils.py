import os

from osgeo import gdal


def align_raster(source_tiff_path, target_tiff_path, output_tiff_path):
    """
    Align the target GeoTIFF to the grid of the source GeoTIFF using gdalwarp.

    Args:
        source_tiff_path (str): Path to the source GeoTIFF file.
        target_tiff_path (str): Path to the target GeoTIFF file to be aligned.
        output_tiff_path (str): Path to save the aligned GeoTIFF file.

    Returns:
        None
    """
    # Open the source GeoTIFF to get its transform and resolution
    source_dataset = gdal.Open(source_tiff_path, gdal.GA_ReadOnly)
    if source_dataset is None:
        raise ValueError(f"Failed to open source GeoTIFF file: {source_tiff_path}")

    # Get the affine transform and pixel size from the source GeoTIFF
    source_transform = source_dataset.GetGeoTransform()
    pixel_size_x = source_transform[1]
    pixel_size_y = abs(source_transform[5])

    # Close the source dataset
    source_dataset = None

    # Build gdalwarp command
    warp_command = [
        "gdalwarp",
        "-of",
        "GTiff",
        "-tr",
        str(pixel_size_x),
        str(pixel_size_y),
        "-tap",
        "-t_srs",
        "EPSG:4326",  # Replace with the target CRS if different
        target_tiff_path,
        output_tiff_path,
    ]

    # Execute the gdalwarp command
    os.system(" ".join(warp_command))


# Example usage
source_tiff_path = r"C:\Users\kenji\dev\sdm_bio_vinaceous-breasted-amazon\data\features\MANT\bioclim01.tif"
target_tiff_path = r"C:\Users\kenji\dev\sdm_bio_vinaceous-breasted-amazon\data\features\MANT\ambdata_vegetacao_ibge1992_br.tif"
output_tiff_path = r"C:\Users\kenji\dev\sdm_bio_vinaceous-breasted-amazon\data\features\TEST\ambdata_vegetacao_ibge1992_br.tif"
align_raster(source_tiff_path, target_tiff_path, output_tiff_path)
