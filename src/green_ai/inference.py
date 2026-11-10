
from pathlib import Path
from io import BytesIO

import numpy as np
from PIL import Image, ImageOps

from ai_edge_litert.interpreter import Interpreter


BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "models" / "green_leaf_model_int8.tflite"

IMAGE_SIZE = (224, 224)

CLASS_NAMES = [
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
]


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    interpreter = Interpreter(model_path=str(MODEL_PATH))
    interpreter.allocate_tensors()

    return interpreter


interpreter = load_model()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def preprocess_image(image_bytes):
    try:
        image = Image.open(BytesIO(image_bytes))
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
        image = image.resize(IMAGE_SIZE)

        image_array = np.asarray(image, dtype=np.float32)
        image_array = np.expand_dims(image_array, axis=0)

        return image_array

    except Exception as error:
        raise ValueError("Could not read the uploaded image.") from error


def predict_image(image_bytes):
    image_array = preprocess_image(image_bytes)

    input_info = input_details[0]
    input_dtype = input_info["dtype"]

    if np.issubdtype(input_dtype, np.integer):
        scale, zero_point = input_info["quantization"]

        if scale <= 0:
            raise ValueError("Invalid model input quantization.")

        image_array = np.round(
            image_array / scale + zero_point
        )

        limits = np.iinfo(input_dtype)
        image_array = np.clip(
            image_array, limits.min, limits.max
        ).astype(input_dtype)

    else:
        image_array = image_array.astype(input_dtype)

    interpreter.set_tensor(
        input_info["index"],
        image_array
    )

    interpreter.invoke()

    output_info = output_details[0]
    predictions = interpreter.get_tensor(
        output_info["index"]
    )

    output_scale, output_zero_point = output_info["quantization"]

    if np.issubdtype(output_info["dtype"], np.integer):
        if output_scale > 0:
            predictions = (
                predictions.astype(np.float32) - output_zero_point
            ) * output_scale

    predictions = np.asarray(predictions).flatten()

    if len(predictions) != len(CLASS_NAMES):
        raise ValueError("Model output does not match the three classes.")

    predicted_index = int(np.argmax(predictions))
    confidence = float(predictions[predicted_index])

    return {
        "prediction": CLASS_NAMES[predicted_index],
        "confidence": confidence
    }
