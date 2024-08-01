"""
Description:labelme标注文件的json格式
Author：BrilliantBirch(白彬楠)
Date:2024/7/31
E-mail:xiaobai3924@gmail.com
"""
class labelmeJson():
    def __init__(self,version):
        self.version=version
        self.flags={}
        self.shapes=[]
        self.imagePath=""
        self.imageData=None
        self.imageHeight=1080
        self.imageWidth=1920
    def to_dict(self):
        return{
            'version':self.version,
            'flags':self.flags,
            'shapes':self.shapes,
            'imagePath':self.imagePath,
            'imageData':self.imageData,
            'imageHeight':self.imageHeight,
            'imageWidth':self.imageWidth
        }