"""
Description：筛选标签-将需要用于训练的标签筛选出来成为新的训练集，并生成Dataset yaml文件
！！！注意！！！：新标签会直接覆盖，请备份原标签
Author:BrilliantBirch(白彬楠)
Date:2024/8/9
E-mail:xiaobai3924@gmail.com
Website:brilliantbirch-bbn.com
"""

import os
import sys
import argparse
from tqdm import tqdm
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.fileutility import *


def filter_labels(label_file, classes_to_keep):

    classes_id={}
    for index,classes_set in enumerate(classes_to_keep):
        #对标签索引重新排序（按筛选后的标签）
        classes_id[classes_set[1]]=index
    if os.path.basename(label_file)=='classes.txt':
        with open(label_file, 'w') as file:
            labels = [label for label,_ in classes_to_keep]
            for label in labels:
                file.write(f'{label}\n')
        return
    with open(label_file, 'r',encoding='utf-8') as file:
        lines = file.readlines()
    
    
    with open(label_file, 'w',encoding='utf-8') as file:
        for line in lines:
            label_id = int(line.split()[0])
            if label_id in classes_id.keys():
                label=classes_id[label_id]
                line=f'{label}'+line[1:]
                file.write(line) 
                
def process_directory(directory, classes_to_keep_dic):
    for filename in tqdm(os.listdir(directory),'处理中'):
        if filename.endswith('.txt'):
            filter_labels(os.path.join(directory, filename), classes_to_keep_dic)

def convertTxt2ID(predefinedTxt,classes_to_keep):
    classes_txt=classMapping(predefinedTxt)
    classes_id={}
    for cls in classes_to_keep:
        classes_id[cls]=classes_txt[cls]
    classes_to_keep = sorted(classes_id.items(), key=lambda item: item[1])
    return classes_to_keep
        

   
                
def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--labels',type=str,default=r'D:\data\Detect\OCR_YOLODatasetCheck\labels',help='label文件路径')  
    parser.add_argument('--classes_to_keep',nargs='+',default={'Trk', 'TrkHead_Normal','Container_Normal'},help='需要筛选的标签名')

    opt=parser.parse_args()
    return opt
def main():
    opt=parser()
    predefinedTxt=os.path.join(opt.labels,'classes.txt')
    classes_to_keep=convertTxt2ID(predefinedTxt,opt.classes_to_keep)
    process_directory(opt.labels, classes_to_keep)
    

if __name__=='__main__':
    main()
   