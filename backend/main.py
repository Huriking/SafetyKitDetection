from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
from detection import process_image, process_video
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware 
import base64
import json

app = FastAPI()

UPLOAD_DIR = "backend/uploads"
PROCESSED_DIR = "backend/processed"
REPORTS_DIR = "backend/reports"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    print("Inside the image router")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    print("File path:", file_path)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    base64_image, report_json = process_image(file_path)
    
    return JSONResponse({
        "processed_image": base64_image,
        "report": report_json
    })

@app.post("/upload/video/")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Debug: Check if the file is really saved
    if not os.path.exists(file_path):
        return JSONResponse({"error": "File not saved"}, status_code=500)

    # Process video function
    video_base64, report_json = process_video(file_path)

    return JSONResponse({"processed_video": video_base64, "report": report_json})


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = Path(PROCESSED_DIR) / filename
    if file_path.exists():
        return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
    return JSONResponse({"error": "File not found"}, status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
