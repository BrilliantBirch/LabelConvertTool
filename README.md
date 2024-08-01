[简体中文](ReadMe_ch.md)|English  
E-mail: xiaobai3924@gmail.com
Data set cleaning and label conversion tools  
1. help clean the unusable images in the dataset (black images and duplicate images are eliminated)  
2. provide Labelmejson file to PPOCR text detection dataset and YOLO dataset labeling format conversion between each other  

# Example 
## Cleaning a dataset  
* Removes black and duplicate images from the dataset and extracts a specified number of images.
  ```
  cd data
  python washData.py --ImageFolder {directory of the images you want to wash}
  ```
  Will create a new black folder in the image statistics directory to hold the screened black images and a duplicate folder to hold the screened duplicates.  
  Supports hash and feature matching to determine duplicates.  
  ```
  python washData.py --ImageFolder {directory of images to be washed} --duplicateMethod {hash or feature}
  ```
## labelme format converted to the format required by yolo and ppocr  
Convert labelme labeled json format to the format required by yolo and ppocr dataset, after conversion, you can directly carry out the training  
If you want to convert to ppocr format dataset, you should follow the steps below to label the text when using labelme annotation (you don't need this step if you don't need to convert to PPOCR dataset).  
1. label category add a Text  
2. in the description attribute to write text content  
**tips** script execution is completed in the specified directory will generate label.txt and filestate.txt as well as images, can be imported directly into the directory in the PPOCRLabel, the use of recognition results, you can generate text recognition training set.  
```
cd labelConvert
python convert2yolo.py --labelmeJson {directory of labelme-formatted json files} --classes '{predefined categories of labels}' --image '{path to original image storage}'                                    
``` 
After executing the script, the PPOCR and YOLO folders will be generated in the labelConvert folder, which are the converted PPOCR and YOLO datasets respectively.  
If you need to specify the generation script reference  
```
python convert2yolo.py -h #View help
```
## yolo and ppocr format conversion to labelme json format
```
cd labelConvert
python convert2yolo.py -h #View help

--yoloConvert #Converts from yolo format only.
--ppocrConvert #Convert from ppocr only.
--version #Version of labelme
--yoloLabels #Directory for yolo labels.
--imageFolder #Directory for images (must be specified for yolo conversion)
--predefinedClass #predefined class of the label (must be specified for yolo conversion)
--outputdir #Output directory for labelme json annotation files.
--ppocrLabels #Directory where PPOCR annotation files are stored.
```
