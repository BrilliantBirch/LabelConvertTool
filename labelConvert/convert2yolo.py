"""
    Description:Labelme json format annotation file conversion to txt (for YOLO and PPOCR)
                Labelme json file needs to add text recognition in the description field
                It will output the annotation folder in YOLO format and the annotation folder in PPOCR format
                (with pictures and text cropped images for PPOCR text recognition) in the specified directory.
                
                Currently only polygonal and rectangular boxes are supported.
    Author:BrilliantBirtch(白彬楠)
    Date:2024/7/29
    E-mail:xiaobai3924@gmail.com
"""
import json
import os
import argparse
import cv2
import glob
import threading 
import shutil
from tqdm import tqdm

def process_directory(input_dir, yoloOutputDir,ppocrOutputDir,class_mapping,image):
    if not os.path.exists(yoloOutputDir):
        os.makedirs(yoloOutputDir)
    if not os.path.exists(ppocrOutputDir):
        os.makedirs(ppocrOutputDir)
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    for json_file in tqdm(json_files,desc='Converting...Wait'):
        convert_labelme(json_file, yoloOutputDir,ppocrOutputDir,class_mapping,image)
        
def convert_labelme(json_file,yoloOutputDir,ppocrOutputDir,class_mapping,image):
    """Single json file conversion

    Args:
        json_file (str): labelme format annotation file
        yoloOutputDir (str): the directory yolo format annotation
        class_mapping (str): the directory ppocr format annotation
        image (str): the origin image folder
    """
    os.makedirs(ppocrOutputDir,exist_ok=True)
    os.makedirs(os.path.join(yoloOutputDir,'labels'),exist_ok=True)
    os.makedirs(os.path.join(yoloOutputDir,'images'),exist_ok=True)
    with open(json_file, 'r',encoding='utf-8') as f:
        data = json.load(f)
    yolo_annotations = []
    ppocr_annotations=[]    
    image_height = data['imageHeight']
    image_width = data['imageWidth']
    for shape in data['shapes']:
        label = shape['label']
        if label not in class_mapping:
            continue
        points = shape['points']
        if shape['shape_type'] == 'polygon':
            #convert to YOLO format
            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            xmin = min(x_coords)
            xmax = max(x_coords)
            ymin = min(y_coords)
            ymax = max(y_coords)
            #convert to PPOCR format
            ppocrPoints = [(round(x), round(y)) for x, y in points]
        elif shape['shape_type'] == 'rectangle':
            #convert to YOLO format
            (xmin, ymin), (xmax, ymax) = points
            #convert to PPOCR format
            x_coords = [p[0] for p in points]
            y_coords = [p[1] for p in points]
            left = round(min(x_coords))
            right = round(max(x_coords))
            top = round(min(y_coords))
            bottom = round(max(y_coords))
            p1=[left,top]
            p2=[right,top]
            p3=[right,bottom]
            p4=[left,bottom]
            ppocrPoints=[p1,p2,p3,p4]
        else:
            continue
         #ppocr format
        if label == 'Text':
            text=shape['description']
            if text is None:
                continue
            text = text.strip()
            ppocr_data = {
                "transcription":text,
                "points":ppocrPoints,
                "difficult":False
            }
            ppocr_annotations.append(ppocr_data)
            continue
        #yolo bbox format
        x_center = (xmin + xmax) / 2.0 / image_width
        y_center = (ymin + ymax) / 2.0 / image_height
        width = (xmax - xmin) / image_width
        height = (ymax - ymin) / image_height
        class_id = class_mapping[label]
        yolo_annotations.append(f"{class_id} {x_center} {y_center} {width} {height}")
       
    
    image_name=os.path.basename(data['imagePath'])
    src_path=os.path.join(image,image_name)
    #export PPOCR image set
    ppocrImageFile=os.path.join(ppocrOutputDir,image_name)
    shutil.copy(src_path,ppocrImageFile)
    #output PPOCR format
    fileState=os.path.join(ppocrOutputDir,'fileState.txt')
    Label = os.path.join(ppocrOutputDir,'Label.txt')
    folder_name = os.path.basename(ppocrOutputDir)
    if ppocr_annotations.__len__()!=0:
        ppocr_annotations=json.dumps(ppocr_annotations,ensure_ascii=False)
        with open(Label,'a',encoding='utf-8') as l:
            l.write(f'{folder_name}/{image_name}\t{ppocr_annotations}\n')
        with open(fileState,'a',encoding='utf-8') as fs:
            fs.write(f'{ppocrImageFile}\t1\n')
    #export YOLO image set
    yoloImageSet= os.path.join(yoloOutputDir,'images')
    yoloImageFile=os.path.join(yoloImageSet,image_name)
    shutil.copy(src_path,yoloImageFile)
    #output YOLO format
    output_yoloLabel = os.path.join(yoloOutputDir,'labels', os.path.splitext(os.path.basename(json_file))[0] + ".txt")
    with open(os.path.join(yoloOutputDir,'labels', 'classes.txt'),'w',encoding='utf-8') as c:
        for class_key,_ in class_mapping.items():
            c.write(f'{class_key}\n')
    with open(output_yoloLabel, 'w',encoding='utf-8') as f:
        f.write("\n".join(yolo_annotations))
    
    
    
    
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
    
def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--labelmeJson',type=str,default=r'D:\data\Detect\TrkAnnotation\labelme',help='Directory of Labelme json format labeled files')
    parser.add_argument('--yoloOutputDir',type=str,default=r'D:\data\Detect\OCR_YOLODataset806',help='Specify the directory to output YOLO format')
    parser.add_argument('--ppocrOutputDir',type=str,default=r'D:\data\Detect\OCR_PPOCRDataset806',help='Specify the directory to output PPOCR format')
    parser.add_argument('--classes',type=str,default=r'D:\labelme\labels.txt',help='Directory of predefined label txt')
    parser.add_argument('--image',type=str,default=r'D:\data\Detect\TrkContainDetect',help='Directory of the labeled image')
    opt = parser.parse_args()
    print(opt)
    return opt

def main():
    opt = parser()
    convert(opt)

if __name__=='__main__':
    Root = os.path.dirname(os.path.abspath(__file__))
    # Convert disk letters to uppercase
    if os.name == 'nt':  # only Windows 
        if Root[1:3] == ':\\':  # check if disk path
            Root = Root[0].upper() + Root[1:]
    os.chdir(Root)
    main()