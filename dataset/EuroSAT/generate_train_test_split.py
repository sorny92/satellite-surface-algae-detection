import math
import pathlib
import sys
import random

def write2file(path, list):
    with open(path, "w") as f:
        for i in list:
            f.write(f"{i}\n")

path = pathlib.Path(sys.argv[1])
image_paths = list(path.glob("*/*"))
image_paths = sorted(image_paths)

random.seed(1992)
random.shuffle(image_paths)
ratio = 0.8
train_set, test_set = image_paths[:math.floor(len(image_paths) * ratio)], \
    image_paths[math.floor(len(image_paths) * ratio):]

print(len(train_set))
print(len(test_set))

write2file("train.csv", train_set)
write2file("test.csv", test_set)