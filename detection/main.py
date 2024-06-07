import os
import cv2
import numpy as np
import easyocr
import util
from ultralytics import YOLO

# Define path to the model weights
model_weights_path = os.path.join('detection', 'model', 'weights', 'best.pt')

# Load the model
model = YOLO(model_weights_path)

def get_next_run_folder():
    base_path = os.path.join('runs_done')
    run_folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f)) and f.startswith('Run')]
    if not run_folders:
        return os.path.join(base_path, 'Run1')
    last_run_number = max([int(f[3:]) for f in run_folders])
    return os.path.join(base_path, f'Run{last_run_number + 1}')

def process_image(img_path, run_folder):
    img = cv2.imread(img_path)
    H, W, _ = img.shape

    # Perform detection using the model
    results = model.predict(source=img_path, save=False, imgsz=640)

    bboxes = []
    class_ids = []
    scores = []

    base_filename = os.path.basename(img_path).split('.')[0]

    # Extract bounding boxes, class IDs, and scores from the results
    for result in results:
        for detection in result.boxes:
            bbox = detection.xyxy[0].cpu().numpy()  # Get bounding box coordinates
            xc, yc, w, h = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2, bbox[2] - bbox[0], bbox[3] - bbox[1]
            bbox = [int(xc), int(yc), int(w), int(h)]
            score = detection.conf.cpu().numpy()[0]  # Get confidence score
            class_id = detection.cls.cpu().numpy()[0]  # Get class ID

            bboxes.append(bbox)
            class_ids.append(int(class_id))
            scores.append(float(score))

    # Perform Non-Maximum Suppression (NMS)
    bboxes, class_ids, scores = util.NMS(bboxes, class_ids, scores)

    reader = easyocr.Reader(['en'])
    results = []
    detected = False
    output_paths = []

    for bbox_ in bboxes:
        xc, yc, w, h = bbox_
        license_plate = img[int(yc - (h / 2)):int(yc + (h / 2)), int(xc - (w / 2)):int(xc + (w / 2)), :].copy()
        img = cv2.rectangle(img, (int(xc - (w / 2)), int(yc - (h / 2))), (int(xc + (w / 2)), int(yc + (h / 2))), (255, 105, 180), 15)
        license_plate_gray = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)
        _, license_plate_thresh = cv2.threshold(license_plate_gray, 64, 255, cv2.THRESH_BINARY_INV)
        output = reader.readtext(license_plate_thresh)

        # Debugging the OCR output
        print("OCR Output:", output)

        for out in output:
            text_bbox, text, text_score = out
            # Debugging the detected text and score
            print(f"Detected Text: {text}, Score: {text_score}")
            if text_score > 0.1:  # Ensure the score threshold is low enough to capture the detected text
                results.append((text, text_score))
                detected = True

        license_plate_path = os.path.join(run_folder, f'{base_filename}_license_plate.jpg')
        license_plate_gray_path = os.path.join(run_folder, f'{base_filename}_license_plate_gray.jpg')
        license_plate_thresh_path = os.path.join(run_folder, f'{base_filename}_license_plate_thresh.jpg')

        cv2.imwrite(license_plate_path, license_plate)
        cv2.imwrite(license_plate_gray_path, license_plate_gray)
        cv2.imwrite(license_plate_thresh_path, license_plate_thresh)

        output_paths.append(license_plate_path.replace("\\", "/"))
        output_paths.append(license_plate_gray_path.replace("\\", "/"))
        output_paths.append(license_plate_thresh_path.replace("\\", "/"))

    annotated_image_path = os.path.join(run_folder, f'{base_filename}_annotated.jpg')
    cv2.imwrite(annotated_image_path, img)
    output_paths.append(annotated_image_path.replace("\\", "/"))

    # Debugging the final results
    print("Results:", results)
    print("Detected:", detected)
    print("Output Paths:", output_paths)

    if not detected:
        results.append(("No license plate detected. Please choose another image with higher quality, ensuring the whole car is visible.", 0))

    output_paths = [os.path.relpath(path, 'runs_done').replace("\\", "/") for path in output_paths if isinstance(path, str)]

    return results, detected, output_paths
