import pathlib
import urllib.parse
import shutil

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
        print(arguments)
        path_arguments = "/".join(arguments)
        print(path_arguments)
        full_url = urllib.parse.urljoin(self.root_url, path_arguments)

        response = requests.get(full_url, auth=HTTPBasicAuth(os.getenv('USER'), os.getenv('PASS')), stream=stream)
        if response.status_code != 200:
            raise Exception(f"status {response.status_code}: {response.text}")
        return response

    def is_product_online(self, product_id: str):
        response_text = self.do_request(["odata/v1", f"Products('{product_id}')/Online/$value"]).text
        return response_text == "true"

    def download_product(self, product_id: str, download_path: str, try_to_download=True):
        is_online = self.is_product_online(product_id)
        if try_to_download and is_online:
            response_raw = self.do_request(["odata/v1", f"Products('{product_id}')/$value"], stream=True).raw
            with open(download_path, 'wb') as out_file:
                shutil.copyfileobj(response_raw, out_file)


s = SentinelDownloader()
s.download_product("8364b44f-aa7f-4589-8695-44b7ed7b8f65", "hahaha")
