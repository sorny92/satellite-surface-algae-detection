import torch
from torch.utils.data import Dataset
import pathlib
from eoreader import utils


class EuroSAT(Dataset):
    def __init__(self, dataset_path, transforms=None, one_hot=False):
        self.image_paths = []
        self.transforms = transforms
        self.dataset_root = pathlib.Path(dataset_path).parent
        self.one_hot = one_hot
        if self.one_hot:
            from sklearn.preprocessing import LabelEncoder
            from sklearn.preprocessing import OneHotEncoder
            self.labels = ["AnnualCrop", "Forest", "HerbaceousVegetation", "Highway", "Industrial", "Pasture", "PermanentCrop", "Residential", "River", "SeaLake"]
            l_encoder = LabelEncoder()
            i_encoded = l_encoder.fit_transform(self.labels)
            o_encoder = OneHotEncoder(sparse=False)
            i_encoded = i_encoded.reshape(len(i_encoded), 1)
            self.one_hot_encoded = o_encoder.fit_transform(i_encoded)

            
        with open(dataset_path, "r") as f:
            for row in f:
                self.image_paths.append(row.strip())

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        p = pathlib.Path(self.image_paths[idx])
        label, path = p.parent.name, p
        im = utils.read(self.dataset_root / path, allow_pickle=True)
        im = torch.from_numpy(im.astype("int16").to_numpy())
        if self.transforms:
            im = self.transforms(im)
        if self.one_hot:
            label = torch.Tensor(self.one_hot_encoded[self.labels.index(label)])
        return im, label


if __name__ == "__main__":
    import sys

    es = EuroSAT(sys.argv[1])
    item = es[0]
    print(item)
