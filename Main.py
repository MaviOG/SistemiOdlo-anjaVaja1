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
    #Main
    IniFilePath = GetConfig()
    FilePath = GetFile(IniFilePath)
    Header = ReadHeader(FilePath)
    Pozitiv,Negativ = ReadCsvAndReturnValues(Header,FilePath)
    
    Output(FilePath,Header,Optimist(Pozitiv),Pesimist(Negativ),Laplace(Pozitiv,Negativ),Savage(Pozitiv,Negativ),Negativ,Pozitiv)
    
    
    

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
def Output(FilePath,Header,Optimist,Pesimist,Laplace,Savage,Negativ,Pozitiv):
    print("Izračun osnovnih metod odločanja.")
    print('Prebrana je bila datoteka "'+FilePath.split("\\")[-1]+'.')
    print(f"Optimist: {Optimist}")
    print(f"Pesimist: {Pesimist}")
    print(f"Laplace: {Laplace}")
    print(f"Savage: {Savage}")
    print("Hurwitzev kriterij:")
    max_length = max(len(header) for header in Header)

            # Calculate the spacing based on the maximum length
    spacing = max_length + 5  # Adjust the spacing as needed
    spacingNumber = max(9, len('h') - 1)
    first_spacing = max(8, len('h') - 1)  # Adjust spacing for the first column

            # Print the header row with adjusted spacing
    print("h".ljust(first_spacing), end='')  # Print first column header
    print(" ".join(header.ljust(spacing) for header in Header[1:]))  # Print other column headers
    
    
    for y in range(0,11):
        HurwitzevArray = []
        for z in range(len(Header)-1):
            HurwitzevArray.append(Hurwitzev((y/10),Pozitiv[z],Negativ[z]))
        print(str(y/10).ljust(spacingNumber), end='')
        #print(HurwitzevArray)
        print(" ".join(str(header).ljust(spacing) for header in HurwitzevArray[:]))


    print()  # Move to the next line
    
            # Print subsequent rows
if __name__ == '__main__':
    main()  # next section explains the use of sys.exit