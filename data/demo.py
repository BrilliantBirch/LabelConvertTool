import os
import shutil
import sys
from tqdm import tqdm


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from common.fileutility import *

imageFolder=r'D:\data\Detect\TrkContainDetect'
trainData_target=r'D:\data\Detect\done\xuhaiyan'
labelFolder=r'D:\data\Detect\done\xuhaiyan\labelme'

os.makedirs(trainData_target,exist_ok=True)
count=0
f_name=[]
for f in tqdm(os.listdir(labelFolder),'读取标注文件中'):
    if not f.endswith('.json'): 
        continue
    filename=os.path.splitext(f)[0]
    filename=find_file(imageFolder,filename)
    if filename is None:
        count+=1
        f_name.append(f)
        continue
    source = os.path.join(imageFolder,filename)
    shutil.copy(source,os.path.join(trainData_target,filename))
if count != 0:
    print(f'有{count}条数据未找到:{f_name}')