try:
    from ultralytics import YOLO
except:
    import sys
    sys.path.append('')
    from ultralytics import YOLO
from ultralytics.utils import SETTINGS
from ultralytics.utils.plotting import Annotator, colors, save_one_box
from copy import deepcopy
# import src.classifiction as classification
import numpy as np
from PIL import Image
import cv2 as cv
import torch
# from util import *
import argparse
from torchvision import models

parser = argparse.ArgumentParser(description='Demo')
parser.add_argument('--img_path', type=str, default='', help='Path to the image')
args = parser.parse_args()

# Load classifier convnextv2-n
# classifier, preprocess = classification.get_pretrained_model('convnextv2-n')
classifier = models.resnet50()
classifier.fc = torch.nn.Linear(2048, 5)

ckpt = torch.load('best_resnet50_model_99.4.pth')
classifier.load_state_dict(ckpt)
classifier = classifier.cuda()
classifier.eval()

# Load YOLO model
detector = YOLO("yolov10s.pt")

def scale_boxes(box, ratio=1.0, image_shape=None):
    assert image_shape is not None
    x1, y1, x2, y2 = box
    width = box[2] - box[0]
    height = box[3] - box[1]
    new_height = height * ratio
    new_width = width * ratio
    new_x1 = x1 - (new_width - width) / 2
    new_y1 = y1 - (new_height - height) / 2
    new_x2 = x1 + new_width
    new_y2 = y1 + new_height
    if new_x1 < 0:
        new_x1 = 0
    if new_y1 < 0:
        new_y1 = 0
    if new_y2 > image_shape[0]:
        new_y2 = image_shape[0]
    if new_x2 > image_shape[1]:
        new_x2 = image_shape[1]
    
    return [new_x1, new_y1, new_x2, new_y2]

def get_detcetion_boxes(model, img_path):
    """Get the detection boxes from img_path

    Args:
        model: YOLO model
        img_path: Path to the image

    Returns:
        (ori_img, bbox): Original image (nd.array) and the bounding boxes
    """
    result = model(img_path, verbose=False, conf=0.25)[0]
    bbox = result.boxes
    ori_img = result.orig_img
    # save_path = img_path.split('.')[0] + '_detection.jpg'
    # result.save(filename=save_path)
    return ori_img, bbox


def box_filter(boxes):
    """Fileter the boxes with class in [13, 23], which are the classes of cats and other animals in COCO

    Args:
        boxes: List of boxes

    Returns:
        new_boxes: List of boxes with class in [13, 23]
    """
    new_boxes = []
    for box in boxes:
        if box.cls in [15]:
            new_boxes.append(box)
    return new_boxes

def get_croped_imgs(img, boxes):
    """crop the images

    Args:
        img (nd.array): Original image
        boxes: Bounding boxes from the detection model

    Returns:
        images_cropped: List of cropped images
    """
    images_cropped = []
    
    for box in boxes:
        corrd = box.xyxy.squeeze().cpu().numpy().tolist()
        corrd = scale_boxes(corrd, 1.7, img.shape[:2])
        img_cropped = img[
            int(corrd[1]):int(corrd[3]),
            int(corrd[0]):int(corrd[2])
        ]
        images_cropped.append(img_cropped)
    return images_cropped


def get_batch(images_crop):
    """Pack the cropped images into a batch

    Args:
        images_crop (list): List of cropped images

    Returns:
        Tensor: a batch of images with shape (N, C, H, W) after preprocessing
    """
    batch = []
    for img_crop in images_crop:
        img = cv.cvtColor(img_crop, cv.COLOR_BGR2RGB) # Convert BGR to RGB
        img = Image.fromarray(img)
        img_crop = transforms(img).unsqueeze(0)
        batch.append(img_crop)
    return torch.cat(batch, dim=0)

def classify_images(images_crop):
    """Classify the cropped images

    Args:
        images_crop (list): List of cropped images

    Returns:
        prob_list: confidence of the predicted class, list of floats
        pred_cls_list: predicted class, list of integers
    """
    prob_list = []
    pred_cls_list = []
    batch = get_batch(images_crop).cuda()
    output = classifier(batch)# .logits
    output = torch.nn.functional.softmax(output, dim=-1)
    for i in range(output.size(0)):
        prob, predicted = torch.max(output[i], 0)
        try:
            prob_list.append(prob.item())
            pred_cls_list.append(predicted.item())
        except:
            pass
    return prob_list, pred_cls_list


def plot_results(save_path, img, boxes, probs, pred_cls, names):
    """Plot the results of the detection and classification

    Args:
        img: original image
        boxes: detection boxes after filtering
        probs: confidence of the predicted class
        pred_cls: predicted class
        names: class names dictionary for plotting
    """
    annotator = Annotator(deepcopy(img), 
                          pil=False,
                          example=names,
                          font_size=None,
                          line_width=None,)
    for i,d in enumerate(boxes):
        c, conf, id = pred_cls[i], probs[i], None
        name = ("" if id is None else f"id:{id} ") + names[c]
        label = (f"{name} {conf:.2f}" if conf else name)
        box = d.xyxy.squeeze()
        annotator.box_label(box, label, color=colors(c, True), rotated=False)
    return annotator.result()
    # annotator.save(save_path)
    

from torchvision.transforms import transforms
transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])


def pipeline(img_path):
    img, bbox = get_detcetion_boxes(detector, img_path)
    bbox = box_filter(bbox)
    images_crop = get_croped_imgs(img, bbox)
    if len(images_crop) == 0:
        # print('No cat detected')
        pass
        
    else:
        prob_list, pred_cls_list = classify_images(images_crop)
        # save_path = img_path.split('.')[0] + '_annotated.jpg'
    
    class_names = {0: 'Pallas cat', 1: 'Persian cat', 2: 'Ragdolls', 3: 'Singapura cat', 4: 'Sphynx'}
    return plot_results(
        None,
        img, 
        bbox, 
        prob_list if len(images_crop) > 0 else [], 
        pred_cls_list if len(images_crop) > 0 else [], 
        class_names)
    
    # return save_path

if __name__ == "__main__":
    
    IMGPATH = args.img_path
    # Get preprocess for the classification model
    
    # get img, bbox, and croped images
    img, bbox = get_detcetion_boxes(detector, IMGPATH)
    bbox = box_filter(bbox)
    images_crop = get_croped_imgs(img, bbox)
    
    if len(images_crop) == 0:
        print('No cat detected')
        exit()
        
    # To save the cropped images
    for i, img_crop in enumerate(images_crop):
        cv.imwrite(f'crop_{i}.jpg', cv.cvtColor(img_crop, None))
    
    # Classify the cropped images
    prob_list, pred_cls_list = classify_images(images_crop)
    
    # Plot the results and save the annotated image
    save_path = IMGPATH.split('.')[0] + '_annotated.jpg'
    class_names = {0: 'Persian cat', 1: 'Ragdolls', 2: 'Sphynx', 3: 'Pallas cat', 4: 'Singapura cat'}
    plot_results(
        save_path,
        img, 
        bbox, 
        prob_list, 
        pred_cls_list, 
        class_names)