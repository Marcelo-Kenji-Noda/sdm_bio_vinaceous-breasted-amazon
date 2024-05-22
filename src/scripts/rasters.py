from sdm_bio import RasterLayer, SDM
import pytoml
import os
import pandas as pd
import rasterio
if __name__ == '__main__':
    HOME = os.path.dirname(os.path.realpath(__file__))
    ARQUIVO = HOME + "/config.toml"
    with open(ARQUIVO,"rb") as f:
        config = pytoml.load(f)
        
    data = (
    pd.read_parquet("C:/Users/kenji/dev/web-scraping-images-vinacea/web-scraping-images-vinacea/assets/INPUT/gbif.parquet")[['Latitude','Longitude']].rename(
        columns={'Latitude':'lat','Longitude':'lon'}
        )
    )
    
    data['target'] = 1
    
    sdm_model = SDM(data)

    #df = sdm_model.generate_random_points(n_points = 5000)
    #df.to_parquet("C:/Users/kenji/dev/sdm_bio_vinaceous-breasted-amazon/data/data.parquet")
    sdm_model.generate_uniform_points_within_polygon(spacing=0.1)

    raster_layers = []
    for col, path  in zip(config['raster_files']['columns'],config['raster_files']['paths']):
        with rasterio.open(path) as src:
            raster_layers.append(RasterLayer(name=col, path=path, no_data=src.nodata))
    
    
    if config['raster_files']['run_download']:
        pd.DataFrame(raster_layers).to_parquet(config["raster_files"]["info"])
        tiff_files = sdm_model.crop_tiff_files(tiff_files=raster_layers, output_file_path=config['raster_files']['output_path'])
        sdm_model.export_self_geoframe_to_json(config['files']['presence_absence_json'])
        
        df = sdm_model.export_dataframe_with_raster_features(config['files']['presence_absence_json'], raster_layers=raster_layers, output_file_path=config['files']['features_path'])
    else:
        df = pd.read_parquet(config['files']['features_path'])
        #df2 = sdm_model.filter_occurences(df[['lat','lon','target']])
        #df2.to_parquet("C:/Users/kenji/dev/sdm_bio_vinaceous-breasted-amazon/data/data_filtered.parquet")
    print(df.head(), df.shape)