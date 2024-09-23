from datetime import datetime
from flask import url_for
import os
import cv2
import json

def save_data_to_json(data, filename='data.json'):
    try:
        with open(filename,'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:

        existing_data = []

    

    existing_data.append(data)

    with open(filename,'w') as file:
        json.dump(existing_data, file, indent=4)

def check_duplicate(data):
    existing_data,_ = get_data_from_json()

    existing_names = [item['name'] for item in existing_data]

    is_duplicates = data in existing_names
    
    if is_duplicates:
        return True
    return False

def get_data_from_json(filename='data.json'):
    try:
        with open(filename,'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return {"error":"Missing data"}, 400
    
    return data, 200

def process_data(data):
    # Ambil elemen pertama dari list jika ada

        # Ambil nilai 'name' dari record, properti lainnya bisa diberi default
    name = data.get('name')

    if not name:
        return {"error": "Missing name"}, 400
    if not check_duplicate(data):
        return {"error": "nama sudah ada"},400


    # Set atribut lain secara default jika tidak ada
    timestamp_create = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_data = data.get('total_data', 0)
    sync_status = data.get('sync_status', "Not Synced")
    description = data.get('description', '')

    # Respon sukses setelah proses
    response = {
        "message": "Data received successfully",
        "name": name,
        "timestamp_create": timestamp_create,
        "total_data": total_data,
        "sync_status": sync_status,
        "description": description
    }

    save_data_to_json(response)

    return response, 200

def capture_image(user_name="reza"):
    user_folder = os.path.join('projects', user_name)
    os.makedirs(user_folder, exist_ok=True)

    existing_files = os.listdir(user_folder)
    image_count = len(existing_files) + 1

    camera = cv2.VideoCapture(0)    

    if not camera.isOpened():
        return {"error": "Cannot access the camera"}, 500
    
    ret, frame = camera.read()
    camera.release()

    if not ret:
        return {"error": "Failed to capture image"}, 500
    
    img_name = f'image_{image_count}.jpg'
    img_path = os.path.join(user_folder, img_name)
    cv2.imwrite(img_path, frame)

    return {"success": "Captured image successfully", "image_path": img_path}, 200

def projects_image(name):
    folder_path = f'projects/{name}'

    if not os.path.exists(folder_path):
        return {"error": "folder gak ada"}, 400
    
    images = []
    for file in os.listdir(folder_path):
        image_url = url_for('custom_static', filename=f'{name}/{file}', _external=True)
        images.append({"titel": file, "url":image_url})

    return images,200