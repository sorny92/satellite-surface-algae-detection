from tqdm import tqdm

from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import os


# Para la recoleccion de datos se va a utilizar el
# POLYGON((41.37 0.29, 41.37 0.43, 41.22 0.43, 41.22 0.29, 41.37 0.29))


## DEvolver un xml con los uuid de las imagenes de interes
# https://scihub.copernicus.eu/dhus/search?q=footprint:"Intersects(POLYGON((41.37 0.29, 41.37 0.43, 41.22 0.43, 41.22 0.29, 41.37 0.29)))"


## Comprobar si la uuid esta disponible en el historico
# curl -u $USER:$PASS "https://scihub.copernicus.eu/dhus/odata/v1/Products('8364b44f-aa7f-4589-8695-44b7ed7b8f65')/Online/\$value"

## Descargar o hacer trigger del retrieval del historico
# curl -u $USER:$PASS "https://scihub.copernicus.eu/dhus/odata/v1/Products('8364b44f-aa7f-4589-8695-44b7ed7b8f65')/\$value"

api = SentinelAPI(os.getenv('USER'), os.getenv('PASS'), 'https://apihub.copernicus.eu/apihub')
api.download("8364b44f-aa7f-4589-8695-44b7ed7b8f65")
res = api.query("POLYGON((41.37 0.29, 41.37 0.43, 41.22 0.43, 41.22 0.29, 41.37 0.29))",
                date=("20230101", "20230120"),
                platformname='Sentinel-2',
                cloudcoverpercentage=(0, 30))
for v in res:
    print(v)
    for k in res[v]:
        print(f"    {k}")
        print(f"        {res[v][k]}")
    break