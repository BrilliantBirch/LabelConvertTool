"""
Description:从目标文件夹中消除另一个文件夹中已有的文件
Author：BrillliantBirch
Date:2024/8/19
E-mail:xiaobai3924@gmal.com
"""
import os
import shutil
from tqdm import tqdm

tragetFolder=r'E:\tempData\629'
reference_folder=r'E:\OCRSceneImage\TrainData\YOLO\images'

def remove_matching_files(target_folder, reference_folder):
    # 遍历参考文件夹中的所有文件
    removeList=[]
    for root, dir, files in os.walk(reference_folder):
        for file in tqdm(files,desc='清除中：'):
            # 获取参考文件的完整路径
            reference_file_path = os.path.join(root, file)
            
            # 构建目标文件夹中的对应文件路径
            relative_path = os.path.relpath(reference_file_path, reference_folder)
            target_file_path = os.path.join(target_folder,relative_path)
            
            # 如果目标文件夹中存在相同的文件，则删除它
            if os.path.exists(target_file_path):
                os.remove(target_file_path)
                removeList.append(os.path.basename(target_file_path))
    for file in removeList:
        print(f'{file}\n')        
    print(f'共去除{len(removeList)}个文件')
    
remove_matching_files(tragetFolder, reference_folder)