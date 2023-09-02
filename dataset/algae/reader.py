import torch
from torch.utils.data import Dataset
import pathlib
import numpy as np


class Algae(Dataset):
    def __init__(self, dataset_path, with_incognito=False, transforms=None):
        self.dataset_path = pathlib.Path(dataset_path)
        self.image_paths = []
        self.transforms = transforms
        if self.dataset_path.is_dir():
            self.dataset_root = pathlib.Path(dataset_path).parent
            self.image_paths.extend((self.dataset_path / "algae").glob("*"))
            self.image_paths.extend((self.dataset_path / "no_algae").glob("*"))
            if with_incognito:
                self.image_paths.extend((self.dataset_path / "incognito").glob("*"))
        else:
            with open(dataset_path, "r") as f:
                for r in f.readlines():
                    self.image_paths.append(r.strip())


    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        p = pathlib.Path(self.image_paths[idx])
        label, path = p.parent.name, p
        if self.dataset_path.is_dir():
            img_path = self.dataset_root / path
        else:
            img_path = path
        im = np.load(img_path)
        ## Add the missing channel from eoreader to get 13
        if im.shape[0] == 12:
            im = np.concatenate((im[:9, ...], np.zeros((1, im.shape[-1], im.shape[-1])), im[9:, ...]))
        im = torch.from_numpy(im)
        if self.transforms:
            im = self.transforms(im)
        if self.dataset_path.is_dir():
            if label == "incognito":
                label = "no_algae"
            return im, label
        else:
            if label == "incognito":
                label = [0.1]
            if label == "no_algae":
                label = [0.0]
            else:
                label = [1.0]
            return im, torch.FloatTensor(label)


if __name__ == "__main__":
    import sys

    es = Algae(sys.argv[1])
    item = es[0]
    print(item)
