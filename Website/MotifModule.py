import cv2
import os
from PIL import Image, ImageDraw
import numpy as np
class Motif:
    def __init__(self, fullpath):
        self.fullpath = fullpath
    
    def UrutanLidi(self):
        
        image_fullpath = self.fullpath[1:]

        image = cv2.imread(image_fullpath)

        h, w, c = image.shape

        temp = []
        for i in range(1, 1+h):
            temp.append(i)

        return f"{temp}"

    def GridLidi(self):
        image_fullpath = self.fullpath[1:]

        if os.path.exists(f"{image_fullpath[:-4]}_grid.jpg"):
            return f"{image_fullpath[:-4]}_grid.jpg"

        else:
            image = Image.open(image_fullpath)

            width, height, = image.size
            image = image.resize((width * 10, height * 10), Image.Resampling.NEAREST)

            draw = ImageDraw.Draw(image)

            width, height, = image.size

            grid_size = 10

            for x in range(0, width, grid_size):
                draw.line((x, 0, x, height), fill=(127, 127, 127))
            
            for y in range(0, height, grid_size):
                draw.line((0, y, width, y), fill=(127, 127, 127))

            image.save(f"{image_fullpath[:-4]}_grid.jpg")

            return f"{image_fullpath[:-4]}_grid.jpg"
    
    def GridMotif(self):
        image_fullpath = self.fullpath
        image_fullpath = image_fullpath[1:]
        

        if os.path.exists(f"{image_fullpath[:-4]}_grid.png"):
            return f"{image_fullpath[:-4]}_grid.png"
        
        else: 
            png_image = Image.open(image_fullpath)
            background = Image.new('RGB', png_image.size, (255, 255, 255))
            
            background.paste(png_image, mask=png_image.split()[3])
            
            image = background
            draw = ImageDraw.Draw(image)

            width, height = image.size

            grid_size = 10

            for x in range(0, width, grid_size):
                draw.line((x, 0, x, height), fill=(127, 127, 127))

            for y in range(0, height, grid_size):
                draw.line((0, y, width, y), fill=(127, 127, 127))

            image.save(f"{image_fullpath[:-4]}_grid.png")
            
            return f"{image_fullpath[:-4]}_grid.png"
        
    def redLine(self):
        image_fullpath = self.fullpath

        if os.path.exists(f"{image_fullpath[:-4]}_red.jpg"):
            return f"{image_fullpath[:-4]}_red.jpg"

        else:
            image = Image.open(image_fullpath)
            draw = ImageDraw.Draw(image)
            
            width, height = image.size
            
            x1, y1 = 0, height // 2
            x2, y2 = width, height // 2

            draw.line((x1, y1, x2, y2), fill='red', width=3)

            
            draw = ImageDraw.Draw(image)

            image.save(f"{image_fullpath[:-4]}_red.jpg")
            return f"{image_fullpath[:-4]}_red.jpg"
        
    def GridHelp(self):

        image_fullpath = self.fullpath[1:]

        if os.path.exists(f"{image_fullpath[:-4]}_grid_help.jpg"):
            return f"{image_fullpath[:-4]}_grid_help.jpg"

        else:
            image = Image.open(image_fullpath)

            width, height = image.size

            image = Image.new('RGB', (width, 1), color=(255, 255, 255))

            width, height = image.size
            image = image.resize((width * 10, height * 10))

            # Create a draw object
            draw = ImageDraw.Draw(image)

            width, height = image.size

            # Set the grid size
            grid_size = 10

            # Draw vertical gridlines
            for x in range(0, width, grid_size):
                draw.line((x, 0, x, height), fill=(0, 153, 153))


            # Save the image with gridlines
            image.save(f"{image_fullpath[:-4]}_grid_help.jpg")

            return f"{image_fullpath[:-4]}_grid_help.jpg"

    def Slice(self):
        namaFile = self.fullpath

        namaDirektori = f"{namaFile[:-4]}"
        Direktori = f"{namaDirektori}"
        temp = []
        if(not os.path.exists(Direktori)):
            os.mkdir(Direktori)

            image = Image.open(namaFile)

            width, height = image.size

            #Pemisahan Baris
            img = cv2.imread(f"{namaFile}", 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            for i in range(0,width, 10):
                    try:
                        na = np.array(img[i:i+10, : ], dtype=np.uint8)
                        # membuat Numpy array menjadi PIL Image dan menyimpan menjadi bentuk jpg
                        Image.fromarray(na).save(f"{namaDirektori}/Baris"+str(i)+".jpg")
                        temp.append(f"{namaDirektori}/Baris"+str(i)+".jpg")
                    except ValueError:
                        break
            return f"{temp}"
        else:
            image = Image.open(namaFile)
            width, height = image.size

            for i in range(0, height, 10):
                try:
                    temp.append(f"{namaDirektori}/Baris"+str(i)+".jpg")
                except ValueError:
                    break
            return f"{temp}"