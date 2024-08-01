"""
Description:YOLO and PPOCR format convert to Labelme format
Author:BrilliantBirch(白彬楠)
Date:2024/7/31
E-mail:xiaobai3924@gmail.com
"""
import os
import json
import shutil
import argparse
import sys
from tqdm import tqdm

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.jsonformat import labelmeJson

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
            class_dict[index] = line.strip()
    return class_dict

#.读取YOLO格式的标注文件
def readyolo(yolofile,class_dict):
    annotations=[]
    with open(yolofile,'r',encoding='utf-8') as y:
        for line in y:
            parts = line.strip().split()
            if len(parts) != 5:
                continue  # 忽略不符合格式的行
            
            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            
            # 计算点坐标 (左上角和右下角)
            x_center *= 1920.0  # 假设图像宽度是 1.0 的归一化值
            y_center *= 1080.0  # 假设图像高度是 1.0 的归一化值
            width *= 1920.0
            height *= 1080.0
            
            x_min = x_center - width / 2
            x_max = x_center + width / 2
            y_min = y_center - height / 2
            y_max = y_center + height / 2
            
            points = [
                [x_min, y_min],
                [x_max, y_max],
            ]
            if class_dict[class_id]=='Text':
                continue
            
            annotations.append({
                'class': class_dict[class_id],
                'points': points,
                'shape_type':'rectangle',
                'description':''
            })
    filename=os.path.basename(yolofile)
    return filename,annotations
        

def serialize(obj):
    if isinstance(obj, labelmeJson):
        return obj.to_dict()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def find_file(directory, target_filename):
    """Find target file

    Args:
        directory (str): directory to be found
        target_filename (_type_): target file


    Returns:
        str: Returns the name of the file in the directory if there is one, or None if there isn't.
    """
    with os.scandir(directory) as it:
        for entry in it:
            if entry.is_file() and os.path.splitext(entry.name)[0] == os.path.splitext(target_filename)[0]:
                return entry.name
    return None

def outputLabelmeFormat(annotations,**kwargs):
    """Output labelme's json annotation file to the specified directory.

    Args:
        outputdir (str): 标注文件的指定输出目录
        filename (str): 标注文件命名
        version (str): labelme版本号
        points (list): 标注框坐标
        description (str): 文本框识别内容
    """
    version=kwargs.get('version','5.4.1')
    filename=kwargs.get('filename','')
    outputdir=kwargs.get('outputdir','')
    labelme = labelmeJson(version=version)
    labelme.imagePath=f'..\\{filename}'
    jsonname=os.path.join(outputdir,os.path.splitext(filename)[0]+'.json')
    for annotation in annotations:
        label=annotation['class']
        points=annotation['points']
        shape_type=annotation['shape_type']
        description=annotation['description']
        data={
            'label':label,
            'points':points,
            'group_id':None,
            'description':description,
            'shape_type':shape_type,
            'flags':{},
            'mask':None
        }
        labelme.shapes.append(data)
    with open(jsonname,'w',encoding='utf-8') as f:
        json.dump(labelme,f,indent=2,ensure_ascii=False,default=serialize)
        


def yolosConvert(labelsPath,yoloFolder,originImageFolder,outputdir,version):
    for yolofile in tqdm(os.listdir(yoloFolder),'yolo格式转换labelme格式中'):
        yoloPath = os.path.join(yoloFolder,yolofile)
        yoloConvert(labelsPath,yoloPath,originImageFolder,outputdir,version)

def yoloConvert(labelsPath,yoloPath,originImageFolder,outputdir,version):
    """
    Conversion of a single yolo annotation file
    """
    class_id=classMapping(labelsPath)
    filename,annotations=readyolo(yoloPath,class_id)
    image_name=find_file(originImageFolder,filename)
    if  image_name is not None:
        outputLabelmeFormat(annotations,outputdir=outputdir,filename=image_name,version=version)
  
  
def ppocrConvert(ppocrPath,outputdir,version):
    """
        PPOCR convert to labelme
    """
    with open(ppocrPath,'r',encoding='utf-8') as p:
        for line in tqdm(p,"PPOCR格式转换中"):
            annotations=[]
            parts = line.strip().split('\t')
            if not parts.__len__() ==2:
                continue
            filename = os.path.basename(parts[0])
            for jsons in json.loads(parts[1]):
                annotations.append({
                    'class':'Text',
                    'points':jsons['points'],
                    'shape_type':'polygon',
                    'description':jsons['transcription']
                })
            outputLabelmeFormat(annotations,outputdir=outputdir,filename=filename,version=version)
def dict_append(mydict,key,value):
    if key in mydict:
        mydict[key][0].extend(value)
    else:
        mydict[key] = [value]

def convert(*args):
    """
        PPOCR and YOLO format convert to Labelme json format
    """
    ppocrLabels=args[0].ppocrLabels
    yoloLabels=args[0].yoloLabels
    predefinedClass=args[0].predefinedClass
    outputdir=args[0].outputdir
    version=args[0].version
    imageFolder=args[0].imageFolder
    
    annotations_dic=dict()
    class_id=classMapping(predefinedClass)
    # read yolo
    for yoloLabel in tqdm(os.listdir(yoloLabels),'正在读取yolo标注文件'):
        filename,annotations=readyolo(os.path.join(yoloLabels,yoloLabel),class_id)
        image_name=find_file(imageFolder,filename)
        if image_name is None:
            continue
        dict_append(annotations_dic,image_name,annotations)
    
    # read ppocr
    with open(ppocrLabels,'r',encoding='utf-8') as p:
        lines= p.readlines()
    for line in tqdm(lines,desc="读取PPOCR标注文件中",unit="行"):
        annotations=[]
        parts = line.strip().split('\t')
        if not parts.__len__() ==2:
            continue
        filename = os.path.basename(parts[0])
            
        for jsons in json.loads(parts[1]):
            annotations.append({
                'class':'Text',
                'points':jsons['points'],
                'shape_type':'polygon',
                'description':jsons['transcription']
            })
        dict_append(annotations_dic,filename,annotations)
        
    for filename,annotations in tqdm(annotations_dic.items(),'转换至Labelme json格式中'):
        annotations=annotations[0]
        outputLabelmeFormat(annotations,outputdir=outputdir,filename=filename,version=version)

def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--yoloConvert',action='store_true',help='only yolo convert to labelme')
    parser.add_argument('--ppocrConvert',action='store_true',help='only ppocr convert to labelme')
    parser.add_argument('--version',type=str,default='5.4.1',help='version of labelme')
    parser.add_argument('--yoloLabels',type=str,default=r'E:\LabelConvertTool\labelConvert\YOLO\labels',help='Directory of yolo to be converted')
    parser.add_argument('--imageFolder',type=str,default=r'E:\LabelConvertTool\labelConvert\YOLO\images',help='Image set')
    parser.add_argument('--predefinedClass',type=str,default=r'E:\OCRSceneImage\Trk\labelme\labels.txt',help='Predefined classes text files')
    parser.add_argument('--outputdir',type=str,default=r'',help='labelme json output dir')
    parser.add_argument('--ppocrLabels',type=str,default=r'E:\LabelConvertTool\labelConvert\PPOCR\Label.txt',help='Directory of ppocr to be converted')
    opt = parser.parse_args()
    print(opt)
    return opt

def main():
    opt = parser()
    if opt.yoloConvert and not opt.ppocrConvert:
        yolosConvert(opt.predefinedClass,opt.yoloLabels,opt.imageFolder,opt.outputdir,opt.version)
    elif opt.ppocrConvert and not opt.yoloConvert:
        ppocrConvert(opt.ppocrLabels,opt.outputdir,opt.version)
    else:
        convert(opt)
    
if __name__=='__main__':
    Root = os.path.dirname(__file__)
    os.chdir(Root)
    main()