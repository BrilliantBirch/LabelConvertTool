"""
Desciption:合作标注时随机平均分配给指定人数
Author：BrilliantBirch(白彬楠)
Date:2024/7/31
E-mail:xiaobai3924@gmail.com
"""

import os
import random
import shutil
import argparse
from tqdm import tqdm

def split_and_store_images(source_dir, target_base_dir, num_parts):
    # 获取所有图片文件的路径
    image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    # 随机打乱图片文件的顺序
    random.shuffle(image_files)
    
    # 计算每一份的大小
    part_size = len(image_files) // num_parts
    extra = len(image_files) % num_parts

    # 创建目标文件夹并分配图片文件
    start = 0
    for i in range(num_parts):
        end = start + part_size + (1 if i < extra else 0)
        part_files = image_files[start:end]
        
        target_dir = os.path.join(target_base_dir, f'part_{i+1}')
        os.makedirs(target_dir, exist_ok=True)
        
        for file_name in tqdm(part_files,f'第{i+1}份，共{num_parts}份'):
            source_path = os.path.join(source_dir, file_name)
            target_path = os.path.join(target_dir, file_name)
            shutil.move(source_path, target_path)
        
        start = end
def parser():
    parsers = argparse.ArgumentParser()
    parsers.add_argument('--source',type=str,default=r'E:\OCRSceneImage\prelabel',help='源文件夹路径')
    parsers.add_argument('--target',type=str,default=r'E:\OCRSceneImage\12fragments',help='目标文件夹路径')
    parsers.add_argument('--nums',type=int,default=12,help='要均分的人数')
    
    opt = parsers.parse_args()
    return opt
def main():
    opt=parser()
    
    split_and_store_images(opt.source, opt.target, opt.nums)

if __name__=='__main__':
    Root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(Root)
    main()