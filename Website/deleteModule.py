import os
import shutil

class Delete:
    def __init__(self, fullpath):
        self.fullpath = fullpath
    
    def DeleteMotif(self):
       
        image_fullpath = self.fullpath[1:]
        format = image_fullpath[-3:]

        if(format == "jpg"):
            if os.path.exists(image_fullpath):
                os.remove(image_fullpath)
                shutil.rmtree(f"{image_fullpath[:-4]}_grid")
                os.remove(f"{image_fullpath[:-4]}_grid.jpg")
                os.remove(f"{image_fullpath[:-4]}_grid_help.jpg")
                return "Remove"
            else:
                return "The file does not exist"
        else:
            if os.path.exists(image_fullpath):
                os.remove(image_fullpath)
                shutil.rmtree(f"{image_fullpath[:-4]}_grid_red")
                os.remove(f"{image_fullpath[:-4]}_grid.png")
                os.remove(f"{image_fullpath[:-4]}_grid_red.jpg")
                os.remove(f"{image_fullpath[:-4]}.zip")
                return "Remove"
            else:
                return "The file does not exist"