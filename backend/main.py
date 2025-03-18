from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
from detection import process_image, process_video
from pathlib import Path

app = FastAPI()

UPLOAD_DIR = "backend/uploads"
PROCESSED_DIR = "backend/processed"
REPORTS_DIR = "backend/reports"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

@app.post("/upload/image/")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path, report_path = process_image(file_path)
    return JSONResponse({"processed_image": output_path, "report": report_path})

@app.post("/upload/video/")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path, report_path = process_video(file_path)
    return JSONResponse({"processed_video": output_path, "report": report_path})

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = Path(PROCESSED_DIR) / filename
    if file_path.exists():
        return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
    return JSONResponse({"error": "File not found"}, status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
