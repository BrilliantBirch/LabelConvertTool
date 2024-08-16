"""
    Description:Split the dataset, default is 6:2:2 distribution train set: val set: test set
    Author:BrilliantBirch(白彬楠)
    Date:2024/8/2
    E-mail:xiaobai3924@gmail.com
    Website:brilliantbirch-bbn.com
"""
import os
import yaml
import shutil
import argparse
from sklearn.model_selection import train_test_split
from tqdm import tqdm

def outputyaml(classes,output):
    
    yaml_content = {
        'path': os.path.abspath(output),  # dataset root dir
        'train': r'train/images',
        'val': r'val/images',
        'nc': len(classes),
        'names': classes
    }
    with open(os.path.join(output,'dataset.yaml'), 'w') as file:
        yaml.dump(yaml_content, file, default_flow_style=False,sort_keys=False)
        
def readlabels(dataRoot):
    img_dir = os.path.join(dataRoot, 'images')
    label_dir = os.path.join(dataRoot, 'labels')
    # 获取所有图片和标注文件
    image_files = [os.path.join(img_dir,f) for f in os.listdir(img_dir) if f.endswith('.jpg') or f.endswith('.png')]
    label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt') and f!='classes.txt']

    image_names = set(os.path.splitext(os.path.basename(i))[0] for i in image_files)
    label_names = set(os.path.splitext(l)[0] for l in label_files)

    # 找出不匹配的文件
    missing_labels = image_names - label_names
    missing_images = label_names - image_names

    # 打印结果
    if missing_labels:
        print("Images with missing labels:", missing_labels)
    if missing_images:
        print("Labels with missing images:", missing_images)
    # 确保图片和标注文件一一对应
    assert image_names == label_names, "Mismatch between image files and label files"
    images = list(image_files)
    return images

def move_files(filelist,splitname,output):
    for file_name in tqdm(filelist,f'分割{splitname}中：'):
        img_src = file_name
        lbl_src=os.path.splitext(file_name)[0]+'.txt'
        lbl_src=lbl_src.replace('\\images','\\labels')
        file_name=os.path.basename(file_name)
        img_dst = os.path.join(output,splitname, 'images', file_name)
        lbl_name=os.path.basename(lbl_src)
        lbl_dst = os.path.join(output,splitname, 'labels', lbl_name)
        shutil.copy(img_src, img_dst)
        shutil.copy(lbl_src, lbl_dst)

def splitData(images,output):
    # 计算训练集、验证集和测试集的样本数量
    split_ratios = {'train': 0.8, 'val': 0.19, 'test': 0.01}
    num_images = len(images)
    num_train = int(num_images * split_ratios['train'])
    num_val = int(num_images * split_ratios['val'])
    num_test = num_images - num_train - num_val  # 确保所有图片都被分配

    # 分割数据集
    train_images, rest_images = train_test_split(images, test_size=num_val + num_test)
    val_images, test_images = train_test_split(rest_images, test_size=num_test)
    # return train_images,val_images,test_images
    # 创建分割数据集的目录
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(output, split, 'images'), exist_ok=True)
        os.makedirs(os.path.join(output, split, 'labels'), exist_ok=True)
    move_files(train_images, 'train',output)
    move_files(val_images, 'val',output)
    move_files(test_images, 'test',output)

def readclassesTxt(classesTxt):
    with open(classesTxt, 'r',encoding='utf-8') as file:
        classes = [line.strip() for line in file.readlines()]
    names_dict = {i: name for i, name in enumerate(classes)}
    return names_dict

def parsers():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',type=str,default=r'E:\OCRSceneImage\TEST',help='yolo数据根目录')
    parser.add_argument('--output',type=str,default=r'E:\OCRSceneImage\TEST\split',help='数据集分割导出目录')
    parser.add_argument('--classesTxt',type=str,default=r'E:\OCRSceneImage\TEST\labels\classes.txt',help='classes.txt路径')
    parser.add_argument('--yaml',action='store_true',help='是否导出dataset.yaml')
    opt=parser.parse_args()
    return opt


def main():
    opt=parsers()
    images =readlabels(opt.data)
    
    splitData(images,opt.output)
    
    if opt.yaml:
        classes=readclassesTxt(opt.classesTxt)
        outputyaml(classes,opt.output)
    
if __name__=='__main__':
    main()
    pass