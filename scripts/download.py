import logging
import pathlib

import sentinelsat.exceptions
from sentinelsat import SentinelAPI
import os
import pandas as pd
import datetime
from enum import Enum


class Downloader:
    class ProductState(Enum):
        AVAILABLE = 1
        REQUESTED = 2

    def __init__(self, user, password):
        self.api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus/')

    def get_product_id(self, polygon, date) -> dict[str, dict]:
        day, month, year = [int(x) for x in date.split("-")]
        date = datetime.datetime(year, month, day)
        from_date = date.strftime('%Y%m%d')
        to_date = (date + datetime.timedelta(days=1)).strftime('%Y%m%d')

        return self.api.query(polygon, (from_date, to_date),
                              # Platform to Sentinel-2 as it's the only one we use as source of data
                              platformname="Sentinel-2",
                              # We only use this source of data
                              processinglevel="Level-2A")

    def request_product(self, id: str) -> ProductState:
        try:
            self.api.download(id)
        except sentinelsat.exceptions.LTATriggered:
            logging.warning(f"{id} is going to be retreived from long term archive")


def download_all_data(path: pathlib.Path):
    data = pd.read_csv(path)
    d = Downloader(os.getenv('USER'), os.getenv('PASS'))
    for idx in range(data.shape[0]):
        print(data.loc[idx])
        polygon = data["POLYGON"][idx]
        date = data["Fecha"][idx]
        product_list = d.get_product_id(polygon, date)
        for k in product_list:
            d.request_product(k)


if __name__ == "__main__":
    data_path = pathlib.Path("dataset", "raw_data", "DATOS_27_05_23.csv")
    download_all_data(data_path)
