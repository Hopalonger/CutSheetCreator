from OpenL2MScrape import login, Quit
from os import listdir
from os import walk
from os import mkdir
from Main import BigFunc
import shutil
import os
import argparse

import time
mypath = "C:/Users/ripte/Documents/CutSheetCreator/Input"
outputpath = "C:/Users/ripte/Documents/CutSheetCreator/Output"
Completed =  "C:/Users/ripte/Documents/CutSheetCreator/Completed"
Local = "C:/Users/ripte/Documents/CutSheetCreator"

parser = argparse.ArgumentParser(
    description='Take AKIPS Information and use it to generate Cutsheets')

parser.add_argument('--username', '-u',
                    help='REQUIRED: Username for OpenL2M (ONID EX: Hopkinsr)', nargs=1, required=True)
parser.add_argument('--password', '-p',
                    help='REQUIRED: Username for OpenL2M (ONID Password)', nargs=1, required=True)

parser.add_argument('--mode', '-m',
                    help=' Port Organizational Mode, Options: Managed, Unmanaged, Managed attempts to organizes interfaces and Patch Panel Cables through reordering Jack numbers then paring with interface (For full rewires) [ Defaults: Unmanaged]', nargs=1, default="Unmanaged")

parser.add_argument('--file', '-f',
                    help='Specify File Path for file that you want to parse, this will only run that singular file [Default: Will loop through input]', nargs=1, default="loop")

parser.add_argument('--ELE', '-e',
                    help='Specify an an ELE that you would like to add to each of the ports Descriptions [EX -e 35611] [Default: No ELE]', nargs=1, default="none")


args = parser.parse_args()
# print(parser.parse_args())
# Get the Username
#print(args.username[0])
#print(args.password[0])


def GetInputFiles():

    filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
    print("Found Files:")
    print(filenames)
    return filenames


if args.file != "loop":
    print("Moving User Input File")
    shutil.move(args.file[0], mypath + "/userinput.csv")

# Get all Input Files From Input Directory
Files = GetInputFiles()



# Start the Selinum Instance 
print("Logging Into OpenL2MScrape")
# Log the user into OpenL2m 
login(args.username[0], args.password[0])
for File in Files:
    print(File)
    
    if File[-4:] == ".csv":
        print(f"Starting to Process File: {File}")
        

        Filepath =  mypath + "/" + File

        shutil.move(Filepath,Local +"/" + File )#Move file from input folder to main dir for processing
        #Completed = Completed + "/" + File
        print("File Moved to Processing Directory...")

        
        Filename = File[0:-4]

        print("Running File: " + Filename)

        # Get the filename from the Akips File Hostname
        NewFilename = BigFunc(File, args.ELE[0], args.mode[0])

        # Make Output Directory
        path = os.path.join(outputpath + "/", NewFilename)

        # Try to make a Directory 
        try:
            os.mkdir(path)
        except FileExistsError:
            print("Output Directory already exists, continuing...")


        NewFileNameNoExt = NewFilename[0:-4]

        output = outputpath + "/" + NewFilename
        # Copy The input File into the completed output
        shutil.copy(Local + "/" + File, outputpath + "/" + NewFilename + "/INPUT_" + NewFilename + ".csv")
        # Rename the Input file to have the proper name

        os.rename(Local + "/" + File, Local + "/" + NewFilename + ".csv")

        #File was renamed so we use the new file name 
        # Move the Local File to Completed
        shutil.move(Local + "/" + NewFilename + ".csv", Completed)

        #Create a folder for each device
        print("Output Directory created")

        BigFuncCommandOut = Local + "/" + "OutputCommands_" + NewFilename + ".txt"
        CommandsOUtput = output + "/" + "OutputCommands_" + NewFilename + ".txt"
        shutil.move(BigFuncCommandOut,CommandsOUtput) # move output cmmands to output

        BigFuncCommandOut = Local + "/" + "Port_Patch_" + NewFilename + ".csv"
        CommandsOUtput = output + "/" + "Port_Patch_" + NewFilename + ".csv"
        shutil.move(BigFuncCommandOut,CommandsOUtput) # move port patch to output

        BackupCommandsLocal = Local + "/" + "Backup_" + NewFilename + ".csv"
        BackupCommandsCompleted = output + "/" + "Backup_" + NewFilename + ".csv"
        # move backup patch to output
        shutil.move(BackupCommandsLocal, BackupCommandsCompleted)


        OutPutActive = Local + "/" + "OutputActive_" + NewFilename + ".txt"
        OutPutActivecsv = Local + "/" + "OutputActive_" + NewFilename + ".csv"
        OutputActiveOut = output + "/" + "OutputActive_" + NewFilename + ".txt"
        OutputActiveOutcsv = output + "/" + "OutputActive_" + NewFilename + ".csv"
        # Move output Table to Output
        shutil.move(OutPutActive, OutputActiveOut)
        shutil.move(OutPutActivecsv,OutputActiveOutcsv)# Move output csv to Output

        OutputInactive = Local + "/" + "Deactivated_" + NewFilename + ".txt"
        OutputInactivecsv = Local + "/" + "Deactivated_" + NewFilename + ".csv"
        OutputInactiveOut = output + "/" + "Deactivated_" + NewFilename + ".txt"
        OutputInactiveOutcsv = output + "/" + "Deactivated_" + NewFilename + ".csv"
        shutil.move(OutputInactive,OutputInactiveOut)# Move output Table to Output for the inactive Sheets
        shutil.move(OutputInactivecsv,OutputInactiveOutcsv)# Move output csv to Output for the inactive sheets
        print("Output Files Moved to Output Directory...")
        print(Completed)




Quit()
