import os
import argparse
import zipfile
import subprocess

DEFAULT_DATASET = 'vishesh2395/crops-disease-dataset'
TARGET_DIR = 'datasets/CropsDisease'


def extract_zip(zip_path, target_dir):
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Zip file not found: {zip_path}")
    os.makedirs(target_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(target_dir)
    print(f'Extracted {zip_path} to {target_dir}')


def download_kaggle(dataset, target_dir):
    try:
        subprocess.run(['kaggle', '--version'], check=True, stdout=subprocess.DEVNULL)
    except Exception:
        raise RuntimeError('Kaggle CLI is not installed or not available on PATH.')

    os.makedirs(target_dir, exist_ok=True)
    print(f'Downloading Kaggle dataset {dataset} to {target_dir}...')
    subprocess.run(['kaggle', 'datasets', 'download', '-d', dataset, '-p', target_dir, '--force'], check=True)
    zip_path = os.path.join(target_dir, dataset.split('/')[-1] + '.zip')
    if os.path.exists(zip_path):
        extract_zip(zip_path, target_dir)
        os.remove(zip_path)
    else:
        print('Download complete, but no zip archive was found. Please check the target folder.')


def main():
    parser = argparse.ArgumentParser(description='Prepare the crop disease dataset for Agrolinga.')
    parser.add_argument('--dataset', default=DEFAULT_DATASET, help='Kaggle dataset identifier')
    parser.add_argument('--target', default=TARGET_DIR, help='Directory to store the extracted dataset')
    parser.add_argument('--zip', help='Use a local zip file instead of downloading from Kaggle')
    parser.add_argument('--skip-download', action='store_true', help='Do not download; just extract a local zip file')
    args = parser.parse_args()

    if args.zip:
        if args.skip_download:
            extract_zip(args.zip, args.target)
            return
        print('Extracting provided zip file...')
        extract_zip(args.zip, args.target)
        return

    if args.skip_download:
        print('Skip download was requested, but no zip path was provided.')
        return

    try:
        download_kaggle(args.dataset, args.target)
        print('Dataset is ready in', args.target)
        print('Expected training root: datasets/CropsDisease/Final_Dataset')
    except Exception as e:
        print('Could not download dataset automatically:', e)
        print('Manual steps:')
        print('1. Install Kaggle CLI: pip install kaggle')
        print('2. Configure KAGGLE_USERNAME and KAGGLE_KEY environment variables')
        print(f'3. Download the dataset manually from https://www.kaggle.com/datasets/{args.dataset}')
        print('4. Extract the archive under datasets/CropsDisease/Final_Dataset')


if __name__ == '__main__':
    main()
