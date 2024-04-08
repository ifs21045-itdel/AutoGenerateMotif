import uuid
from PIL import Image
import os

class Save:
    def __init__(self, fullpath, username):
        self.fullpath = fullpath
        self.username = username
    
    def SaveMotifAsal(self):
        
        image_fullpath = self.fullpath[1:]
        img = Image.open(str(image_fullpath))
        namaDirektori = "media/Hasil"
        Direktori = namaDirektori

        if(not os.path.exists(Direktori)):
            os.mkdir(Direktori)
        unique_file_name = uuid.uuid4().hex

        img = img.save(f"media/Hasil/{unique_file_name}.jpg")

        os.remove(image_fullpath)

        return f"/media/Hasil/{unique_file_name}.jpg"
    
    def SaveMotiHasil(self):
        
        image_fullpath = self.fullpath[1:]
        folderUser = self.username

        img = Image.open(str(image_fullpath))

        unique_file_name = uuid.uuid4().hex

        img = img.save(f"media/Hasil/{unique_file_name}.png")

        folder_path = (f"media/{folderUser}")
        test = os.listdir(folder_path)
        for images in test:
            if images.endswith(".png"):
                os.remove(os.path.join(folder_path, images))
        
        for images in test:
            if images.endswith(".jpg"):
                os.remove(os.path.join(folder_path, images))

        return f"/media/Hasil/{unique_file_name}.png"