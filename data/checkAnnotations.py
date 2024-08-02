import os
import cv2
"""
    Demo
    根据设置的阈值显示像素面积过大或过小的标签
"""
# YOLO标注文件夹路径
annotations_path = r"D:\data\Detect\coco128\labels"
# 图像文件夹路径
images_path = r"D:\data\Detect\coco128\images"

def load_annotations(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    annotations = [list(map(float, line.strip().split())) for line in lines]
    return annotations

def visualize_annotations(image_path, annotations):
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    for annotation in annotations:
        class_id, x_center, y_center, w, h = annotation
        x1 = int((x_center - w / 2) * width)
        y1 = int((y_center - h / 2) * height)
        x2 = int((x_center + w / 2) * width)
        y2 = int((y_center + h / 2) * height)
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.imshow("Annotated Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def detect_anomalies(annotations, threshold_min_area=0.01, threshold_max_area=0.5):
    anomalies = []
    for annotation in annotations:
        _, x_center, y_center, w, h = annotation
        if x_center < 0 or x_center > 1 or y_center < 0 or y_center > 1:
            anomalies.append(annotation)
        area = w * h
        if area < threshold_min_area or area > threshold_max_area:
            anomalies.append(annotation)
    return anomalies

# 遍历所有标注文件
for annotation_file in os.listdir(annotations_path):
    annotation_path = os.path.join(annotations_path, annotation_file)
    image_path = os.path.join(images_path, annotation_file.replace('.txt', '.jpg'))
    
    annotations = load_annotations(annotation_path)
    anomalies = detect_anomalies(annotations)
    
    if anomalies:
        print(f"Anomalies detected in {annotation_file}: {anomalies}")
        visualize_annotations(image_path, anomalies)
