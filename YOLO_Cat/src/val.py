#######
#  Need to run 'python src/val.py' from the root directory
#  Need to download the yolov5s.pt to the root directory
#  Need to download the best_model.pth to the root directory
#######
try:
    from ultralytics import YOLO
except:
    import sys
    sys.path.append('') # Chage to the path to the root directory if fail to import ultralytics
    from ultralytics import YOLO
from ultralytics.utils import SETTINGS
from ultralytics.utils.plotting import Annotator, colors, save_one_box
from copy import deepcopy
import src.classification as classification
import numpy as np
from PIL import Image
import cv2 as cv
import torch
# from src.util import *
import argparse
from torchvision import models
import os

parser = argparse.ArgumentParser(description='Demo')
parser.add_argument('--img_path', type=str, default='', help='Path to the val folder')
parser.add_argument('--save_path', type=str, default='reslut', help='Path to save the result')
args = parser.parse_args()

# Load classifier convnextv2-n
# classifier, preprocess = classification.get_pretrained_model('convnextv2-n')
classifier = models.resnet50()
classifier.fc = torch.nn.Linear(2048, 5)

ckpt = torch.load('best_model.pth')
classifier.load_state_dict(ckpt)
classifier = classifier.cuda()
classifier.eval()

# Load YOLO model
detector = YOLO("yolov8s.pt")

def scale_boxes(box, ratio=1.0, image_shape=None):
    assert image_shape is not None
    x1, y1, x2, y2 = box
    width = box[2] - box[0]
    height = box[3] - box[1]
    new_height = height * ratio
    new_width = width * ratio
    # 扩大1.2倍
    # # 计算新的左上角和右下角坐标
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

def get_detcetion_boxes(model, img_path, save_path):
    """Get the detection boxes from img_path

    Args:
        model: YOLO model
        img_path: Path to the image

    Returns:
        (ori_img, bbox): Original image (nd.array) and the bounding boxes
    """
    result = model(img_path, verbose=False)[0]
    bbox = result.boxes
    ori_img = result.orig_img
    # save_path = img_path.split('.')[0] + '_detection.jpg'
    result.save(filename=save_path)
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


def get_batch(images_crop, labels=None):
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
    labels = torch.tensor(labels).repeat(len(batch)).t()
    return torch.cat(batch, dim=0), labels

corrects = 0
crops_count = 0
@torch.no_grad()
def classify_images(images_crop, label):
    """Classify the cropped images

    Args:
        images_crop (list): List of cropped images

    Returns:
        prob_list: confidence of the predicted class, list of floats
        pred_cls_list: predicted class, list of integers
    """
    prob_list = []
    pred_cls_list = []
    batch,labels = get_batch(images_crop, label)
    global crops_count
    crops_count += batch.size(0)
    
    batch = batch.cuda()
    labels = labels.cuda()
    output = classifier(batch)# .logits
    output = torch.nn.functional.softmax(output, dim=-1)
    # print(labels)
    # print(output)
    # exit()
    correct = torch.sum(torch.argmax(output, dim=-1) == labels)
    # print(correct)
    global corrects
    corrects += correct
    
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
                          example=names)
    for i,d in enumerate(boxes):
        c, conf, id = pred_cls[i], probs[i], None
        name = ("" if id is None else f"id:{id} ") + names[c]
        label = (f"{name} {conf:.2f}" if conf else name)
        box = d.xyxy.squeeze()
        annotator.box_label(box, label, color=colors(c, True), rotated=False)
    annotator.save(save_path)
    


if __name__ == "__main__":
    # Get preprocess for the classification model
    from torchvision.transforms import transforms
    import time
    transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    dir_list = os.listdir(args.img_path)
    class_names = {0: 'Persian cat', 1: 'Ragdolls', 2: 'Sphynx', 3: 'Pallas cat', 4: 'Singapura cat'}
    label_map = {
        'singapura_all': 4,
        'pallas_all': 3,
        'Sphynx_all': 2,
        'Ragdolls': 1,
        'Persian_cats': 0
    }
    count = 0
    time_start = time.time()
    for dir in dir_list:
        sample_list = os.listdir(f'{args.img_path}/{dir}')
        for sample in sample_list:
            IMGPATH = f'{args.img_path}/{dir}/{sample}'
            DETCPATH = f'results/detection/{dir}'
            ANNOPATH = f'results/annotated/{dir}'
            CROPPATH = f'results/crop/{dir}'
            os.makedirs(DETCPATH, exist_ok=True)
            os.makedirs(ANNOPATH, exist_ok=True)
            os.makedirs(CROPPATH, exist_ok=True)
            
            # get img, bbox, and croped images
            img, bbox = get_detcetion_boxes(detector, IMGPATH, save_path=os.path.join(DETCPATH, IMGPATH.split('/')[-1]))
            bbox = box_filter(bbox)
            images_crop = get_croped_imgs(img, bbox)
            
            label = label_map[dir]
            
            for i, img_crop in enumerate(images_crop):
                corp_save_path = os.path.join(CROPPATH,IMGPATH.split('/')[-1].split('.')[0] + f'_crop_{i}.jpg')
                cv.imwrite(corp_save_path, cv.cvtColor(img_crop, None))
            
            # Classify the cropped images
            if len(images_crop) != 0:
                
                prob_list, pred_cls_list = classify_images(images_crop, label)
            
                # Plot the results and save the annotated image
                save_path = os.path.join(ANNOPATH, IMGPATH.split('/')[-1])
                
                plot_results(
                    save_path,
                    img, 
                    bbox, 
                    prob_list, 
                    pred_cls_list, 
                    class_names)
                
            count += 1
    time_end = time.time()
    print(f'Processed Images: {count}')
    print(f'Classified Crops: {crops_count}')
    print('Classification Accuracy: {:.2f}%'.format(corrects/crops_count*100))
    print(f'Time: {time_end - time_start:.2f}s')