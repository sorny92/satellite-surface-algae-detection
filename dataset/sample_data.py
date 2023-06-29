from processing import ProcessProduct
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


def visualize_stack(image_stack, bounding_box=None):
    import cv2
    import numpy as np

    # Create figure and axes
    fig, ax = plt.subplots()
    chop = da.concatenate([image_stack[3:4], image_stack[2:3], image_stack[1:2]])
    chop = da.moveaxis(chop, 0, -1)
    chop *= 255
    numpy_data = chop.compute()
    numpy_data = numpy_data.astype(np.uint8)

    lab = cv2.cvtColor(numpy_data, cv2.COLOR_RGB2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl, a, b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2RGB)

    import matplotlib.patches as patches
    ax.imshow(enhanced_img)
    # Create a Rectangle patch
    rect = patches.Rectangle((bounding_box[0], bounding_box[2]),
                             bounding_box[1] - bounding_box[0],
                             bounding_box[3] - bounding_box[2],
                             linewidth=1, edgecolor='r',
                             facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)
    plt.show()


if __name__ == "__main__":
    import dask.array as da
    import matplotlib.pyplot as plt

    logging.basicConfig(level=logging.INFO)
    data = pd.read_csv("dataset/raw_data/DATOS_12_04_23.csv")

    for filename in data["NOMBRE_FICHERO"].unique():
        prod = Reader().open(filename)
        pp = ProcessProduct(product=prod)
        for idx, row in data[data["NOMBRE_FICHERO"] == filename].iterrows():
            polygon_str = row["POLYGON"]
            date = row["Fecha"]

            polygon = get_roi_from_polygon(polygon_str, prod)
            window = pp.get_bbox_from_window(polygon, 64)
            stack = pp.generate_stack(prod.get_existing_bands(), window)
            bbox_relative = pp.get_xy_relative_to_window(window, polygon)
            visualize_stack(stack, bbox_relative)
