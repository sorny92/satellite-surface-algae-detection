from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
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
        return self.api.query(polygon, date)

    def request_product(self, id: str) -> ProductState:
        self.api.download(id)


if __name__ == "__main__":
    data_path = "dataset/DATOS_12_04_23.csv"
    data = pd.read_csv(data_path)
    #print(data)
    print(data.loc[0])
    polygon = data["POLYGON"][0]
    date = data["Fecha"][0]

    d = Downloader(os.getenv('USER'), os.getenv('PASS'))
    d.get_product_id(polygon, date)


    #
    # api.download("8364b44f-aa7f-4589-8695-44b7ed7b8f65")
    # res = api.query("POLYGON((41.37 0.29, 41.37 0.43, 41.22 0.43, 41.22 0.29, 41.37 0.29))",
    #                 date=("20230101", "20230120"),
    #                 platformname='Sentinel-2',
    #                 cloudcoverpercentage=(0, 30))
# for v in res:
#     print(v)
#     for k in res[v]:
#         print(f"    {k}")
#         print(f"        {res[v][k]}")
#     break
