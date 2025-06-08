from pathlib import Path
from fastapi.responses import JSONResponse
from backend.detection import process_image, process_video
from backend.report_gen import generate_equipment_report
from backend.googcloud import upload_directory_to_gcs
import shutil

def handleFile(filepath, multimedia, type:str):
    location = filepath.UPLOAD_DIR/ multimedia.filename
    check_save = savefile(location,multimedia)
    if check_save:
        if type == "image":
            media = process_image(filepath.model, filepath.PROCESSED_IMAGE_DIR/multimedia.filename, location)
            report_json  = generate_equipment_report(filepath.REPORTS_DIR, media.report)
            return JSONResponse({
                "processed_image": str(media.path),
                "report": str(report_json)
            })
        elif type == "video":
            media = process_video(filepath.model, filepath.PROCESSED_VIDEO_DIR/multimedia.filename, location)
            report_json = generate_equipment_report(filepath.REPORTS_DIR, media.report)
            return JSONResponse({
                "processed_video": str(media.path),
                "report": str(report_json)
            })
    else:
        return JSONResponse({"error": "File not saved"}, status_code=500)


def savefile(location, multimedia):
    with open(location, "wb") as buffer:
            shutil.copyfileobj(multimedia.file, buffer)       
    if not location.is_file():
        return False
    else:
         return True
    
def delfiles(filepath):
    upload_directory_to_gcs(filepath.PROCESSED_IMAGE_DIR, 'processed_image')
    upload_directory_to_gcs(filepath.PROCESSED_VIDEO_DIR, 'processed_video')
    upload_directory_to_gcs(filepath.UPLOAD_DIR, 'uploads')
    upload_directory_to_gcs(filepath.REPORTS_DIR, 'reports')
