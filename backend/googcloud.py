from google.cloud import storage
from pathlib import Path, PurePosixPath  # Add this at the top if not already
import os
from backend.detection import delete_file

# Print to verify
print("GOOGLE_APPLICATION_CREDENTIALS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# ✅ Explicitly set your project ID
PROJECT_ID = "protect-iq"
GCS_BUCKET_NAME = "protect_iq"
MODEL_BLOB_PATH = "protect_iq/models/best.pt"

# ✅ Pass project ID here
storage_client = storage.Client(project=PROJECT_ID)

def ensure_model_downloaded_from_gcs(model_dir: Path) -> Path:
    """Ensures YOLO model is available locally, downloads from GCS if on GCP and missing."""
    model_path = model_dir / "best.pt"
    is_gcp = os.getenv("GAE_ENV", "").startswith("standard") or os.getenv("K_SERVICE")

    if not model_path.exists() and is_gcp:
        print("🧠 Model not found locally on GCP, downloading from GCS...")
        bucket = storage_client.get_bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(MODEL_BLOB_PATH)
        blob.download_to_filename(str(model_path))
        print(f"✅ Model downloaded to {model_path}")

    return model_path

def upload_to_gcs(local_file_path, gcs_blob_path):
    """Upload a single file from the local file system to Google Cloud Storage."""
    print(local_file_path,gcs_blob_path)
    bucket = storage_client.get_bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(gcs_blob_path)
    blob.upload_from_filename(local_file_path)
    print(f"✅ Uploaded: {local_file_path} → gs://{GCS_BUCKET_NAME}/{gcs_blob_path}")
    delete_file(local_file_path)
    print("deleted" + str(local_file_path))



def upload_directory_to_gcs(directory_path, gcs_directory_path):
    """Upload all files from a directory to a specific folder in the GCS bucket."""
    for file in Path(directory_path).glob('*'):
        if file.is_file():
            # 🔧 Normalize the blob path to use forward slashes
            gcs_file_path = str(PurePosixPath(gcs_directory_path) / file.name)
            upload_to_gcs(file, gcs_file_path)

