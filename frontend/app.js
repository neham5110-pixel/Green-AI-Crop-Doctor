
const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const predictButton = document.getElementById("predictButton");
const result = document.getElementById("result");

let selectedImage = null;

// Preview the selected image
imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];

    imagePreview.replaceChildren();
    result.textContent = "";
    selectedImage = null;

    if (!file) return;

    if (!file.type.startsWith("image/")) {
        result.textContent = "Please select a valid image file.";
        imageInput.value = "";
        return;
    }

    selectedImage = file;

    const preview = document.createElement("img");
    preview.src = URL.createObjectURL(file);
    preview.alt = "Selected potato leaf image";

    imagePreview.appendChild(preview);
});

// Send the image to the FastAPI backend
predictButton.addEventListener("click", async () => {
    if (!selectedImage) {
        result.textContent = "Please select a potato leaf image first.";
        return;
    }

    const formData = new FormData();
    formData.append("file", selectedImage);

    predictButton.disabled = true;
    result.textContent = "Analyzing image... Please wait.";

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Prediction failed.");
        }

        const prediction =
            data.prediction || data.class || data.predicted_class;

        const confidence = data.confidence;

        if (!prediction) {
            throw new Error("The server returned an unexpected response.");
        }

        result.textContent = confidence !== undefined
            ? `Prediction: ${prediction} | Confidence: ${(
                Number(confidence) * 100
            ).toFixed(2)}%`
            : `Prediction: ${prediction}`;

    } catch (error) {
        result.textContent = error.message ||
            "Could not connect to the prediction server.";
    } finally {
        predictButton.disabled = false;
    }
});
