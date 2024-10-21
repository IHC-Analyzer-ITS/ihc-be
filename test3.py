import cv2
import numpy as np

def combine_panorama_images(images):
    """
    Mengkombinasikan beberapa gambar menjadi panorama.

    Args:
        images: List gambar (NumPy arrays).

    Returns:
        Gambar panorama (NumPy array) atau None jika stitching gagal.
    """

    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    status, stitched_image = stitcher.stitch(images)

    if status != cv2.STITCHER_OK:
        print(f"Stitching gagal. Error code: {status}")
        return None

    # Cropping untuk menghilangkan border hitam
    stitched_image = crop_black_borders(stitched_image)

    return stitched_image


def crop_black_borders(img):
    """
    Cropping border hitam dari gambar.

    Args:
        img: Gambar (NumPy array).

    Returns:
        Gambar yang sudah di-crop (NumPy array).
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours[0])
    cropped_img = img[y:y+h, x:x+w]
    return cropped_img



# Contoh penggunaan:
img1 = cv2.imread("static/images/img_3_1.png")
img2 = cv2.imread("static/images/img_3_2.png")
img3 = cv2.imread("static/images/img_3_3.png")

images = [img1, img2, img3]

panorama = combine_panorama_images(images)

if panorama is not None:
    cv2.imwrite("panorama.jpg", panorama)
    cv2.imshow("Panorama", panorama)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

