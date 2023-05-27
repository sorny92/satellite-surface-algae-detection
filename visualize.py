import geopandas as gpd

import rasterio
from rasterio.windows import Window, from_bounds

from eoreader.reader import Reader
from eoreader.bands import GREEN, NDVI, CLOUDS, BLUE
from matplotlib import pyplot as plt
import pandas as pd
from shapely import wkt
from scripts.download import Downloader
import os
from shapely.geometry import box

import hvplot.pandas
import hvplot.xarray


# hvplot.extension('matplotlib')

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
        polygon_proj = polygon.to_crs(prod.crs())
        window_bounds = polygon.bounds.values[0]
        print(polygon)
        print(window_bounds)
        print(window_bounds.shape)

        full_prod = load(prod, polygon, GREEN)
        bounds = full_prod.rio.bounds()
        window_bounds_gpd = gpd.GeoDataFrame(
            geometry=[box(*window_bounds)],
            crs=polygon_proj.crs
        )

        plot = full_prod[0, ::1, ::1].hvplot.quadmesh(
            "x", "y",
            coastline="10m",
            cmap="bwy_r",
            tiles=True,
            frame_width=1270,
            frame_height=720
        ) * window_bounds_gpd.hvplot(
            facecolor=(0, 0, 0, 0),
            edgecolor="g", linewidth=4,
        ) \
        #        * polygon.hvplot(
        #     facecolor=(0, 0, 0, 0),
        #     edgecolor="b", linewidth=4,
        #     xlim=(bounds[0], bounds[2]),
        #     ylim=(bounds[1], bounds[3])
        # )
        hvplot.show(plot)
        break
