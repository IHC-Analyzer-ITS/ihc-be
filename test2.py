import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def create_panorama(images):
    # Inisialisasi SIFT
    sift = cv2.SIFT_create()
    panorama = images[0]

    for i in range(1, len(images)):
        # Deteksi fitur dan deskriptor
        kp1, des1 = sift.detectAndCompute(panorama, None)
        kp2, des2 = sift.detectAndCompute(images[i], None)

        # Periksa apakah deskriptor kosong
        if des1 is None or des2 is None:
            print(f"Deskriptor kosong untuk gambar {i}. Melewati gambar ini.")
            continue  # Lewati gambar ini jika deskriptor kosong

        # Mencocokkan deskriptor
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
        matches = bf.match(des1, des2)

        # Urutkan matches berdasarkan jarak
        matches = sorted(matches, key=lambda x: x.distance)

        # Ambil titik-titik dari matches
        points1 = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        points2 = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

        # Estimasi matriks homografi
        if len(points1) >= 4 and len(points2) >= 4:
            matrix, _ = cv2.findHomography(points2, points1, cv2.RANSAC)

            # Warping gambar berikutnya
            height, width = panorama.shape[:2]
            panorama = cv2.warpPerspective(images[i], matrix, (width + images[i].shape[1], height))

            # Menempatkan panorama lama di tempatnya
            panorama[0:height, 0:width] = cv2.addWeighted(panorama[0:height, 0:width], 0.5, panorama[0:height, 0:width], 0.5, 0)

    return panorama

# Fungsi utama
if __name__ == "__main__":
    # Baca gambar
    image_paths = ['static/images/img_1_0.png', 'static/images/img_1_1.png', 'static/images/img_1_2.png']  # Ganti dengan jalur gambar Anda
    images = [cv2.imread(img_path) for img_path in image_paths]

    # Periksa apakah semua gambar berhasil dibaca
    for i, img in enumerate(images):
        if img is None:
            print(f"Gambar pada index {i} tidak dapat dibaca: {image_paths[i]}")
            exit()

    # Membuat panorama
    panorama = create_panorama(images)

    # Menampilkan hasil menggunakan Matplotlib
    plt.imshow(cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB))
    plt.axis('off')  # Menonaktifkan sumbu
    plt.show()

    # Simpan panorama
    cv2.imwrite('panorama.jpg', panorama)
