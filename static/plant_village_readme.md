# Crop Disease Dataset

This project now targets a broader crop disease dataset that includes key
Indian crops such as wheat, rice/paddy, maize/corn, and potato. The model is
built to support multi-crop disease classification from a single image.

## Recommended Dataset Source

A suitable dataset is the Kaggle crop disease dataset:

- https://www.kaggle.com/datasets/vishesh2395/crops-disease-dataset

That dataset is organized with separate folders for each crop and disease class,
which works well with the Agrolinga training pipeline.

## Expected Dataset Layout

Place the extracted dataset under one of the supported locations:

- `datasets/CropsDisease/Final_Dataset`
- `datasets/crops-disease-dataset/Final_Dataset`
- `dataset/CropsDisease/Final_Dataset`
- `dataset/crops-disease-dataset/Final_Dataset`

The training scripts will detect any of those paths automatically.

## Training

Run:

```bash
python train_disease_model_fixed.py --dataset datasets/CropsDisease/Final_Dataset --imagenet
```

This produces `models/disease_model.h5` and `models/class_mapping.json`.

## Prediction

Use the existing prediction entry point:

```bash
python predict_disease.py path/to/image.jpg --pretty
```

If the trained model is missing, the app will fall back to a simple heuristic.

## Notes

- The new integration is designed for the Kaggle-style multi-crop dataset.
- It can be extended to additional crops by adding directories at the dataset root.
- The pipeline expects image directories named after class labels (for example,
  `Wheat___Healthy`, `Rice___BrownSpot`, `Corn___Common_Rust`).
