import os
import sys
import configparser
import csv
def main():
    #Initialization
    IniFilePath = ""
    FilePath = ""
    Header= []
    #Main
    IniFilePath = GetConfig()
    FilePath = GetFile(IniFilePath)
    Header = ReadHeader(FilePath)
    print("Izračun osnovnih metod odločanja.")
    print('Prebrana je bila datoteka "'+FilePath.split("\\")[-1]+'.')
    print("Optimist:")
    print("Pesimist:")
    print("Laplace:")
    print("Savage:")
    print("Hurwitzev kriterij:")
    max_length = max(len(header) for header in Header)

            # Calculate the spacing based on the maximum length
    spacing = max_length + 5  # Adjust the spacing as needed
    first_spacing = max(8, len('h') - 1)  # Adjust spacing for the first column

            # Print the header row with adjusted spacing
    print("h".ljust(first_spacing), end='')  # Print first column header
    print(" ".join(header.ljust(spacing) for header in Header[1:]))  # Print other column headers
    print()  # Move to the next line

            # Print subsequent rows
    









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
if __name__ == '__main__':
    main()  # next section explains the use of sys.exit