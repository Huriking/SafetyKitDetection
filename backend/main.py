from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pathlib import Path
from backend.googcloud import ensure_model_downloaded_from_gcs
from backend.middleLayer import delfiles, handleFile
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import os
from google.cloud import storage
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://protect-iq.el.r.appspot.com/"],  # For production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class filepaths:
    def __init__(self):
        # Determine base directory
        if os.getenv("GAE_ENV", "").startswith("standard") or os.getenv("K_SERVICE"):
            base_dir = Path("/tmp")  # GAE temporary directory
        else:
            base_dir = Path(__file__).resolve().parent  # Local development directory
        self.CURRENT_DIR = base_dir
        self.FRONTEND_DIR = base_dir.parent / "frontend"
        self.UPLOAD_DIR = base_dir / "uploads"  # Temporary storage for uploads
        self.PROCESSED_IMAGE_DIR = base_dir / "processed_image"  # Temporary processed images
        self.PROCESSED_VIDEO_DIR = base_dir / "processed_video"  # Temporary processed video
        self.REPORTS_DIR = base_dir / "reports"  # Temporary report storage
        self.MODEL_DIR = base_dir / "models"  # Model storage, ensure downloading if necessary

        # Create directories on local or temporary storage (in GAE, only /tmp is writable)
        self.FRONTEND_DIR.mkdir(parents=True, exist_ok=True)
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.PROCESSED_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        self.PROCESSED_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
        self.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        self.MODEL_DIR.mkdir(parents=True, exist_ok=True)

        # Ensure model is available — handles GCP download if needed
        model_path = ensure_model_downloaded_from_gcs(self.MODEL_DIR)

        # Load YOLO model
        from ultralytics import YOLO
        self.model = YOLO(str(model_path))

filepath=filepaths()
app.mount("/static", StaticFiles(directory=filepath.FRONTEND_DIR), name="static")
app.mount("/reports",StaticFiles(directory=filepath.REPORTS_DIR), name="static")
app.mount("/processed_video", StaticFiles(directory=filepath.PROCESSED_VIDEO_DIR), name="static")
app.mount("/processed_image", StaticFiles(directory=filepath.PROCESSED_IMAGE_DIR), name="static")

@app.get("/")
async def read_index():
    response = FileResponse(filepath.FRONTEND_DIR/"index2.html", media_type="text/html")
    response.headers["Cache-Control"] = "no-store"
    return response

@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    response= handleFile(filepath, file, "image")
    return response

@app.post("/upload/video/")
async def upload_video(file: UploadFile = File(...)):
    response= handleFile(filepath, file, "video")
    return response

@app.post("/terminate")
async def terminate():
    delfiles(filepath)

