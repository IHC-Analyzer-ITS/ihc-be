import torch
import torchvision

print("PyTorch version:", torch.__version__)
print("Torchvision version:", torchvision.__version__)
print("CUDA is available:", torch.cuda.is_available())

import numpy as np
import matplotlib.pyplot as plt
import cv2

from ultralytics import YOLO
from segment_anything import SamPredictor, sam_model_registry

#SAM setup
def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)

def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)

def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))


# Load the trained YOLO model
model = YOLO('model/yolov8_ihc_segmentation.pt')

# Load image using OpenCV
image = cv2.imread('0_1010_0_1_2.jpg')

# Perform inference on a new image
results = model.predict(image)

# Access the first (and only) Results object in the list
results = results[0]

# Menghitung jumlah objek yang terdeteksi
detected_count = len(results.boxes)  # Menghitung jumlah kotak prediksi
print(f"Jumlah objek yang terdeteksi: {detected_count}")

# Array untuk menyimpan input_box dari bounding box
input_boxes = []  # This will store all bounding boxes

# Loop melalui kotak yang terdeteksi
for i, box in enumerate(results.boxes):
    x1, y1, x2, y2 = box.xyxy[0].int().tolist()
    input_boxes.append([x1, y1, x2, y2])

# Load SAM model
sam_checkpoint = "model/sam_vit_l_0b3195.pth"
model_type = "vit_l"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)

# Initialize SAM predictor
predictor = SamPredictor(sam)

# Prepare the image for SAM
predictor.set_image(image)  # Use the loaded image

# Start a single figure for displaying results
fig, axes = plt.subplots(1, 2, figsize=(15, 10))

# Display the original image
axes[0].imshow(image)
axes[0].set_title("Original Image")
axes[0].axis('off')

# Create an empty mask for ground truth
ground_truth_mask = np.zeros(image.shape[:2], dtype=np.uint8)

# Function to display the mask
def show_mask(mask, ax):
    # Show the mask
    masked_image = np.ma.masked_where(mask == 0, mask)
    ax.imshow(masked_image, cmap='jet', alpha=0.5)

# Loop through each bounding box and predict the mask
for i, input_box in enumerate(input_boxes):
    input_box = np.array([input_box])

    # Predict the mask using the bounding box from YOLO
    masks, _, _ = predictor.predict(
        point_coords=None,
        point_labels=None,
        box=input_box,
        multimask_output=False
    )

    # Tampilkan hasil segmentasi
    show_mask(masks[0], axes[0])  # Tampilkan mask hasil segmentasi

    # Tambahkan mask ke ground truth mask
    ground_truth_mask = np.maximum(ground_truth_mask, masks[0])  # Menggabungkan hasil mask

# Tampilkan ground truth mask pada gambar kedua
axes[1].imshow(ground_truth_mask, cmap='gray')
axes[1].set_title("Ground Truth Mask from SAM")
axes[1].axis('off')

plt.show()