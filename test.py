import cv2
import numpy as np

def stitch_images(image_paths):
    # Baca gambar-gambar
    images = [cv2.imread(img_path) for img_path in image_paths]
    
    # Periksa jika ada gambar yang gagal dibaca
    if any(img is None for img in images):
        raise Exception("Satu atau lebih gambar gagal dibaca.")
    
    # Buat objek stitcher
    stitcher = cv2.Stitcher_create()

    # Lakukan stitching (penggabungan gambar)
    status, panorama = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        # Simpan hasil panorama
        panorama_path = "static/images/panorama_stitched.png"
        cv2.imwrite(panorama_path, panorama)
        return panorama_path
    else:
        raise Exception(f"Stitching gagal dengan status: {status}")

# Path dari gambar yang ingin digabungkan
image_paths =['static/images/img_0_0.png', 'static/images/img_1_0.png', 'static/images/img_2_0.png']  # Sesuaikan dengan path gambar yang ingin kamu gunakan

# Gabungkan gambar
try:
    combined_image_path = stitch_images(image_paths)
    print(f"Gambar berhasil digabungkan dan disimpan di: {combined_image_path}")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")
