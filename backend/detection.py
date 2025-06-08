import cv2
import json
from pathlib import Path
from datetime import datetime
import subprocess


class result:
    path=""
    report=""
CLASSES = ["Helmet", "Gloves", "Vest", "Boots", "Goggles", "None", "Person"]

def run_detection(model, img):
    return model(img)

def annotate_image(img, results):
    detected_items = {}
    for i, box in enumerate(results[0].boxes):
        xmin, ymin, xmax, ymax = box.xyxy[0]
        cls = int(box.cls[0])
        label = CLASSES[cls]

        unique_id = f"Person_{i}"
        if unique_id not in detected_items:
            detected_items[unique_id] = []

        detected_items[unique_id].append(label)

        cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (0, 255, 0), 2)
        cv2.putText(img, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return img, detected_items

def generate_report(file_path, detected_items):
    return json.dumps({
        "timestamp": str(datetime.now()),
        "file": file_path.name,
        "detections": detected_items
    }, indent=4)

# ------------------------------
# Image-Specific Functions
# ------------------------------

def read_image(image_path):
    print(image_path)
    return cv2.imread(str(image_path))

def save_image(img, output_image_path):
    success = cv2.imwrite(str(output_image_path), img)
    if not success:
        print("FAIIIIIIILLLLLLLL")
    return success

def process_image(model, output_image_path, image_path):
    print(output_image_path)
    img = read_image(image_path)
    results = run_detection(model, img)
    annotated_img, detected_items = annotate_image(img, results)
    save_image(annotated_img, output_image_path)

    result.path = Path("processed_image") / output_image_path.name
    result.report = generate_report(image_path, detected_items)
    return result

# ------------------------------
# Video-Specific Helper Functions
# ------------------------------

def open_video(video_path):
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"Failed to open video file: {video_path}")
        return None
    return cap

def get_video_properties(cap):
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f"Video properties: {frame_width}x{frame_height}, FPS: {fps}")
    return frame_width, frame_height, fps

def create_video_writer(output_video_path, frame_width, frame_height, fps):
    fourcc = cv2.VideoWriter_fourcc(*"X264")  # H.264 codec
    out = cv2.VideoWriter(str(output_video_path), fourcc, fps, (frame_width, frame_height))
    if not out.isOpened():
        print(f"Failed to open video writer with codec X264!")
        return None
    return out

def process_frame(model, frame, detected_items):
    results = run_detection(model, frame)
    annotated_frame, detections = annotate_image(frame, results)

    for k, v in detections.items():
        if k not in detected_items:
            detected_items[k] = []
        detected_items[k].extend(v)

    return annotated_frame

def close_video_resources(cap, out):
    cap.release()
    out.release()
    cv2.destroyAllWindows()

def reencode_video(input_video_path, output_video_path):
    """Re-encode the video to H.264 (video) and AAC (audio) for compatibility."""
    command = [
        'ffmpeg',
        '-i', str(input_video_path),
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-preset', 'fast',
        '-crf', '23',
        '-b:a', '192k',
        '-movflags', '+faststart',
        '-y',
        str(output_video_path)
    ]
    subprocess.run(command, check=True)
    delete_file(input_video_path)

def delete_file(delete_filepath: Path):
    try:
        if delete_filepath.exists() and delete_filepath.is_file():
            delete_filepath.unlink()
            print(f"Deleted video: {delete_filepath}")
        else:
            print(f"File not found or is not a file: {delete_filepath}")
    except Exception as e:
        print(f"Error deleting video: {delete_filepath}\n{e}")

def reencode_video_if_needed(output_video_path, video_path):
    reencoded_video_path = output_video_path.parent / (video_path.stem + "_reencoded.mp4")
    result.path = Path("processed_video") / reencoded_video_path.name
    print(result.path)
    reencode_video(output_video_path, reencoded_video_path)
    return reencoded_video_path

def generate_video_report(reencoded_video_path, detected_items):
    result.report = generate_report(reencoded_video_path, detected_items)
    print(f"Processed video saved at {reencoded_video_path}")
    return result

def process_video(model, output_video_path, video_path):
    cap = open_video(video_path)
    if not cap:
        return None, None

    frame_width, frame_height, fps = get_video_properties(cap)
    out = create_video_writer(output_video_path, frame_width, frame_height, fps)
    if not out:
        return None, None

    detected_items = {}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        annotated_frame = process_frame(model, frame, detected_items)
        out.write(annotated_frame)

    close_video_resources(cap, out)

    print(f"Initial processed video saved at {output_video_path}")

    reencoded_video_path = reencode_video_if_needed(output_video_path, video_path)
    return generate_video_report(reencoded_video_path, detected_items)

if __name__ == "__main__":
    # To process an image
    img_output, img_report = process_image("backend/test_images/sample.jpg")
    print(f"Processed Image Saved: {img_output}")
    print(f"Report Generated: {img_report}")

    # To process a video
    vid_output, vid_report = process_video("backend/test_videos/sample.mp4")
    print(f"Processed Video Saved: {vid_output}")
    print(f"Report Generated: {vid_report}")
