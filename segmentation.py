import numpy as np
import cv2
import torch
from PIL import Image
from ultralytics import YOLO
from segment_anything import SamPredictor, sam_model_registry
import matplotlib.pyplot as plt

# Load YOLO model
model = YOLO('model/yolov8_ihc_segmentation.pt')

# Load SAM model
sam_checkpoint = "model/sam_vit_l_0b3195.pth"
model_type = "vit_l"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
predictor = SamPredictor(sam)

def segment_image(image: np.ndarray):
    # Perform YOLO inference
    results = model.predict(image)[0]
    detected_count = len(results.boxes)

    # Extract bounding boxes
    input_boxes = []
    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].int().tolist()
        input_boxes.append([x1, y1, x2, y2])

    # Initialize SAM predictor with image
    predictor.set_image(image)

    # Prepare mask image
    ground_truth_mask = np.zeros(image.shape[:2], dtype=np.uint8)

    # Segment objects using SAM
    for input_box in input_boxes:
        input_box = np.array([input_box])
        masks, _, _ = predictor.predict(
            point_coords=None,
            point_labels=None,
            box=input_box,
            multimask_output=False
        )
        ground_truth_mask = np.maximum(ground_truth_mask, masks[0])

    # Convert mask to image for response
    mask_img = Image.fromarray((ground_truth_mask * 255).astype(np.uint8))
    return mask_img, detected_count

# input_image = cv2.imread('0_1010_0_1_2.jpg')
# mask_img, detected_count = segment_image(input_image)

# mask_img.save('output_images/mask123.png')
# print(f'jumlah objek terdeteksi: {detected_count}')