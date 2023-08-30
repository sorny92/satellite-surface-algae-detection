import torch
from torch.utils.data import Dataset
import pathlib
import numpy as np


class Algae(Dataset):
    def __init__(self, dataset_path, transforms=None):
        self.dataset_path = pathlib.Path(dataset_path)
        self.image_paths = []
        self.transforms = transforms
        self.dataset_root = pathlib.Path(dataset_path).parent
        self.image_paths.extend((self.dataset_path / "algae").glob("*"))
        self.image_paths.extend((self.dataset_path / "no_algae").glob("*"))

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        p = pathlib.Path(self.image_paths[idx])
        label, path = p.parent.name, p
        im = np.load(self.dataset_root / path)
        ## Add the missing channel from eoreader to get 13
        if im.shape[0] == 12:
            im = np.concatenate((im[:9, ...], np.zeros((1, im.shape[-1], im.shape[-1])), im[9:, ...]))
        im = torch.from_numpy(im)
        if self.transforms:
            im = self.transforms(im)
        return im, label


if __name__ == "__main__":
    import sys

    es = Algae(sys.argv[1])
    item = es[0]
    print(item)
