import eoreader.products
from eoreader.bands import SpectralBandNames
import rasterio
import numpy as np
from utils.bands import band_resolutions
import xarray
from logging import debug, warning, info


class ProcessProduct:
    sentinel2_tile_size = (10980, 10980)

    def __init__(self, product: eoreader.products.Product):
        self._prod = product
        self._product_footprint = None
        self._affine_transform = None

    def get_product_affine_transform(self):
        if not self._affine_transform:
            if not self._product_footprint:
                self._product_footprint = self._prod.footprint()
            bbox_product = self._product_footprint.bounds.values[0]
            self._affine_transform = rasterio.transform.from_bounds(*bbox_product,
                                                                    self.sentinel2_tile_size[0],
                                                                    self.sentinel2_tile_size[1])
        return self._affine_transform

    def get_bbox_from_window(self, polygon, window_size: int):
        """
        Retrieves a bounding box with a specified window size around a given polygon within a product.

        Parameters:
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
        info("Extract squared bbox from a product")
        left, top, right, bottom = polygon.bounds.values[0]
        at = self.get_product_affine_transform()
        r, c = rasterio.transform.rowcol(at, [left, right], [bottom, top])
        rows_center = np.floor(np.mean(r))
        columns_center = np.floor(np.mean(c))
        window_size /= 2
        x, y = rasterio.transform.xy(at, [rows_center - window_size, rows_center + window_size - 1],
                                     [columns_center - window_size,
                                      columns_center + window_size - 1])
        info(f"The bbox is: {np.array([x[0], y[1], x[1], y[0]])}")
        return np.array([x[0], y[1], x[1], y[0]])

    def get_xy_relative_to_window(self, window, polygon):
        at = self.get_product_affine_transform()
        left, top, right, bottom = polygon.bounds.values[0]
        r_w, c_w = rasterio.transform.rowcol(at, [window[0], window[2]], [window[1], window[3]])
        r, c = rasterio.transform.rowcol(at, [left, right], [bottom, top])

        return np.array([c[0] - c_w[0],
                         c[1] - c_w[0],
                         r[0] - r_w[1],
                         r[1] - r_w[1]])

    def generate_stack(self, bands, window, resample=True):
        bands_data = []
        biggest_shape = None
        for band in bands:
            arr = self._prod.stack(
                band,
                window=window,
                resolution=band_resolutions[band]
            )
            if band is SpectralBandNames.BLUE:
                biggest_shape = arr.shape
                info(biggest_shape)
            bands_data.append(arr)
        if resample:
            for idx, band_data in enumerate(bands_data):
                resampled_band = band_data.rio.reproject(
                    band_data.rio.crs,
                    shape=biggest_shape[1:],
                    resampling=rasterio.enums.Resampling.bilinear,
                )
                bands_data[idx] = resampled_band
            bands_data = xarray.concat(bands_data, dim="z", coords="all", compat="override", join="override")
            bands_data = bands_data.squeeze("bands")
            debug(bands_data.shape)
        return bands_data
