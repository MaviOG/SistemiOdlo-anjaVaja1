from PIL import Image, ImageDraw, ImageFont
import os
import sys
import configparser
import csv
def main():
    #Initialization
    IniFilePath = ""
    FilePath = ""
    Header= []
    Pozitiv = []
    Negativ =[]
    PNGFile = "graf.png"
    PNGData = ""

    #Main
    IniFilePath = GetConfig()
    FilePath = GetFile(IniFilePath)
    Header = ReadHeader(FilePath)
    Pozitiv,Negativ = ReadCsvAndReturnValues(Header,FilePath)
    PNGData = HurwitzevKriterijPNG(Header,Pozitiv,Negativ)
    CreatePNGAndSave(PNGFile, PNGData,len(Header))
    Output(FilePath,Header,Optimist(Pozitiv),Pesimist(Negativ),Laplace(Pozitiv,Negativ),Savage(Pozitiv,Negativ),Negativ,Pozitiv,PNGFile)
    
    
def CreatePNGAndSave(filename, text,lenght):
    fnt = ImageFont.truetype('arial.ttf', 40)
    image = Image.new(mode="RGB", size=((lenght*300),800), color="white")
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), text, font=fnt, fill=(0, 0, 0))
    image.save(filename)
    print(f"Image '{filename}' saved successfully.")
    


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
    return min(SavageMax)

    
def Laplace(Pozitivno,Negativno):
    AvrageByColumn = []
    for x in range (len(Pozitivno)):

        AvrageByColumn.append(((Pozitivno[x]+Negativno[x])/2))
    return(max(AvrageByColumn))
def Optimist(List):#Izbere najvecjo stevilko
    return max(List)
def Pesimist(List):
    return min(List)

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
def Output(FilePath,Header,Optimist,Pesimist,Laplace,Savage,Negativ,Pozitiv,PNGFile):
    print("Izračun osnovnih metod odločanja.")
    print('Prebrana je bila datoteka "'+FilePath.split("\\")[-1]+'.')
    print(f"Optimist: {Optimist}")
    print(f"Pesimist: {Pesimist}")
    print(f"Laplace: {Laplace}")
    print(f"Savage: {Savage}")
    HurwitzevKriterij(Header,Pozitiv,Negativ)
    print(f"Graf Hurwitzovega kriterija je bil shranjen v datoteko ('{PNGFile}').")



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

def HurwitzevKriterijPNG(Header, Pozitiv, Negativ):
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
        result += str(y / 10).ljust(spacingNumber)
        result += " ".join(str(header).ljust(spacing) for header in HurwitzevArray[:]) + "\n"
    return result

    print()  # Move to the next line
    
            # Print subsequent rows
if __name__ == '__main__':
    main()  # next section explains the use of sys.exit