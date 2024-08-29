"""根据图片获取labelme json文件
"""
import os
import shutil
from tqdm import tqdm
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.fileutility import *

labelsFolder=r'E:\OCRSceneImage\prelabel\labelme'
imagesFolder=r'E:\OCRSceneImage\12fragments'
targetFolder=r'E:\OCRSceneImage\labels'
missMatchFiles=[]

for root,_,files in os.walk(imagesFolder):
    for file in tqdm(files,desc=f'读取{os.path.basename(root)}目录中:'):
        # labelFolder=os.path.join(root,'labelme')
        # os.makedirs(labelFolder,exist_ok=True)
        filename=os.path.splitext(file)[0]
        labelname=find_file(labelsFolder,filename)
        if labelname is not None:
            source=os.path.join(labelsFolder,labelname)
            curTargetFolder=os.path.join(targetFolder,os.path.basename(root))
            os.makedirs(curTargetFolder,exist_ok=True)
            dst=os.path.join(curTargetFolder,labelname)
            shutil.copy2(source,dst)
        else:
            missMatchFiles.append(filename)
        
print(f'有{len(missMatchFiles)}条数据缺失')