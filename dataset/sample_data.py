from processing import generate_stack, get_bbox_with_window
import pandas as pd
from eoreader.reader import Reader
from shapely import wkt
import geopandas as gpd
from logging import debug, warning, info
import logging


def get_roi_from_polygon(polygon_string: str, product=None):
    info("Generating roi from polygon")
    wkt_polygon = wkt.loads(polygon_string)
    polygon = gpd.GeoDataFrame(index=[0], crs="EPSG:4326", geometry=[wkt_polygon])
    if product:
        return polygon.to_crs(prod.crs())
    else:
        return polygon


def visualize_stack(image_stack):
    import cv2
    plt.figure(figsize=(10, 10))
    chop = da.concatenate([image_stack[3:4], image_stack[2:3], image_stack[1:2]])
    chop = da.moveaxis(chop, 0, -1)

    lab= cv2.cvtColor(chop.compute(), cv2.COLOR_RGB2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl,a,b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)

    plt.imshow(enhanced_img)
    plt.show()


if __name__ == "__main__":
    import dask.array as da
    import matplotlib.pyplot as plt

    logging.basicConfig(level=logging.INFO)
    data = pd.read_csv("dataset/raw_data/DATOS_12_04_23.csv")

    for idx in range(data.shape[0]):
        print(data.loc[idx])
        polygon_str = data["POLYGON"][idx]
        date = data["Fecha"][idx]
        filename = data["NOMBRE_FICHERO"][idx]
        prod = Reader().open(filename)

        polygon = get_roi_from_polygon(polygon_str, prod)
        window = get_bbox_with_window(prod, polygon, 64)
        stack = generate_stack(prod, prod.get_existing_bands(), window)
        visualize_stack(stack)
        break
