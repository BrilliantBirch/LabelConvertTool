"""
    Description:Split the dataset, default is 6:2:2 distribution train set: val set: test set
    Author:BrilliantBirch(白彬楠)
    Date:2024/8/2
    E-mail:xiaobai3924@gmail.com
"""
import os
import shutil
from sklearn.model_selection import train_test_split
from collections import defaultdict

# 设置目录路径
data_dir = r'D:\data\Detect\coco128'
output_dir = 'output'
img_dir = os.path.join(data_dir, 'images')
label_dir = os.path.join(data_dir, 'labels')

# 获取所有图片和标注文件
image_files = [f for f in os.listdir(img_dir) if f.endswith('.jpg') or f.endswith('.png')]
label_files = [f for f in os.listdir(label_dir) if f.endswith('.txt')]

# 确保图片和标注文件一一对应
assert sorted([os.path.splitext(i)[0] for i in image_files]) == sorted([os.path.splitext(l)[0] for l in label_files])

# 读取标注文件并统计类别数量
# class_counts = defaultdict(int)
# image_to_labels = defaultdict(set)

# for label_file in label_files:
#     img_file = label_file.replace('.txt', '.jpg')
#     with open(os.path.join(label_dir, label_file), 'r') as f:
#         for line in f:
#             class_id = int(line.split()[0])
#             class_counts[class_id] += 1
#             image_to_labels[img_file].add(class_id)

# 统计每张图片的类别
images = list(image_files)

# 计算训练集、验证集和测试集的样本数量
split_ratios = {'train': 0.6, 'val': 0.2, 'test': 0.2}
num_images = len(images)
num_train = int(num_images * split_ratios['train'])
num_val = int(num_images * split_ratios['val'])
num_test = num_images - num_train - num_val  # 确保所有图片都被分配

# 分割数据集
train_images, rest_images = train_test_split(images, test_size=num_val + num_test)
val_images, test_images = train_test_split(rest_images, test_size=num_test)

# 创建分割数据集的目录
for split in ['train', 'val', 'test']:
    os.makedirs(os.path.join(output_dir, split, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, split, 'labels'), exist_ok=True)

def move_files(file_list, split_name):
    for file_name in file_list:
        img_src = os.path.join(img_dir, file_name)
        lbl_src = os.path.join(label_dir, file_name.replace('.jpg', '.txt'))
        img_dst = os.path.join(output_dir, split_name, 'images', file_name)
        lbl_dst = os.path.join(output_dir, split_name, 'labels', file_name.replace('.jpg', '.txt'))
        shutil.copy(img_src, img_dst)
        shutil.copy(lbl_src, lbl_dst)

# 复制文件到对应目录
move_files(train_images, 'train')
move_files(val_images, 'val')
move_files(test_images, 'test')

print("数据集分割完成")
