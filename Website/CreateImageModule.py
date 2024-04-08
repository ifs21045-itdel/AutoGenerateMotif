import cv2
import os
import uuid
import pants
import numpy as np
from PIL import Image
from itertools import permutations
from .Function import TabuSearch
from .Function import RandomSearch
from .Function import GreedySearch
from .Function import ACO
from .Function import SkorPertama
from .ProcessImage import ScaleImage
from .ProcessImage import ProcesImage
from .ProcessImage import SeparateImage
from .ProcessImage import ConvertRGB
from .ProcessImage import ConvertArrayImage
from .ProcessImage import ConvertLiditoArray
from .ProcessImage import CreateImage

class CreateImageMotif:
    def __init__(self, fullpath, namaMotif, jmlBaris, Baris, mode, username):
        self.fullpath = fullpath
        self.namaMotif = namaMotif
        self.jmlBaris = jmlBaris
        self.Baris = Baris
        self.mode = mode
        self.username = username
    
    def imageEven(self):
        def SkorACO(a, b):
            temp1 = Array_data[a[0]]
            temp2 = Array_data[a[1]]
            temp3 = Array_data[b[0]]
            temp4 = Array_data[b[1]]

            SkorArray1 = SkorPertama(temp1, temp2)
            SkorArray2 = SkorPertama(temp3, temp4)
            SkorArray3 = SkorPertama(temp2, temp3)

            SkorArray = 1/(1 + SkorArray1 + SkorArray2 + SkorArray3)
            return SkorArray
        
        image_fullpath = self.fullpath
        image_name = self.namaMotif
        
        jmlBaris = int(self.jmlBaris)
        jmlBaris = int(jmlBaris/2)
        
        Baris = int(self.Baris)

        ModeGenerate = self.mode
        folderUser = self.username
        makeFolder = f"media/{folderUser}"

        if(not os.path.exists(makeFolder)):
            os.mkdir(makeFolder)
        
        ModeGenerate = int(ModeGenerate)

        unique_file_name = uuid.uuid4().hex
        unique = f"{folderUser}/{unique_file_name}.png"
        image_save_path = image_fullpath.replace(image_name, unique)

        namaDirektori = f"Image/{folderUser}"
        Direktori = str(namaDirektori)

        if(not os.path.exists(Direktori)):
            os.mkdir(Direktori)

        #Separate Image
        img = cv2.imread(str(image_fullpath), 1)
        SeparateImage(img, Direktori)

        height, width, channels = img.shape

        img = []
        Lidi = []

        # Conver to RGBA
        img, Lidi = ConvertRGB(img, Lidi, height, Direktori)

        # Convert Binary
        Array_data = []
        Tabu_List = []

        Array_data = ConvertArrayImage(img, Array_data)

        comb = list(permutations(Lidi, 2))

        SkorArray = []
        for i in range(0, int(len(Lidi))):
            for j in range(0, int(len(Lidi)-1)):
                temp1 = Array_data[i].copy()
                temp2 = Array_data[j].copy()

                SkorArray.append(SkorPertama(temp1, temp2))
        
        #ACO
        world = pants.World(comb, SkorACO)
        solver = pants.Solver()

        comb = np.array_split(comb, height)
        PanjangLidi = int(len(Lidi))-1

        if(ModeGenerate == 1):
            Tabu_List, Best_Solution = TabuSearch(PanjangLidi, Array_data, Baris, jmlBaris, Tabu_List)
            a = Best_Solution[0]
        elif(ModeGenerate == 2):
            a = GreedySearch(PanjangLidi, comb, Baris, jmlBaris)
        elif(ModeGenerate == 3):
            a = RandomSearch(PanjangLidi, jmlBaris)
        elif(ModeGenerate == 4):
            a = ACO(solver, world, jmlBaris)
        
        img = cv2.imread(str(image_fullpath), 1)

        height, width, channels = img.shape
        img = []

        img = ConvertLiditoArray(img, height, Direktori)

        c = a.copy()
        c = c[::-1]
        a.extend(c)
        b = a.copy()
        b = [x+1 for x in b]

        img = CreateImage(a, img)
        Image.fromarray(img).save(f"{namaDirektori}/Hasil1.jpg")
        
        img = Image.open(f"{namaDirektori}/Hasil1.jpg")
        img = ProcesImage(img)
        img = ScaleImage(img)
        img.save(image_save_path)

        return f"/media/{folderUser}/{unique_file_name}.png", b
        
    def imageOdd(self):
        def SkorACO(a, b):
            temp1 = Array_data[a[0]]
            temp2 = Array_data[a[1]]
            temp3 = Array_data[b[0]]
            temp4 = Array_data[b[1]]

            SkorArray1 = SkorPertama(temp1, temp2)
            SkorArray2 = SkorPertama(temp3, temp4)
            SkorArray3 = SkorPertama(temp2, temp3)

            SkorArray = 1/(1 + SkorArray1 + SkorArray2 + SkorArray3)
            return SkorArray
        
        image_fullpath = self.fullpath
        image_name = self.namaMotif
        
        jmlBaris = int(self.jmlBaris)+1
        jmlBaris = int(jmlBaris/2)
        
        Baris = int(self.Baris)

        ModeGenerate = self.mode
        folderUser = self.username
        makeFolder = f"media/{folderUser}"

        if(not os.path.exists(makeFolder)):
            os.mkdir(makeFolder)
        
        ModeGenerate = int(ModeGenerate)

        unique_file_name = uuid.uuid4().hex
        unique = f"{folderUser}/{unique_file_name}.png"
        image_save_path = image_fullpath.replace(image_name, unique)

        namaDirektori = f"Image/{folderUser}"
        Direktori = str(namaDirektori)

        if(not os.path.exists(Direktori)):
            os.mkdir(Direktori)

        #Separate Image
        img = cv2.imread(str(image_fullpath), 1)
        SeparateImage(img, Direktori)

        height, width, channels = img.shape

        img = []
        Lidi = []

        # Conver to RGBA
        img, Lidi = ConvertRGB(img, Lidi, height, Direktori)

        # Convert Binary
        Array_data = []
        Tabu_List = []

        Array_data = ConvertArrayImage(img, Array_data)

        comb = list(permutations(Lidi, 2))

        SkorArray = []
        for i in range(0, int(len(Lidi))):
            for j in range(0, int(len(Lidi)-1)):
                temp1 = Array_data[i].copy()
                temp2 = Array_data[j].copy()

                SkorArray.append(SkorPertama(temp1, temp2))
        
        #ACO
        world = pants.World(comb, SkorACO)
        solver = pants.Solver()

        comb = np.array_split(comb, height)
        PanjangLidi = int(len(Lidi))-1

        if(ModeGenerate == 1):
            Tabu_List, Best_Solution = TabuSearch(PanjangLidi, Array_data, Baris, jmlBaris, Tabu_List)
            a = Best_Solution[0]
        elif(ModeGenerate == 2):
            a = GreedySearch(PanjangLidi, comb, Baris, jmlBaris)
        elif(ModeGenerate == 3):
            a = RandomSearch(PanjangLidi, jmlBaris)
        elif(ModeGenerate == 4):
            a = ACO(solver, world, jmlBaris)
        
        img = cv2.imread(str(image_fullpath), 1)

        height, width, channels = img.shape
        img = []

        img = ConvertLiditoArray(img, height, Direktori)

        temp = a.pop()
        c = a.copy()
        c = c[::-1]

        a.append(temp)
        a.extend(c)
        b = a.copy()
        b = [x+1 for x in b]

        img = CreateImage(a, img)
        Image.fromarray(img).save(f"{namaDirektori}/Hasil1.jpg")
        
        img = Image.open(f"{namaDirektori}/Hasil1.jpg")
        img = ProcesImage(img)
        img = ScaleImage(img)
        img.save(image_save_path)

        return f"/media/{folderUser}/{unique_file_name}.png", b

