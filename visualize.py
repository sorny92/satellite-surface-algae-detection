from eoreader.reader import Reader
from eoreader.bands import GREEN, NDVI, CLOUDS
from matplotlib import pyplot as plt


if __name__ == "__main__":
    file = "S2A_MSIL2A_20230325T112111_N0509_R037_T29SPD_20230325T172652.zip"
    prod = Reader().open(file)
    prod.plot()
    plt.show()