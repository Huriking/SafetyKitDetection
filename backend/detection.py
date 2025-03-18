import cv2
import os
import json
from datetime import datetime
from ultralytics import YOLO

# Base directory (script location)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Absolute Paths
MODEL_PATH = os.path.join(BASE_DIR, "models", "best.pt")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Ensure directories exist
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Load YOLO model from local weights
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

model = YOLO(MODEL_PATH)

# Define class labels
CLASSES = ["Helmet", "Gloves", "Vest", "Boots", "Goggles", "None", "Person"]

def process_image(image_path):
    """Process an image and save detection results."""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    img = cv2.imread(image_path)
    results = model(img)

    detected_items = {}
    
    for i, box in enumerate(results[0].boxes):
        xmin, ymin, xmax, ymax = box.xyxy[0]  # Bounding box coordinates
        cls = int(box.cls[0])  # Class index
        label = CLASSES[cls]  # Get class label

        unique_id = f"Person_{i}"
        if unique_id not in detected_items:
            detected_items[unique_id] = []
        
        detected_items[unique_id].append(label)
        
        cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
        cv2.putText(img, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save processed image
    output_path = os.path.join(PROCESSED_DIR, os.path.basename(image_path))
    cv2.imwrite(output_path, img)

    # Generate and save detection report
    report_path = generate_report(detected_items, image_path)
    return output_path, report_path

def process_video(video_path):
    """Process a video and save detection results frame by frame."""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Input video not found: {video_path}")

    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    output_video_path = os.path.join(PROCESSED_DIR, os.path.basename(video_path))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    detected_items = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for i, box in enumerate(results[0].boxes):
            xmin, ymin, xmax, ymax = box.xyxy[0]
            cls = int(box.cls[0])
            label = CLASSES[cls]

            unique_id = f"Person_{i}"
            if unique_id not in detected_items:
                detected_items[unique_id] = []
            detected_items[unique_id].append(label)

            cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
            cv2.putText(frame, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        out.write(frame)  # Save processed frame to video

    cap.release()
    out.release()

    # Generate and save detection report
    report_path = generate_report(detected_items, video_path)
    return output_video_path, report_path

def generate_report(detected_items, file_path):
    """Generate a JSON report for detected objects."""
    report_data = {
        "timestamp": str(datetime.now()),
        "file": os.path.basename(file_path),
        "detections": detected_items
    }
    
    report_path = os.path.join(REPORTS_DIR, f"{os.path.basename(file_path)}.json")
    with open(report_path, "w") as f:
        json.dump(report_data, f, indent=4)
    
    return report_path

# Example Usage
if __name__ == "__main__":
    # To process an image
    img_output, img_report = process_image("backend/test_images/sample.jpg")
    print(f"Processed Image Saved: {img_output}")
    print(f"Report Generated: {img_report}")

    # To process a video
    vid_output, vid_report = process_video("backend/test_videos/sample.mp4")
    print(f"Processed Video Saved: {vid_output}")
    print(f"Report Generated: {vid_report}")
