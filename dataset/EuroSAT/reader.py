import torch
from torch.utils.data import Dataset
import pathlib
from eoreader import utils
import numpy as np
from dask import dataframe


class EuroSAT(Dataset):
    def __init__(self, dataset_path):
        self.image_paths = []
        with open(dataset_path, "r") as f:
            for row in f:
                self.image_paths.append(row.strip())

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        p = pathlib.Path(self.image_paths[idx])
        label, path = p.parent.name, p
        im = utils.read(path)
        im = im.astype("uint16")
        return im, label


if __name__ == "__main__":
    import sys

    es = EuroSAT(sys.argv[1])
    item = es[0]
    print(item)
