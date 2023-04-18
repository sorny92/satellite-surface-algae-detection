from eoreader.reader import Reader
from eoreader.bands import GREEN, NDVI, CLOUDS, BLUE
from matplotlib import pyplot as plt
import pandas as pd
from scripts.download import Downloader
import os

if __name__ == "__main__":
    data = pd.read_csv("dataset/DATOS_12_04_23.csv")
    d = Downloader(os.getenv('USER'), os.getenv('PASS'))
    for idx in range(data.shape[0]):
        print(data.loc[idx])
        polygon = data["POLYGON"][idx]
        date = data["Fecha"][idx]
        filename = data["NOMBRE_FICHERO"][idx]

        prod = Reader().open(filename)
        blue_band = prod.load([BLUE])
        blue_band[BLUE][:, ::50, ::50].plot()
        plt.show()
        break
