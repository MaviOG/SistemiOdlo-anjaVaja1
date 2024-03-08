from PIL import Image, ImageDraw, ImageFont
from matplotlib import pyplot as plt
import os
import sys
import configparser
import csv
import numpy as np

def main():
    #Initialization
    IniFilePath = ""
    FilePath = ""
    Header= []
    Pozitiv = []
    Negativ =[]
    PNGData = ""
    #Main
    IniFilePath = GetConfig()
    FilePath = GetFile(IniFilePath)
    Header = ReadHeader(FilePath)
    Pozitiv,Negativ = ReadCsvAndReturnValues(Header,FilePath)
    PNGData = HurwitzevKriterijPNG(Header,Pozitiv,Negativ)
    valueLaplace,indexLaplace = Laplace(Pozitiv,Negativ)
    vlaueSavage,indexSavage  = Savage(Pozitiv,Negativ)
    Output(FilePath,Header,Optimist(Pozitiv),Pesimist(Negativ),valueLaplace,indexLaplace,vlaueSavage,indexSavage,Negativ,Pozitiv)
    
    
def Savage(Pozitivno,Negativno):
    SavagePozitiv = []
    SavageNegativ = []
    SavageMax = []
    MaxPozitiv = max(Pozitivno)
    MaxNegativ = max(Negativno)
    for x in range (len(Pozitivno)):
        SavagePozitiv.append(MaxPozitiv - Pozitivno[x])
        SavageNegativ.append(MaxNegativ - Negativno[x])  
    for y in range(len(SavageNegativ)):
        SavageMax.append(max(SavageNegativ[y],SavagePozitiv[y]))
       
    min_value = min(SavageMax)
    index = SavageMax.index(min_value)
    return min(SavageMax),index

    
def Laplace(Pozitivno,Negativno):
    AvrageByColumn = []
    for x in range (len(Pozitivno)):

        AvrageByColumn.append(((Pozitivno[x]+Negativno[x])/2))
    max_value = max(AvrageByColumn)
    index = AvrageByColumn.index(max_value)
    return max(AvrageByColumn),index
def Optimist(List):#Izbere najvecjo stevilko
    return max(List)
def Pesimist(List):
    return max(List)

def ReadCsvAndReturnValues(Header,path):
    FirstLine = []
    SecoundLine = []
    HeaderIndex = 0
    LineCounter = 0
    
    for string in Header:  
        if HeaderIndex == 0:
            pass
        else:
            with open(path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    
                    if LineCounter % 2 == 0:
                        FirstLine.append(int(row[string]))
                        LineCounter +=1
                    else:
                        SecoundLine.append(int(row[string]))
                        LineCounter +=1
                        
        HeaderIndex +=1
    if sum(FirstLine) > sum(SecoundLine):
        return FirstLine,SecoundLine
    else:
        return SecoundLine,FirstLine
def Hurwitzev(h,optimist,pesimist):
    resault = h*optimist+(1-h)*pesimist
    resault = round(resault, 2)
    return resault

def ReadHeader(path):
    path = path.strip('"')
    with open(path) as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        first_row = next(reader)
    return(first_row)

def GetFile(path):
    config = configparser.ConfigParser()
    config.read(path)
    FilePath = config.get('Config','Path')
    return FilePath
def GetConfig():    
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_name = 'Config.ini'
    file_path = os.path.join(current_directory, file_name)
    return file_path
def Output(FilePath,Header,Optimist,Pesimist,Laplace,LaplaceIndex,Savage,SavageIndex,Negativ,Pozitiv):
    indexofOptimist = Pozitiv.index(Optimist)
    indexofPesimist = Negativ.index(Pesimist)
    print("Izračun osnovnih metod odločanja.")
    print('Prebrana je bila datoteka "'+FilePath.split("\\")[-1]+'.')
    print(f"Optimist:{Header[indexofOptimist+1]} {Optimist}")
    print(f"Pesimist:{Header[indexofPesimist+1]} {Pesimist}")
    print(f"Laplace:{Header[LaplaceIndex+1]} {Laplace}")
    print(f"Savage: {Header[SavageIndex+1]} {Savage}")
    HurwitzevKriterij(Header,Pozitiv,Negativ)
    

def HurwitzevKriterij(Header,Pozitiv,Negativ):
    print("Hurwitzev kriterij:")
    max_length = max(len(header) for header in Header)
    spacing = max_length + 5  
    spacingNumber = max(9, len('h') - 1)
    first_spacing = max(8, len('h') - 1)  
    print("h".ljust(first_spacing), end='')  
    print(" ".join(header.ljust(spacing) for header in Header[1:])) 
    for y in range(0,11):
        HurwitzevArray = []
        for z in range(len(Header)-1):
            HurwitzevArray.append(Hurwitzev((y/10),Pozitiv[z],Negativ[z]))
        print(str(y/10).ljust(spacingNumber), end='')
        print(" ".join(str(header).ljust(spacing) for header in HurwitzevArray[:]))
    print("Ustvarjena datoteka z grafom ('plot.png')")

def HurwitzevKriterijPNG(Header, Pozitiv, Negativ):
    ALLHurwitzevArray = []
    result = "Hurwitzev kriterij:\n"
    max_length = max(len(header) for header in Header)
    spacing = max_length + 13 
    spacingNumber = max(13, len('h') - 1)
    first_spacing = max(13, len('h') - 1)  
    result += "h".ljust(first_spacing)
    result += " ".join(header.ljust(spacing-3) for header in Header[1:]) + "\n"
    for y in range(0, 11):
        HurwitzevArray = []
        for z in range(len(Header) - 1):
            HurwitzevArray.append(Hurwitzev((y / 10), Pozitiv[z], Negativ[z]))
            ALLHurwitzevArray.append(Hurwitzev((y / 10), Pozitiv[z], Negativ[z]))
        result += str(y / 10).ljust(spacingNumber)
        result += " ".join(str(header).ljust(spacing) for header in HurwitzevArray[:]) + "\n"
    DrawGraf(ALLHurwitzevArray,Header)
    return result

def DrawGraf(lst,header):
    povecava = 0
    for i in range(int(len(lst) / 10)):
        x = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        y = [lst[povecava], lst[povecava+int(len(lst)/ 10)], lst[povecava+(int(len(lst)/ 10)*2)], lst[povecava+(int(len(lst)/ 10)*3)], lst[povecava+(int(len(lst)/ 10)*4)], lst[povecava+(int(len(lst)/ 10)*5)], lst[povecava+(int(len(lst)/ 10)*6)], lst[povecava+(int(len(lst)/ 10)*7)], lst[povecava+(int(len(lst)/ 10)*8)], lst[povecava+(int(len(lst)/ 10)*9)]]
        plt.plot(x, y,label=header[povecava+1])
        plt.xticks(np.linspace(0.1, 1.0, num=10), ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0'])
        povecava += 1
    plt.legend()
    plt.savefig('plot.png')
    
    

if __name__ == '__main__':
    main()  # next section explains the use of sys.exit