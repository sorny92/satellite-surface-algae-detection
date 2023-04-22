import geopandas as gpd
import rasterio.plot

from rasterio.windows import Window, from_bounds
from eoreader.reader import Reader
from eoreader.bands import GREEN, NDVI, CLOUDS, BLUE
from matplotlib import pyplot as plt
import pandas as pd
from shapely import wkt
from scripts.download import Downloader
import os

def load(prod, window, band):
    """
    Function that loads the wanted band over a proposed window and cleans the temporary directory.
    """
    arr = prod.load(
        band,
        window=window
    )
    prod.clean_tmp()
    return arr[band]

if __name__ == "__main__":
    data = pd.read_csv("dataset/DATOS_12_04_23.csv")
    d = Downloader(os.getenv('USER'), os.getenv('PASS'))
    for idx in range(data.shape[0]):
        print(data.loc[idx])
        polygon = data["POLYGON"][idx]
        date = data["Fecha"][idx]
        filename = data["NOMBRE_FICHERO"][idx]

        prod = Reader().open(filename)

        wkt_polygon = wkt.loads(polygon)
        polygon = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[wkt_polygon])
        polygon = polygon.to_crs(prod.crs())
        polygon.plot()
        window_bounds = polygon.bounds.values[0]
        print(polygon)
        print(window_bounds)

        with rasterio.open(str(prod.get_band_paths([GREEN])[GREEN])) as ds:
            window_pix = from_bounds(*window_bounds, ds.transform)

        full_image = load(prod, None, GREEN)
        img = load(prod, polygon, GREEN)
        print(full_image.shape)
        bands = prod.load([GREEN])
        full_image[0, ::10, ::10].plot()
        bands[GREEN][:, ::10, ::10].plot()
        # prod.plot()
        plt.show()
        break
