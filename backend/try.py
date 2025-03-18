import os
from ultralytics import YOLO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the current script directory
MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")  # Correct path

# Ensure the model file exists before loading
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

# Load the YOLOv8 model
model = YOLO(MODEL_PATH)
print("✅ YOLOv8 model loaded successfully!")
