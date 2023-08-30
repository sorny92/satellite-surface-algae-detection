import torch
from train.barlowtwins import barlowtwins

if __name__ == "__main__":
    # torch.cuda.set_device(1)
    # torch.backends.cudnn.benchmark = True

    model = barlowtwins.BarlowTwins(1, 1, "1-1-1").backbone
    # print(model)
    # weights = torch.load("checkpoint/resnet50.pth", "cpu")
    weights = torch.load(
        "/home/esteve/fast_folder/satellite-surface-algae-detection/runs/Aug26_01-30-06_pop-os/iter_365.pth",
        "cpu")
    new_state_dict = {}
    for key, value in weights["model"].items():
        #print(key, )
        new_state_dict[".".join(key.split(".")[2:])] = value

    missing_keys, unexpected_keys = model.load_state_dict(new_state_dict, strict=False)
    #model.fc.weight.data.normal_(mean=0.0, std=0.01)
    #model.fc.bias.data.zero_()
    model.eval()

    import dataset.algae.reader as reader

    r = reader.Algae("/home/esteve/fast_folder/satellite-surface-algae-detection/dataset/algae")
    for v in r:
        input = v[0].type(torch.Tensor).unsqueeze(0)
        prediction = model(input)
        print(prediction[0])
