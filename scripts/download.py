from tqdm import tqdm
import urllib.parse

import requests
from requests.auth import HTTPBasicAuth
import os


# Para la recoleccion de datos se va a utilizar el
# POLYGON((41.37 0.29, 41.37 0.43, 41.22 0.43, 41.22 0.29, 41.37 0.29))


## DEvolver un xml con los uuid de las imagenes de interes
# https://scihub.copernicus.eu/dhus/search?q=footprint:"Intersects(POLYGON((41.37 0.29, 41.37 0.43, 41.22 0.43, 41.22 0.29, 41.37 0.29)))"


## Comprobar si la uuid esta disponible en el historico
# curl -u $USER:$PASS "https://scihub.copernicus.eu/dhus/odata/v1/Products('8364b44f-aa7f-4589-8695-44b7ed7b8f65')/Online/\$value"

## Descargar o hacer trigger del retrieval del historico
# curl -u $USER:$PASS "https://scihub.copernicus.eu/dhus/odata/v1/Products('8364b44f-aa7f-4589-8695-44b7ed7b8f65')/\$value"

class SentinelDownloader:
    def __init__(self):
        self.root_url = "https://scihub.copernicus.eu/dhus/"

    def do_request(self, arguments: list, stream=False):
        path_arguments = "/".join(arguments)
        full_url = urllib.parse.urljoin(self.root_url, path_arguments)

        response = requests.get(full_url, auth=HTTPBasicAuth(os.getenv('USER'), os.getenv('PASS')), stream=stream)
        if response.status_code != 200:
            raise Exception(f"status {response.status_code}: {response.text}")
        return response

    def is_product_online(self, product_id: str):
        response_text = self.do_request(["odata/v1", f"Products('{product_id}')/Online/$value"]).text
        return response_text == "true"

    @staticmethod
    def is_downloaded(file_path: str, to_be_downloaded_size: int = None):
        if os.path.exists(file_path):
            if to_be_downloaded_size:
                stats = os.stat(file_path)
                return stats.st_size == to_be_downloaded_size
            else:
                return True
        return False

    def download_product(self, product_id: str, download_path: str = "", try_to_download=True):
        is_online = self.is_product_online(product_id)
        if try_to_download and is_online:
            response = self.do_request(["odata/v1", f"Products('{product_id}')/$value"], stream=True)
            if download_path == "":
                download_path = response.headers["content-disposition"].split("=")[-1][1:-1]

            file_length = int(response.headers["content-length"])

            if self.is_downloaded(download_path, file_length):
                raise Exception("File already downloaded")
            with open(download_path, 'wb') as out_file, tqdm(
                    desc=download_path,
                    total=file_length,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(chunk_size=1024):
                    size = out_file.write(data)
                    bar.update(size)


s = SentinelDownloader()
s.download_product("8364b44f-aa7f-4589-8695-44b7ed7b8f65", "")
