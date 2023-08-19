import torch
from torch.utils.data import Dataset
import pathlib
from eoreader import utils
import numpy as np
from dask import dataframe


class EuroSAT(Dataset):
    def __init__(self, dataset_path):
        path = pathlib.Path(dataset_path)
        image_paths = list(path.glob("*/*"))
        self.img_labels = [(p.parent.name, p) for p in image_paths]

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        label, path = self.img_labels[idx]
        im = utils.read(path)
        im = im.astype("uint16")
        return im, label


if __name__ == "__main__":
    import sys
    es = EuroSAT(sys.argv[1])
    item = es[0]
    print(item)
