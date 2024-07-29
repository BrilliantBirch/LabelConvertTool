"""
Author:BrilliantBirch
Description：清洗数据，将数据集中黑图和重复图片去除
            黑图判断方法是将图片以灰度图读取，然后判断非0像素是否小于阈值，阈值可通过实际调整
            重复值判断以计算哈希的方式和特征提取的方式，默认哈希的方式。
            Clean the data, remove the black images and duplicate images from the data set.
            The black image judgment method is to read the image in grayscale, and then determine whether the non-zero pixels are less than the threshold, the threshold can be adjusted by the actual adjustment
            Duplicate value judgment in the way of calculating hash and feature extraction, the default hash way.
Date:2024/7/19

"""
import os
import cv2
import hashlib
import shutil
import argparse
import random
from tqdm import tqdm

def is_black_image(image, threshold=10000):
    # 检查图像是否是全黑
    #Check if the image is all black
    return cv2.countNonZero(image) < threshold
#计算哈希值的方法
def get_image_hash(image_path):
    # 计算图像的哈希值
    #Calculate the hash value of the image
    hasher = hashlib.md5()
    with open(image_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()
#特征匹配的方法
#Feature matching methods
def get_sift_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    return descriptors

def are_images_similar(desc1, desc2, threshold=0.75):
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(desc1, desc2, k=2)
    good_matches = [m for m, n in matches if m.distance < threshold * n.distance]
    return len(good_matches) > 10

def remove_duplicates_and_black_images(opt):
    seen_hashes = set()
    blackcount = 0
    duplicatecount =0
    directory = opt.ImageFolder
    if directory=='':
        print('the following arguments are required: --ImageFolder')
    blackPath = opt.blackPath
    duplicatePath = opt.duplicatePath
    if blackPath=='':
        blackPath=os.path.join(os.path.dirname(directory),'black')
    if duplicatePath=='':
        duplicatePath=os.path.join(os.path.dirname(directory),'duplicate')
    if(os.path.exists(blackPath)==False):
        os.makedirs(blackPath)
    if(os.path.exists(duplicatePath)==False):
        os.makedirs(duplicatePath)
    image_descriptors=[]
    for root, _, files in os.walk(directory):
        for file in tqdm(files,desc='清洗图片中'):
            file_path = os.path.join(root, file)
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                # 以灰度图读取图像
                # Reading images in grayscale
                image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
                if image is None:
                    continue
                # 检查是否是黑图
                if is_black_image(image):
                    # print(f'Removing black image: {file_path}')
                    # os.remove(file_path)
                    dest = os.path.join(blackPath,file)
                    shutil.move(file_path,dest)
                    blackcount+=1
                    continue
                if opt.duplicateMethod=='hash':
                    # 计算图像的哈希值
                    image_hash = get_image_hash(file_path)
                    if image_hash in seen_hashes:
                    # print(f'Removing duplicate image: {file_path}')
                    # os.move(file_path)
                        dest =os.path.join(duplicatePath,file)
                        shutil.move(file_path,dest)
                        duplicatecount+=1
                    else:
                        seen_hashes.add(image_hash)
                
                elif opt.duplicateMethod=='feature':
                    descriptors = get_sift_features(image)
                    if descriptors is None:
                        continue
                    is_duplicate = False
                    for stored_desc in image_descriptors:
                        if are_images_similar(descriptors, stored_desc):
                            print(f'Removing duplicate image: {file_path}')
                            os.remove(file_path)
                            is_duplicate = True
                            break
                    if not is_duplicate:
                        image_descriptors.append(descriptors)
    print(f'删除黑图{blackcount}张，删除重复图片{duplicatecount}张')

def random_selectData(src_dir,dest_dir,num):
    """随机挑选指定张图片到指定目录
       Randomly selects a specified image to a specified directory

    Args:
        src_dir (str): 源目录
        det_dir (str): 指定目录
        num (str): 指定数量
    """
    if not os.path.exists(src_dir):
        raise ValueError(f"Source directory {src_dir} does not exist.")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # 获取源目录中的所有文件
    all_files = os.listdir(src_dir)

    # 过滤出所有的图片文件（可以根据实际情况调整扩展名）
    image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    # 检查是否有足够的图片文件
    if len(image_files) < num:
        raise ValueError(f"Not enough images in {src_dir} to select {num} images.")
    # 随机选择指定数目的图片
    selected_images = random.sample(image_files, num)

    # 复制选择的图片到目标目录
    for image in tqdm(selected_images,desc='随机挑选图片中'):
        src_path = os.path.join(src_dir, image)
        dest_path = os.path.join(dest_dir, image)
        shutil.copy(src_path, dest_path)

def main(opt):
    remove_duplicates_and_black_images(opt)
    if(opt.dataNum!=0):
        random_selectData(opt.ImageFolder,opt.selectedFolder,opt.dataNum)
    
if __name__ == '__main__':
    Root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(Root)
    parser = argparse.ArgumentParser()
    parser.add_argument('--ImageFolder',type=str,default=r'E:\data\OCR\6-29.30Con',help='图像的原始目录')
    parser.add_argument('--blackPath',type=str,default='',help='去除的黑图存放地址')
    parser.add_argument('--duplicatePath',type=str,default='',help='去除的重复图存放地址')
    parser.add_argument('--duplicateMethod',type=str,default='hash',help='去除重复图的方法')
    parser.add_argument('--dataNum',type=int,default=2000,help='随机挑选多少条数据，默认0为全选')
    parser.add_argument('--selectedFolder',type=str,default=os.path.join(Root,'selectedCon'),help='若启用随机挑选，指定挑选后的图片指定目录')
    opt = parser.parse_args()
    #打印参数
    print(opt)
    main(opt)
    
    
