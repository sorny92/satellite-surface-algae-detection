# Automatic detection of floating aquatic vegetation from remote sensing data

## Install deps:

```bash
poetry install
```

## Train Barlow Twins

```bash
python -m train.barlowtwins.train -h
```

To run the training with EuroSAT you need to Download EuroSAT:

[Download link](https://github.com/phelber/EuroSAT)

Then you generate a .csv with the train split:

```bash
python -m dataset.EuroSAT.generate_train_test_split /path/to/eurosat/folders
```

Feed the `train.csv` path to the train script

## Train linear classifier with EuroSAT

Follow the jupyter notebook `finetune_eurosat-linear.ipynb` to replicate it locally with EuroSAT.

## Train linear classifier with aquatic vegetation dataset

First the data needs to be downloaded runnning:

```bash
python -m scripts.download
```

You have to confiure the main function to fit your local system and also need an account for DHub from the Copernicus
program.

Once you have the dataset downloaded you can run the finetunning process.

Follow the jupyter notebook `finetune_mat-linear.ipynb` to replicate it locally with the local dataset.

## Visualize dataset

Also in the `inference` folder couple of jupyter notebooks can be found that allows you to use the model to do image
serach in a tile.