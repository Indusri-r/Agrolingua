import os
print("Crop disease dataset already partially extracted to datasets/CropsDisease/Final_Dataset")
print("Using existing structure for training.")

# Skip zip extraction - use manual extraction
dataset_dir = "datasets/CropsDisease/Final_Dataset"
if not os.path.exists(dataset_dir):
    dataset_dir = "datasets/crops-disease-dataset/Final_Dataset"

print("Dataset:", dataset_dir)
print("Classes found:", [d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))][:10])
print("\nRun: python train_disease_model_fixed.py --dataset datasets/CropsDisease/Final_Dataset")
print("or manually extract the dataset and then retry training.")
