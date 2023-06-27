from eoreader.bands import SpectralBandNames
from shapely import geometry
from eoreader.products import product
import rasterio
import numpy as np
from utils.bands import band_resolutions
import xarray


def get_bbox_with_window(prod: product, polygon: geometry.Polygon, window_size: int):
    """
    Retrieves a bounding box with a specified window size around a given polygon within a product.

    Parameters:
        - product (rasterio.DatasetReader): The rasterio dataset representing the product.
        - polygon (shapely.geometry.Polygon): The polygon for which to calculate the bounding box.
        - window_size: The size of the window around the polygon in the product's coordinate system.

    Returns:
        numpy.ndarray: A numpy array representing the bounding box coordinates [x_min, y_max, x_max, y_min].

    Raises:
        None.

    Example:
        # Import the required libraries
        import rasterio
        import numpy as np
        from shapely.geometry import Polygon

        # Open the product using rasterio
        product = rasterio.open('product.tif')

        # Create a polygon representing the area of interest
        polygon = Polygon([(10, 20), (20, 20), (20, 30), (10, 30)])

        # Define the window size
        window_size = 100

        # Call the function to get the bounding box with the window
        bbox = get_bbox_with_window(product, polygon, window_size)

        # Print the resulting bounding box
        print(bbox)
    """
    sentinel2_tile_size = (10980, 10980)
    bbox_prod = prod.footprint().bounds.values[0]
    # print(bbox_prod)
    left, bottom, right, top = polygon.bounds.values[0]
    # print(left, bottom, right, top)
    at = rasterio.transform.from_bounds(*bbox_prod, sentinel2_tile_size[0], sentinel2_tile_size[1])
    # print(at)
    r, c = rasterio.transform.rowcol(at, [left, right], [bottom, top])
    # rows_center = np.mean(r)
    rows_center = r[0]
    # print(rows_center)
    # columns_center = np.mean(c)
    columns_center = c[0]
    # print(columns_center)

    x, y = rasterio.transform.xy(at, [rows_center - window_size, rows_center + window_size],
                                 [columns_center - window_size, columns_center + window_size])
    # print(x, y)
    return np.array([x[0], y[1], x[1], y[0]])


def generate_stack(prod, bands, window, resample=True):
    bands_data = []
    biggest_shape = None
    for band in bands:
        arr = prod.stack(
            band,
            window=window,
            resolution=band_resolutions[band]
        )
        if band is SpectralBandNames.BLUE:
            biggest_shape = arr.shape
    if resample:
        for idx, band_data in enumerate(bands_data):
            resampled_band = band_data.rio.reproject(
                band_data.rio.crs,
                shape=biggest_shape[1:],
                resampling=rasterio.enums.Resampling.bilinear,
            )
            band_data[idx] = resampled_band
        bands_data = xarray.concat(bands_data, dim="z", join="override")
    return bands_data
