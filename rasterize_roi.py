import pandas as pd
from eoreader.reader import Reader
from eoreader.bands import GREEN, NDVI, CLOUDS, BLUE
from shapely import wkt
import geopandas as gpd


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


data = pd.read_csv("dataset/DATOS_12_04_23.csv")

for idx in range(data.shape[0]):
    print(data.loc[idx])
    polygon = data["POLYGON"][idx]
    date = data["Fecha"][idx]
    filename = data["NOMBRE_FICHERO"][idx]

    prod = Reader().open(filename)

    wkt_polygon = wkt.loads(polygon)
    polygon = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[wkt_polygon])
    polygon_proj = polygon.to_crs(prod.crs())

    full_prod = load(prod, polygon_proj, GREEN)
    full_prod[:, ::10, ::10].plot()

    break
