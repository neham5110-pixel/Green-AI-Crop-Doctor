
# Model Files

Place the trained TensorFlow Lite model files in this directory.

## Required files

- `green_leaf_model_int8.tflite` — quantized potato disease classification model.
- `labels.json` — model class labels.

## Model information

- Architecture: MobileNetV3Small
- Input size: 224 × 224
- Colour format: RGB
- Classes:
  - Potato___Early_blight
  - Potato___Late_blight
  - Potato___healthy

Model binaries are excluded from Git by `.gitignore`. They should be distributed separately or through Git LFS.
