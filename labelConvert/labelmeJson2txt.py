"""
    Description:Labelme json format annotation file conversion to txt (for YOLO and PPOCR)
                Labelme json file needs to add text recognition in the description field
                It will output the annotation folder in YOLO format and the annotation folder in PPOCR format
                (with pictures and text cropped images for PPOCR text recognition) in the specified directory.
    Author:BrilliantBirtch(白彬楠)
    Date:2024/7/29
    E-mail:990563378@qq.com
"""
import json
import os
import argparse
import cv2
import glob
import threading 
import shutil
from tqdm import tqdm

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--labelmeJson',type=str,default=r'E:\OCRSceneImage\Trk\labelme',help='Directory of Labelme json format labeled files')
    parser.add_argument('--yoloOutputDir',type=str,default=os.path.join(Root,'YOLO'),help='Specify the directory to output YOLO format')
    parser.add_argument('--ppocrOutputDir',type=str,default=os.path.join(Root,'YOLO'),help='Specify the directory to output PPOCR format')
    parser.add_argument('--classes',type=str,default=r'E:\OCRSceneImage\Trk\labelme\labels.txt',help='Directory of predefined label txt')
    parser.add_argument('--image',type=str,nargs="?",default=r'E:\OCRSceneImage\Trk',help='If image is not none, an image set will be generated in the output directory.')
    opt = parser.parse_args()
    print(opt)
    return opt

def process_directory(input_dir, yoloOutputDir,ppocrOutputDir, class_mapping,image):
    if not os.path.exists(yoloOutputDir):
        os.makedirs(yoloOutputDir)
    if not os.path.exists(ppocrOutputDir):
        os.makedirs(ppocrOutputDir)
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    for json_file in tqdm(json_files,desc='Converting...Wait'):
       
        convert_labelme(json_file, yoloOutputDir,ppocrOutputDir,class_mapping,image)
        
def convert_labelme(json_file,yoloOutputDir,ppoctTxt,class_mapping,image):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    yolo_annotations = []
    image_height = data['imageHeight']
    image_width = data['imageWidth']
    for shape in data['shapes']:
        label = shape['label']
        if label not in class_mapping:
            continue
        if label=='text':
            #
            pass
        points = shape['points']
        if shape['shape_type'] == 'polygon':
            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            xmin = min(x_coords)
            xmax = max(x_coords)
            ymin = min(y_coords)
            ymax = max(y_coords)
        elif shape['shape_type'] == 'rectangle':
            (xmin, ymin), (xmax, ymax) = points
        else:
            continue
        #convert to YOLO format
        x_center = (xmin + xmax) / 2.0 / image_width
        y_center = (ymin + ymax) / 2.0 / image_height
        width = (xmax - xmin) / image_width
        height = (ymax - ymin) / image_height
        class_id = class_mapping[label]
        yolo_annotations.append(f"{class_id} {x_center} {y_center} {width} {height}")
        #convert to PPOCRformat
        
    #output YOLO format
    output_yoloLabel = os.path.join(yoloOutputDir,'labels', os.path.splitext(os.path.basename(json_file))[0] + ".txt")
    if(os.path.exists(os.path.dirname(output_yoloLabel))==False):
        os.makedirs(os.path.dirname(output_yoloLabel))
    with open(output_yoloLabel, 'w') as f:
        f.write("\n".join(yolo_annotations))
    if image is not None:
        # If image is not none, an image set will be generated in the output directory.
        image_name=os.path.basename(data['imagePath'])
        output_image= os.path.join(yoloOutputDir,'images')
        src_path=os.path.join(image,image_name)
        output_path=os.path.join(output_image,image_name)
        if os.path.exists(output_image)==False:
            os.makedirs(output_image)
        shutil.copy(src_path,output_path)
        
def convert_labelme_to_ppocr(json_file, output_dir):
    print('mock convert')

def classMapping(classes):
    """Convert txt files to categorized dictionaries

    Args:
        classes (str): predefine_labels.txt

    Returns:
        dict: categorized dictionaries
    """
    class_dict=dict()
    with open(classes,mode='r') as c:
        for index, line in enumerate(c):
            class_dict[line.strip()] = index
    return class_dict
def convert(opt):
    """Labelme json format annotation file conversion to txt
    """
    input_dir=opt.labelmeJson
    yoloOutputDir=opt.yoloOutputDir
    ppocrOutputDir=opt.ppocrOutputDir
    classes =opt.classes
    image=opt.image
    #New labels dictionary
    class_mapping=classMapping(classes)
    process_directory(input_dir,yoloOutputDir,ppocrOutputDir,class_mapping,image)
    


def main():
    opt = parser()
    convert(opt)

if __name__=='__main__':
    Root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(Root)
    main()