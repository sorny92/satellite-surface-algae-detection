from PIL import Image
import torchvision.transforms as transforms
from .transforms.custom import BandsJitter, GaussianBlur


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
            #GaussianBlur(p=1.0),
            # Solarization(p=0.0),
            transforms.Lambda(lambda x: x.type(torch.Tensor)/32768)
            #transforms.Normalize(mean=[0.485, 0.456, 0.406],
            #                     std=[0.229, 0.224, 0.225])
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
            # transforms.Normalize(mean=[0.485, 0.456, 0.406],
            #                     std=[0.229, 0.224, 0.225])
        ])

    def __call__(self, x):
        y1 = self.transform(x)
        y2 = self.transform_prime(x)
        return y1, y2
