"""
Desciption:合作标注时随机平均分配给指定人数
Author：BrilliantBirch(白彬楠)
Date:2024/7/31
E-mail:xiaobai3924@gmail.com
"""

import os
import random
import shutil

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
        
        for file_name in part_files:
            source_path = os.path.join(source_dir, file_name)
            target_path = os.path.join(target_dir, file_name)
            shutil.move(source_path, target_path)
        
        start = end

def main():
    source_directory = r''  # 替换为你的源文件夹路径
    target_base_directory = r''  # 替换为你的目标基础文件夹路径
    number_of_parts = 3  # 替换为你想要分成的份数
    split_and_store_images(source_directory, target_base_directory, number_of_parts)

if __name__=='__main__':
    Root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(Root)
    main()