DEMO LINK:
https://agrolingua-production.up.railway.app/
# Agrolinga

AI multilingual farming assistant supporting image analysis, sensor data, and
voice interaction. Outputs disease detection, crop recommendations, organic
advice, and audio in English, Hindi and Telugu.

## Offline Usage & Sample Dataset

Agrolinga is designed to function without network connectivity. All core
prediction/advice logic relies on local rules and a small hard-coded dataset
for markets, crops and translations. For offline experimentation you can also
process an entire dataset of sensor readings using the included CSV file and
helper script.

### Sample Data

A sample file `offline_dataset.csv` is provided at the project root. It contains
columns for soil moisture, temperature, pH, NPK values, EC, CO₂, region,
weather and preferred language. You can edit or extend this file with your own
measurements.

### Batch Processing (Offline)

Run the `batch_analyze.py` script to process every row of the CSV and write a
JSON report to `static/offline_results.json` (which is within the workspace so
you can easily open it).

```sh
python batch_analyze.py
```

The output replicates the same advice generation logic used by the web
interface, including translations and market information, but it does not
require a running Flask server or any internet access.

### Offline Text‑to‑Speech

By default, Agrolinga attempts to generate audio using gTTS. If you are
completely offline gTTS will fail, but the rest of the application—including
batch processing—remains functional. You can optionally add an offline
TTS engine such as `pyttsx3` by updating `languages.py` if needed.

### Crop Disease Dataset

Agrolinga now supports a broader crop disease dataset covering wheat, rice
(paddy), maize/corn, and potato. The new training pipeline expects an
extracted dataset at one of these paths:

- `datasets/CropsDisease/Final_Dataset`
- `datasets/crops-disease-dataset/Final_Dataset`
- `dataset/CropsDisease/Final_Dataset`
- `dataset/crops-disease-dataset/Final_Dataset`

A recommended dataset source is:

- https://www.kaggle.com/datasets/vishesh2395/crops-disease-dataset

This dataset contains multi-crop classes for Wheat, Rice, Potato, and Corn,
so the model can learn a richer set of plant diseases beyond a single crop.

### Direct Disease Prediction

A one-step CLI is available for image-based disease prediction using the
trained crop disease model.

```sh
python predict_disease.py path/to/image.jpg --pretty
```

This uses `model_stub.process_image()` and will load `models/disease_model.h5`
if it exists. If the model is missing, the script falls back to heuristic
color-based detection.
