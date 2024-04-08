import numpy as np
import os
import cv2
from PIL import ImageOps
from PIL import Image

def SeparateImage(img, namaDirektori):
    for i in range(0,72):
        try:
            na = np.array(img[i:i+1, : ], dtype=np.uint8)
            # membuat Numpy array menjadi PIL Image dan menyimpan menjadi bentuk jpg
            Image.fromarray(na).save(f"{namaDirektori}/Baris"+str(i)+".jpg")
            
        except ValueError:
            break



def ConvertRGB(img, Lidi, height, namaDirektori):
    for i in range(0,height):
    
        try:
            img_temp = Image.open(f'{namaDirektori}/Baris'+str(i)+'.jpg')
            img_temp.convert("RGBA")
            datas = img_temp.getdata()
            img.append(datas)
            Lidi.append(i)
        except FileNotFoundError:
            break
    return [img, Lidi]



def ConvertArrayImage(img, Array_data):
    for i in range(0,72):
        try:
            Baca_data = []
            datas = img[i]
            for item in datas:
                if item[0] > 200 and item[1] > 200 and item[2] > 200:
                    Baca_data.append(1)
                else:
                    Baca_data.append(2)
            Array_data.append(Baca_data)
        except IndexError:
            break
    return Array_data



def ConvertLiditoArray(img, height, namaDirektori):
    for i in range(0,height):
        try:
            img.append(cv2.imread(f'{namaDirektori}/Baris'+str(i)+'.jpg', 1))
        except:
            break
    return img



def CreateImage(a, img):
    while len(a) >=0:
        try:
            image1 = a.pop(0)
            image2 = a.pop(0)
            mix = np.vstack((img[image1], img[image2]))
            while len(a) >=0:
                image3 = a.pop(0)
                mix = np.vstack((mix, img[image3]))
        except Exception:
            break
    return mix



def ScaleImage(img):
    img = ImageOps.scale(img, 10, resample=0)
    return img



def ProcesImage(img):
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []

    for item in datas:
        if item[0] > 150 and item[1] > 150 and item[2] > 200:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)

    datas = img.getdata()


    newData = []


    for item in datas:
        if item[0] < 150 and item[1] < 150 and item[2] < 200:
            newData.append((0, 0, 0, 255))
        else:
            newData.append(item)

    img.putdata(newData)

    return img