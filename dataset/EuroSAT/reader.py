import torch
from torch.utils.data import Dataset
import pathlib
from eoreader import utils


class EuroSAT(Dataset):
    def __init__(self, dataset_path, transforms=None):
        self.image_paths = []
        self.transforms = transforms
        self.dataset_root = pathlib.Path(dataset_path).parent
        with open(dataset_path, "r") as f:
            for row in f:
                self.image_paths.append(row.strip())

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        p = pathlib.Path(self.image_paths[idx])
        label, path = p.parent.name, p
        im = utils.read(self.dataset_root / path)
        im = torch.from_numpy(im.astype("float32").to_numpy())
        if self.transforms:
            im = self.transforms(im)
        return im, label


if __name__ == "__main__":
    import sys

    es = EuroSAT(sys.argv[1])
    item = es[0]
    print(item)
