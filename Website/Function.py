import numpy as np
from random import randint
    
def SkorPertama(arr1, arr2):
    skor = 0
    for i in range (0, int(len(arr1))):
        if(arr1[i]==2):
            if(arr1[i] == arr2[i]):
                skor += 0.5
            if i < ((int(len(arr1)))-1):
                if(arr1[i] == arr2[i+1]):
                    skor +=1
            if i > 0:
                if(arr1[i] == arr2[i-1]):
                    skor +=1
                
    return skor

def SkorRasio(arr1, arr2):
    skor2 = 0
    rasio1 = 0
    rasio2 = 0
    
    arr3 = arr1 + arr2
    lengt = int(len(arr3))
    for i in range(0, lengt):
        if(arr3[i] == 1):
            rasio1 += 1
        else:
            rasio2 += 1
#     print(rasio1)
#     print(rasio2)
    
    if(rasio1 > rasio2):
        skor2 = rasio2/rasio1
    else:
        skor2 = rasio1/rasio2
    
    return skor2

def densityPixel(arr4):
#     arr4.append(3)
    arr4 = list(arr4)
    temp = arr4[0]
    temp2 = arr4.copy()
    temp2.append(3)
    arr2 = []
    skor3 = 0
    k = 1
    for i in range (1, len(temp2)):
        if(temp == temp2[i]):
            k += 1
        else:
            arr2.append(k)
            k = 1
            temp = temp2[i]
        if(i == int(len(temp2))):
            arr2.append(k)
    
    #remove value array from 1 to 4
    for i in range (1,5):
        arr2 = list(filter((i).__ne__, arr2))
    
    for i in arr2:
        i -= 4
        skor3 +=i

    skor3 = -skor3
    
    return skor3
        
    
            
def SkorTotal(arr1, arr2):
    
    SkorTotal = SkorPertama(arr1,arr2) * SkorRasio(arr1,arr2) + densityPixel(arr1) + densityPixel(arr2)

    if (SkorTotal < 0):
        SkorTotal = float(0)

    SkorTotal = round(SkorTotal,1)
    
    return float(SkorTotal)


def GreedySearch(Lidi,comb, Baris, jmlBaris):
    jmlBaris = int(jmlBaris)
    arr = list()
    arr.append(Baris)
    for i in range(0, jmlBaris-1):
        # inisiasi baris awal
        if(i == 0):
            n = randint(0,Lidi)
        
        # memasukkan kedalam list baris lidi
        arr.append(n)
        
        #temukan index maksimal skor ke semua baris lidi
        maxIndex = np.argmax(comb[n])
        
        maxIndex = int(maxIndex/2)
        
        # ambil baris skor maksimal
        
        n = comb[n][maxIndex][1]
    
    return arr  
    
def RandomSearch(Lidi, jmlBaris):
    arr = list()
    jmlBaris -= 1
    while(jmlBaris > 0):
        
        n = randint(0, Lidi)
        arr.append(n)     
        jmlBaris -= 1   
    return arr



# Tabu Search with random generate lidi

def GenerateArray(Lidi, Array_data, Baris, jmlBaris):
    ScorePass = 30
    arr = list()
    arr.append(Baris)
    jmlBaris -= 1
    while(jmlBaris > 0):
        
        n = randint(0, Lidi)
        a = []
        b = []
        a = Array_data[Baris].copy()
        b = Array_data[n].copy()
        
        while(SkorTotal(a, b)< ScorePass):
            n = randint(0, Lidi)
            b = Array_data[n].copy()
        
        arr.append(n)
        
        Baris = n
            
        jmlBaris -= 1
        
    return arr

def TabuSearch(Lidi, Array_data, Baris,jmlBaris, Tabu_List):
    
    Best_Solution = []
    
    array = GenerateArray(Lidi, Array_data, Baris, jmlBaris)
    
    if(array not in Tabu_List):
#         print(array)
        Best_Solution.append(array)
        # print(Best_Solution)
        Tabu_List.append(array)
    # else:
        # print("Ada di Tabu")
        
    return [Tabu_List, Best_Solution]

def ACO(solver, world, jmlBaris):

    solution = solver.solve(world)
    # or
    solutions = solver.solutions(world)

    best = float("inf")
    for solution in solutions:
        assert solution.distance < best
        best = solution.distance
        path = solution.tour
    
    #convert array 2D to 1D
    convert = np.array(path)
    result = convert.flatten()

    result = list(result)

    temp = []
    for k in range(0, jmlBaris):
        p = result[k]
        temp.append(p)

    return temp

