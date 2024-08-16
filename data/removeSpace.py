import os
from tqdm import tqdm

labelPath=r'D:\data\Detect\OCR_PPOCRDatasetCheck\rec_gt.txt'
with open(labelPath,'r',encoding='utf-8') as file:
    lines=file.readlines()
print(lines)
with open(r'D:\data\Detect\OCR_PPOCRDatasetCheck\rec_gt_train.txt','w',encoding='utf-8') as file:
    for line in tqdm(lines,'处理中'):
        path=line.split('\t')[0]
        rec=line.split('\t')[1]
        rec=rec.replace(' ','')
        rec=rec.upper()
        file.write(f'{path}\t{rec}')