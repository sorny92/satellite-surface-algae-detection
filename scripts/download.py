from sentinelsat import SentinelAPI
import os
import pandas as pd
from enum import Enum


class Downloader:
    class ProductState(Enum):
        AVAILABLE = 1
        REQUESTED = 2

    def __init__(self, user, password):
        self.api = SentinelAPI(user, password, 'https://apihub.copernicus.eu/apihub')

    def get_product_id(self, polygon, date) -> dict[str, dict]:
        day, month, year = [int(x) for x in date.split("-")]
        # TODO: Change this to user dates properly instead of formating with strings
        from_date = f"20{year:>02}{month:>02}{day:>02}"  # yyyyMMdd
        to_date = f"20{year:>02}{month:>02}{day + 1:>02}"  # yyyyMMdd

        return self.api.query(polygon, (from_date, to_date),
                              # Platform to Sentinel-2 as it's the only one we use as source of data
                              platformname="Sentinel-2",
                              # We only use this source of data
                              processinglevel="Level-2A")

    def request_product(self, id: str) -> ProductState:
        self.api.download(id)


if __name__ == "__main__":
    data_path = "dataset/DATOS_12_04_23.csv"
    data = pd.read_csv(data_path)
    d = Downloader(os.getenv('USER'), os.getenv('PASS'))
    for idx in range(data.shape[0]):
        print(data.loc[idx])
        polygon = data["POLYGON"][idx]
        date = data["Fecha"][idx]
        product_list = d.get_product_id(polygon, date)
        for k in product_list:
            d.request_product(k)
