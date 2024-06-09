import json
import os
import tomllib
from datetime import datetime
from pathlib import Path

import geopandas as gpd
import rasterio
from osgeo import gdal
from rasterio.mask import mask


def mask_tiff_with_shapefile(
    tiff_file: str,
    geoframe: gpd.GeoDataFrame,
    output_file_name: str,
):
    # Abre o arquivo .tiff
    with rasterio.open(tiff_file) as src:
        # Máscara do arquivo .tiff usando o shapefile
        out_image, out_transform = mask(src, geoframe.geometry, crop=True)

        # Atualiza os metadados para refletir a nova forma e posição do recorte
        out_meta = src.meta.copy()
        out_meta.update(
            {
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform,
            }
        )

        # Aplicar uma máscara adicional para remover os valores nodata
        # out_image = np.ma.masked_where(out_image == src.nodata, out_image)

        # Salva o recorte em um novo arquivo .tiff
        with rasterio.open(output_file_name, "w", **out_meta) as dest:
            dest.write(out_image)
    return output_file_name


def update_transform(source_tiff_path, target_tiff_path, output_tiff_path):
    """
    Update the transform of the target GeoTIFF to be exactly the same as the source GeoTIFF
    and save the updated GeoTIFF to a new file.

    Args:
        source_tiff_path (str): Path to the source GeoTIFF file.
        target_tiff_path (str): Path to the target GeoTIFF file to be updated.
        output_tiff_path (str): Path to save the updated GeoTIFF file.

    Returns:
        None
    """
    # Open the source GeoTIFF to get its transform
    source_dataset = gdal.Open(source_tiff_path, gdal.GA_ReadOnly)
    if source_dataset is None:
        raise ValueError(f"Failed to open source GeoTIFF file: {source_tiff_path}")

    # Get the affine transform from the source GeoTIFF
    source_transform = source_dataset.GetGeoTransform()

    # Open the target GeoTIFF to read raster data
    target_dataset = gdal.Open(target_tiff_path, gdal.GA_ReadOnly)
    if target_dataset is None:
        raise ValueError(f"Failed to open target GeoTIFF file: {target_tiff_path}")

    # Get raster band
    band = target_dataset.GetRasterBand(1)

    # Create output GeoTIFF file with the same dimensions and data type as the original
    driver = gdal.GetDriverByName("GTiff")
    output_dataset = driver.Create(
        output_tiff_path,
        target_dataset.RasterXSize,
        target_dataset.RasterYSize,
        1,
        band.DataType,
    )
    if output_dataset is None:
        raise ValueError(f"Failed to create output GeoTIFF file: {output_tiff_path}")

    # Set the affine transform to the output GeoTIFF
    output_dataset.SetGeoTransform(source_transform)

    # Write raster data to the output GeoTIFF
    output_band = output_dataset.GetRasterBand(1)
    output_band.WriteArray(band.ReadAsArray())

    # Set NODATA value
    if band.GetNoDataValue():
        output_band.SetNoDataValue(band.GetNoDataValue())

    # Set the projection (CRS) - copy from source GeoTIFF
    output_dataset.SetProjection(source_dataset.GetProjection())

    # Close the datasets
    source_dataset = None
    target_dataset = None
    output_dataset = None


def update_transformv2(source_tiff_path, target_tiff_path, output_tiff_path):
    """
    Update the transform of the target GeoTIFF to be exactly the same as the source GeoTIFF
    and save the updated GeoTIFF to a new file.

    Args:
        source_tiff_path (str): Path to the source GeoTIFF file.
        target_tiff_path (str): Path to the target GeoTIFF file to be updated.
        output_tiff_path (str): Path to save the updated GeoTIFF file.

    Returns:
        None
    """
    # Open the source GeoTIFF to get its transform
    source_dataset = gdal.Open(source_tiff_path, gdal.GA_ReadOnly)
    if source_dataset is None:
        raise ValueError(f"Failed to open source GeoTIFF file: {source_tiff_path}")

    # Open the target GeoTIFF to get its driver
    target_dataset = gdal.Open(target_tiff_path, gdal.GA_ReadOnly)
    if target_dataset is None:
        raise ValueError(f"Failed to open target GeoTIFF file: {target_tiff_path}")

    # Get the nodata value from the source dataset
    nodata_value = target_dataset.GetRasterBand(1).GetNoDataValue()
    # Get the driver from the target dataset
    driver = target_dataset.GetDriver()

    # Create a copy of the source GeoTIFF
    output_dataset = driver.CreateCopy(output_tiff_path, source_dataset, strict=0)
    if output_dataset is None:
        raise ValueError(f"Failed to create output GeoTIFF file: {output_tiff_path}")

    # Set the nodata value for the output dataset
    output_band = output_dataset.GetRasterBand(1)
    if nodata_value is not None:
        output_band.SetNoDataValue(nodata_value)

    # Close the datasets
    source_dataset = None
    target_dataset = None
    output_dataset = None


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    if config["general"]["force_use_date"]:
        current_date = config["general"]["date"]
    else:
        current_date = datetime.now().strftime("%d-%m-%Y")
    if not os.path.exists(
        os.path.join(
            config["general"]["output_path"],
            current_date,
            "INPUT/TIFF/",
        )
    ):
        os.mkdir(
            os.path.join(
                config["general"]["output_path"],
                current_date,
                "INPUT/TIFF/",
            )
        )
    geoframe = gpd.read_file(
        os.path.join(
            config["general"]["input_path"], config["crop_files"]["shape_file"]
        )
    )
    tiff_files = [
        os.path.join(config["general"]["input_path"], i)
        for i in config["background"]["raster_file_path"]
    ]
    # Create folder
    tiff_output_files = [
        os.path.join(
            config["general"]["output_path"],
            current_date,
            "INPUT/TIFF",
            os.path.basename(i),
        )
        for i in config["background"]["raster_file_path"]
    ]

    for tiff_file, tiff_output_file in zip(tiff_files, tiff_output_files):
        mask_tiff_with_shapefile(
            tiff_file=tiff_file, geoframe=geoframe, output_file_name=tiff_output_file
        )

    for output_file_name in config["crop_files"]["update_transformation_files"]:
        update_transformv2(
            tiff_output_files[0],
            os.path.join(
                config["general"]["output_path"],
                current_date,
                "INPUT/TIFF",
                output_file_name,
            ),
            os.path.join(
                config["general"]["output_path"],
                current_date,
                "INPUT/TIFF",
                f"updated_{output_file_name}",
            ),
        )
        tiff_output_files.append(f"updated_{output_file_name}")
        print("Transform updated successfully. Output file saved as:", output_file_name)

    tiff_files_for_model = set([os.path.basename(i) for i in tiff_output_files])

    for file in config["crop_files"]["update_transformation_files"]:
        os.remove(
            os.path.join(
                config["general"]["output_path"], current_date, "INPUT/TIFF", file
            )
        )
        os.rename(
            os.path.join(
                config["general"]["output_path"],
                current_date,
                "INPUT/TIFF",
                f"updated_{file}",
            ),
            os.path.join(
                config["general"]["output_path"], current_date, "INPUT/TIFF", file
            ),
        )
