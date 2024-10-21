from flask import Flask, render_template, request
import cv2
import numpy as np
import os

app = Flask(__name__)

# Path gambar besar sebagai sumber
BIG_IMAGE_PATH = "static/images/big_image.jpeg"

# Fungsi mengambil potongan gambar pada posisi tertentu
def capture_image_from_big_image(x, y, crop_size=(100, 100)):
    big_image = cv2.imread(BIG_IMAGE_PATH)

    step_size = (50,50)
    
    # Pastikan potongan tidak melewati batas gambar besar
    start_x = min(x * step_size[0], big_image.shape[1] - step_size[0])
    start_y = min(y * step_size[1], big_image.shape[0] - step_size[1])
    
    # Ambil potongan gambar
    cropped_image = big_image[start_y:start_y + crop_size[1], start_x:start_x + crop_size[0]]

    # Simpan potongan gambar
    file_name = f"static/images/img_{x}_{y}.png"
    cv2.imwrite(file_name, cropped_image)
    
    return file_name

# Fungsi untuk menggabungkan gambar menjadi panorama
def stitch_images1(image_files, num_cols):
    rows = []
    
    # Gabungkan gambar secara horizontal per baris
    for row in image_files:
        # Baca gambar di setiap baris dan gabungkan secara horizontal
        images_row = [cv2.imread(img) for img in row]  # Membaca gambar per baris
        row_combined = np.hstack(images_row) 
         # Menggabungkan baris secara horizontal
        rows.append(row_combined)

        stitcher = cv2
    
    # Gabungkan semua baris secara vertikal
    panorama = np.vstack(rows)
    
    # Simpan hasil panorama
    panorama_file = "static/images/panorama.png"
    cv2.imwrite(panorama_file, panorama)
    
    return panorama_file

def stitch_images(image_files, num_cols):

    cv2.ocl.setUseOpenCL(False)
    # Baca gambar-gambar dari file
    images = [cv2.imread(img) for img in sum(image_files, [])]  # Flatten the 2D list to 1D
    
    # Buat objek stitcher
    stitcher = cv2.Stitcher_create()

    # Lakukan stitching (penggabungan gambar)
    status, panorama = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        # Simpan hasil panorama
        panorama_file = "static/images/panorama_stitched.png"
        cv2.imwrite(panorama_file, panorama)
        return panorama_file
    else:
        raise Exception(f"Panorama stitching failed with status {status}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    width = int(request.form.get('width', 5))  # Parameter ukuran foto (misalnya 5)
    height = int(request.form.get('height', 5))
    
    # Array 2D untuk menyimpan file gambar
    image_files = [[None for _ in range(width)] for _ in range(height)]
    
    for y in range(height):
        if y % 2 == 0:  # Zigzag ke kanan
            for x in range(width):
                image_file = capture_image_from_big_image(x, y)
                image_files[y][x] = image_file
        else:  # Zigzag ke kiri
            for x in reversed(range(width)):
                image_file = capture_image_from_big_image(x, y)
                image_files[y][x] = image_file
    
    # Gabungkan gambar menjadi panorama
    panorama_file = stitch_images(image_files, width)
    
    return render_template('result.html', panorama_file=panorama_file)

if __name__ == '__main__':
    if not os.path.exists('static/images'):
        os.makedirs('static/images')
    app.run(debug=True)
