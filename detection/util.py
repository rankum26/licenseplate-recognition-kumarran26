import numpy as np
import cv2

# Non-Maximum Suppression (NMS) to filter out overlapping bounding boxes
def NMS(boxes, class_ids, confidences, overlapThresh=0.5):
    # Convert lists to numpy arrays
    boxes = np.asarray(boxes)
    class_ids = np.asarray(class_ids)
    confidences = np.asarray(confidences)

    # Return empty lists if no boxes are given
    if len(boxes) == 0:
        return [], [], []

    # Calculate the top-left and bottom-right coordinates of bounding boxes
    x1 = boxes[:, 0] - (boxes[:, 2] / 2)
    y1 = boxes[:, 1] - (boxes[:, 3] / 2)
    x2 = boxes[:, 0] + (boxes[:, 2] / 2)
    y2 = boxes[:, 1] + (boxes[:, 3] / 2)

    # Calculate the areas of the bounding boxes
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)

    # Initialize indices array
    indices = np.arange(len(x1))
    for i, box in enumerate(boxes):
        # Create temporary indices excluding the current box
        temp_indices = indices[indices != i]
        # Calculate intersection coordinates
        xx1 = np.maximum(box[0] - (box[2] / 2), boxes[temp_indices, 0] - (boxes[temp_indices, 2] / 2))
        yy1 = np.maximum(box[1] - (box[3] / 2), boxes[temp_indices, 1] - (boxes[temp_indices, 3] / 2))
        xx2 = np.minimum(box[0] + (box[2] / 2), boxes[temp_indices, 0] + (boxes[temp_indices, 2] / 2))
        yy2 = np.minimum(box[1] + (box[3] / 2), boxes[temp_indices, 1] + (boxes[temp_indices, 3] / 2))

        # Calculate width and height of the intersection box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # Compute the ratio of overlap
        overlap = (w * h) / areas[temp_indices]
        # If overlap is greater than the threshold, remove the bounding box
        if np.any(overlap) > overlapThresh:
            indices = indices[indices != i]

    # Return only the boxes at the remaining indices
    return boxes[indices], class_ids[indices], confidences[indices]

# Get outputs from the neural network
def get_outputs(net):
    # Get names of all layers in the network
    layer_names = net.getLayerNames()
    # Get output layers (the ones we are interested in for detection)
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    # Forward pass to get outputs
    outs = net.forward(output_layers)
    # Filter out low-confidence detections
    outs = [c for out in outs for c in out if c[4] > 0.1]
    return outs

# Draw bounding boxes on the image
def draw(bbox, img):
    xc, yc, w, h = bbox
    # Draw rectangle on the image
    img = cv2.rectangle(img,
                        (xc - int(w / 2), yc - int(h / 2)),
                        (xc + int(w / 2), yc + int(h / 2)),
                        (255, 105, 180), 20)  # Pink color (RGB: 255, 105, 180)
    return img
