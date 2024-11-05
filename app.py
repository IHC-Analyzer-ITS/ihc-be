from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
import os
from pathlib import Path
import cv2
from datetime import datetime

import numpy as np

from microscope import *
from segmentation import segment_image

app = FastAPI()

class FolderRequest(BaseModel):
    basedir: str
    project: str
    section: str

class ImageSaveRequest(BaseModel):
    basedir: str
    project: str
    section: str
    index: int

class Test(BaseModel):
    index: int
    dir: str

serCon = SerialController("COM3")

@app.get("/connect")
def connect():
    respond = serCon.connect("COM3")
    return {'massage': respond}

@app.post("/test")
def test_model(testing: Test):
    return {'massage': f"{testing.dir} {testing.index}"}


@app.post("/create-folder/")
async def create_folder(folder_req: FolderRequest):
    # Construct the folder path based on basedir, project, and section
    folder_path = os.path.join(folder_req.basedir, folder_req.project, folder_req.section)

    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # Create the folder if it doesn't exist
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        return {"message": f"Folder '{folder_path}' created successfully."}
    else:
        return {"message": f"Folder '{folder_path}' already existed"}

# Endpoint to capture and save an image to a specific folder
@app.post("/save-image/")
async def save_image(image_req: ImageSaveRequest):
    # Construct the folder path based on basedir, project, and section
    folder_path = os.path.join(image_req.basedir, image_req.project, image_req.section)

    # Check if folder exists
    if not os.path.exists(folder_path):
        raise HTTPException(status_code=400, detail="Folder does not exist")

    # Access the camera and capture an image
    cap = cv2.VideoCapture(image_req.index)  # Use 0 for the default camera
    ret, frame = cap.read()

    if not ret:
        raise HTTPException(status_code=500, detail="Failed to capture image")

    n = 5
    
    top, bottom = 0, n - 1
    left, right = 0, n - 1

    current_number = 1

    while top <= bottom and left <= right:
        # Fill top row (left to right)
        for i in range(left, right + 1):
            current_number += 1
            serCon.right()
            image_filename = f"{image_req.section}_{current_number}.png"
            image_path = os.path.join(folder_path, image_filename)
            cv2.imwrite(image_path, frame)
        top += 1  # Move the top boundary down

        # Fill right column (top to bottom)
        for i in range(top, bottom + 1):
            current_number += 1
            serCon.down()
            image_filename = f"{image_req.section}_{current_number}.png"
            image_path = os.path.join(folder_path, image_filename)
            cv2.imwrite(image_path, frame)
        right -= 1  # Move the right boundary left

        # Fill bottom row (right to left)
        if top <= bottom:
            for i in range(right, left - 1, -1):
                current_number += 1
                serCon.left()
                image_filename = f"{image_req.section}_{current_number}.png"
                image_path = os.path.join(folder_path, image_filename)
                cv2.imwrite(image_path, frame)
            bottom -= 1  # Move the bottom boundary up

        # Fill left column (bottom to top)
        if left <= right:
            for i in range(bottom, top - 1, -1):
                current_number += 1
                serCon.up()
                image_filename = f"{image_req.section}_{current_number}.png"
                image_path = os.path.join(folder_path, image_filename)
                cv2.imwrite(image_path, frame)
            left += 1  # Move the left boundary right
    
    cap.release()

    return {"message": "Image already captured"}

@app.post("/process-image/")
async def process_image_endpoint(file: UploadFile = File(...)):
    # Baca gambar dari file yang diunggah
    output_folder = "output_images"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Folder '{output_folder}' created.")

    image_bytes = await file.read()
    image_np = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Proses gambar menggunakan model YOLO dan SAM
    mask_img, detected_count = segment_image(image)

    # Tentukan path untuk menyimpan gambar hasil
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{file.filename.split('.')[0]}_segmented_{timestamp}.png"
    output_path = os.path.join(output_folder, filename)

    # Simpan gambar hasil segmentasi
    if mask_img.save(output_path):
        print(f"Gambar berhasil disimpan di {output_path}")
    else:
        print("Gagal menyimpan gambar.")

    # Kembalikan path gambar hasil dan jumlah objek yang terdeteksi
    return JSONResponse(content={"detected_count": detected_count, "output_image_path": output_path})

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)