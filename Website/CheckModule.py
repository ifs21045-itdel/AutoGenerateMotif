import cv2
class Check:
    def __init__(self, fullpath, jmlBaris):
        self.fullpath = fullpath
        self.jmlBaris = jmlBaris
    
    def checkformat(self):
        
        image_format = self.fullpath[-3:]
        if(image_format == 'jpg'):
            return '1'
        else:
            return '0'
    
    def checkrow(self):

        jmlBaris = int(self.jmlBaris)
        if(1< jmlBaris <= 40):
            return "1"
        else:
            return "0"
    
    def checkSpecImage1(self):

        img = cv2.imread(str(self.fullpath),1)
        height, width, channels = img.shape

        if(6<= height <=12):
            return "1", height
        else:
            return "0", height

    def checkSpecImage2(self):
        
        img = cv2.imread(str(self.fullpath),1)
        height, width, channels = img.shape

        if(2<= width <= 140):
            return "1", width
        else:
            return "0", width
