# Green AI Crop Doctor 🌿

A potato-leaf disease **screening prototype** using MobileNetV3Small and TensorFlow Lite.

It currently targets three PlantVillage potato classes:

- `Potato___Early_blight`
- `Potato___Late_blight`
- `Potato___healthy`

> **Important:** This is an educational screening tool, not a confirmed diagnosis or pesticide recommendation. Its PlantVillage-based evaluation does not establish real-farm performance. Confirm concerns with a qualified local agricultural extension professional.

## Architecture

```text
Browser UI (HTML/CSS/JS)
        |
        | POST /api/predict
        v
FastAPI backend
        |
        v
TFLite inference module
        |
        v
MobileNetV3Small model + labels.json

Training and evaluation are separate:
training/Green_AI_Crop_Doctor_Potato_Revised.ipynb
```

## Repository layout

```text
green-ai-crop-doctor/
├── backend/
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── src/green_ai/
│   ├── __init__.py
│   └── inference.py
├── training/
│   └── Green_AI_Crop_Doctor_Potato_Revised.ipynb
├── models/
│   ├── .gitkeep
│   └── README.md
├── tests/
│   └── test_api_contract.py
├── .gitignore
├── requirements.txt
├── requirements-training.txt
└── README.md
```

## 1. Train and export the model

Open the notebook in Jupyter or Google Colab and run it from top to bottom. The notebook exports files into its `model/` directory.

Copy these two files into this repository's `models/` directory:

- `green_leaf_model_int8.tflite`
- `labels.json`

The backend uses the INT8 model. The label order must be the exact output order produced during training.

The model is not included in this Git repository. Model binaries can be large; keep them out of normal Git history. For a public demo, use Git LFS or a versioned release asset if appropriate.

## 2. Run locally

Python 3.10 or 3.11 is recommended.

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Place the model files in `models/`, then start the API from the repository root:

```bash
uvicorn backend.main:app --reload
```

Open the frontend by visiting:

```text
http://127.0.0.1:8000/
```

API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 3. If Google Colab is not working

You do not need Colab to run the frontend or API once the model files exist. You can:

1. Train in a local Jupyter environment if your computer has enough RAM.
2. Use Kaggle Notebooks as an alternative hosted notebook environment.
3. Ask a teammate or use a suitable GPU machine to run training once, then download the exported `.tflite` and `labels.json`.
4. Continue frontend and backend development with the model files temporarily absent; the API will clearly report that the model is not installed.

If Colab fails, capture the **first red traceback**, not only the final error line. The exact error is needed to diagnose whether it is a package, runtime, memory, download, or notebook issue.

## 4. GitHub

Create an empty GitHub repository named `green-ai-crop-doctor`. From this folder:

```bash
git init
git add .
git commit -m "Initial Green AI Crop Doctor application"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/green-ai-crop-doctor.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Do not commit private tokens, personal data, datasets, or large model binaries.

## 5. Before publishing

- [ ] Add the trained TFLite model and matching labels (or document where to obtain them).
- [ ] Test the same images against Keras FP32, TFLite FP32 and TFLite INT8.
- [ ] Evaluate on independent field photographs, not only PlantVillage test images.
- [ ] Tune confidence and top-two-margin thresholds on validation data only.
- [ ] Add screenshots of the working app to the README.
- [ ] Record measured latency and model size from your target device.
- [ ] Clearly state limitations and avoid claims of field-ready diagnosis.

## Current limitations

- The model only knows three potato classes. It is not a general plant identifier.
- Low-confidence and low-margin predictions are returned as uncertain, but this is not robust out-of-distribution detection.
- A healthy prediction does not prove that the plant is disease-free.
- No chemical product, dose, tank mix, or spray approval is generated.
