import torch
from PIL import Image
import torchvision.transforms as transforms
from .transforms.custom import BandsJitter, GaussianBlur


def totensor(img):
    return img.type(torch.Tensor)


class Transform:
    def __init__(self):
        self.transform = transforms.Compose([
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomAffine(degrees=360, translate=(0.2, 0.2), shear=15),
            transforms.RandomResizedCrop(64, interpolation=Image.BICUBIC, antialias=True),
            transforms.RandomApply(
                [BandsJitter(brightness=0.4, contrast=0.4)],
                p=0.8
            ),

            #     [transforms.ColorJitter(brightness=0.4, contrast=0.4,
            #                             saturation=0.2, hue=0.1)],
            #     p=0.8
            # ),
            # transforms.RandomGrayscale(p=0.2),
            # GaussianBlur(p=1.0),
            # Solarization(p=0.0),
            transforms.Lambda(totensor),
            # transforms.Normalize(mean=[0.485, 0.456, 0.406],
            #                     std=[0.229, 0.224, 0.225])
            transforms.Normalize(
                mean=[1353.47241558, 1116.58903239, 1040.76400427, 944.92769168, 1197.13633491,
                      2001.1258392, 2372.19987777, 2299.35905499, 731.49383711, 12.09341896,
                      1819.96556774, 1117.73135099, 2597.75184181],
                std=[1795.36927147, 3369.6875368, 3728.19663279, 5280.00906632,
                     4135.21948761, 7225.77528867, 9559.73767298, 10511.2101723,
                     2448.69314796, 19.59578514, 7313.52696182, 5577.66424732,
                     10917.50918372])
        ])
        self.transform_prime = transforms.Compose([
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomAffine(degrees=360, translate=(0.2, 0.2), shear=15),
            transforms.RandomResizedCrop(64, interpolation=Image.BICUBIC, antialias=True),
            transforms.RandomApply(
                [BandsJitter(brightness=0.4, contrast=0.4)],
                p=0.8
            ),

            # transforms.RandomApply(
            #     [transforms.ColorJitter(brightness=0.4, contrast=0.4,
            #                             saturation=0.2, hue=0.1)],
            #     p=0.8
            # ),
            # transforms.RandomGrayscale(p=0.2),
            # GaussianBlur(p=0.1),
            # Solarization(p=0.2),
            transforms.Lambda(totensor),
            transforms.Normalize(
                mean=[1353.47241558, 1116.58903239, 1040.76400427, 944.92769168, 1197.13633491,
                      2001.1258392, 2372.19987777, 2299.35905499, 731.49383711, 12.09341896,
                      1819.96556774, 1117.73135099, 2597.75184181],
                std=[1795.36927147, 3369.6875368, 3728.19663279, 5280.00906632,
                     4135.21948761, 7225.77528867, 9559.73767298, 10511.2101723,
                     2448.69314796, 19.59578514, 7313.52696182, 5577.66424732,
                     10917.50918372])
        ])

    def __call__(self, x):
        y1 = self.transform(x)
        y2 = self.transform_prime(x)
        return y1, y2
