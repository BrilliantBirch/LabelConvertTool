帮助清洗数据集中的不可用图片，提供Labelme标注的json文件与PaddleOCR所需标注格式和YOLO所需txt标注格式之间的互相转换
# 示例 
## 清洗数据集  
* 去除数据集中的黑图和重复图片并可抽取指定数量的图片组成新的图片集
  ```
  cd data
  python washData.py --ImageFolder {你待清洗的图片所在目录}
  ```
  将在图片统计目录新建一个black文件夹存放筛出的黑图和一个duplicate文件夹存放筛选的重复图片  
  支持以哈希值和特征匹配的方式来判断是否重复  
  ```
  python washData.py --ImageFolder  {待清洗的图片所在目录} --duplicateMethod {hash或者feature}
  ```
## labelme格式转换为yolo和ppocr所需格式  
将labelme标注的json格式转换为yolo和ppocr数据集所需的格式，转换后可直接进行训练  
若要转换到ppocr格式的数据集 使用labelme标注时应按以下步骤标注文本  
1. label类别新增一个Text  
2. 在description属性写入文本内容  

```
cd labelConvert
python convert2yolo.py --labelmeJson {labelme格式的json文件目录} --classes '{预定义的标签类别}' --image '{原图片存放路径}'                                    
``` 
执行脚本后 将在labelConvert文件夹生成PPOCR和YOLO文件夹，分别是转换后的PPOCR和YOLO数据集  
若需指定生成脚本参考  
```
python convert2yolo.py -h
```


