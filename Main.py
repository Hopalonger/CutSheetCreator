import csv
from tabulate import tabulate
from datetime import datetime
import sys
from OpenL2MScrape import *


#Todo
#  Rebuild the Search feature based off names - Completed
#Export Vlans as List of Name and Number - Completed
# in main check if vlans exist from report - Scrapped, getting vlans from open l2m from all of them
# if not get from the Scraper
# Start by matching ports with the Gi ports # Completed, code is in main
# Have Table be written as a csv and text file - Completed
# Have Program output the ports that need to be removed as a CutFile, Also as a text and Csv file - Completed
# Fix the Dot Env Password system
# Update the Readme
# Re-write whole program - need to do
# Download AKIPS reports from List of Names, Csv
# Rename Akips File to Name
# Run Cutsheet System based off the files



# Define the cutoff time
CutoffDate = datetime.strptime("2019-06-17", "%Y-%m-%d")

def ReadSheet(File):
    with open(File, newline='') as f:
        reader = csv.reader(f)
        Sheet = list(reader)
        f.close()
        return Sheet
        #open up the file and read it as a giant list

def GetActiveInterfaces(ImportSheet):
    ActiveInts = []
    DeactivatedInts = []
    for Interface in ImportSheet:
        if Interface[5] == "":
            Interface[5] = "2019-06-16 12:00" #if there is no time, assume it is older than Cutoff
        try:
        # If for some reason the date is in a different format than this try the other format
            TimeValue = datetime.strptime(Interface[5],"%Y-%m-%d %H:%M")
        except ValueError:
            TimeValue = datetime.strptime(Interface[5],"%m/%d/%Y %H:%M" )

        if Interface[0] != "": # if there is a value in device
            #print(Interface)
            if Interface[4] =='up': # If Port is currently up Append it to list
                ActiveInts.append(Interface)
            # if down but was active before cutoff date, add to active list
            elif Interface[4] == 'down' and TimeValue >= CutoffDate:
                ActiveInts.append(Interface)

            else:
                DeactivatedInts.append(Interface)
    return [ActiveInts,DeactivatedInts]


def UpdateVlans(Interfaces,Vlans): # Add in each vlan number to the end of each list
    for Interface in Interfaces:
        VlanNum = GetVlan(Interface[7],Vlans)
    #    print(VlanNum)
        Interface.append(VlanNum)

    return Interfaces

def GetVlan(Text,Vlans):
    for Vlan in Vlans: # go throgh the vlan file list
        #print(Text)
        #print(Vlan[0])
        # Set dashes to equal underscores for ease of processing, then if vlan name equal
        # Return the vlan number
        if Text.replace("-","_") == Vlan[0].replace("-","_"):
            #print("Vlans are Equal")
            return Vlan[1]





def ExportFile(Sides,name,Interfaces): #Write both left and right tables to a text file, Side 0 is Right, Side 1 is left

    #For Each Active Int
    # For Each for Right side Cycle through until Interface ID is the same
    # Then Append the Interface Value
    # Repeat Above steps for left side
    for Port in Interfaces:
        for Device in Sides[0]:
            if Device[1] == Port[1]:
                Port.append(Device[9])
                #print(Port)
        for Device in Sides[0]:
            if Device[1] == Port[1]:
                Port.append(Device[9])
                #print(Port)
    header = ["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID","New Port" ]
    #Write as a Pretty Table Txt File
    with open(name + ".txt",'w') as f:
        f.write(tabulate(Interfaces, headers=header, tablefmt="pretty"))
    #    f.write(tabulate(Sides[1], headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID","New Port" ], tablefmt="pretty"))
    f.close()
    # Write as a csv file
    with open(name + ".csv", 'w') as csvfile:
    # creating a csv writer object
        csvwriter = csv.writer(csvfile)

    # writing the Header
        csvwriter.writerow(header)

    # writing the data rows
        csvwriter.writerows(Interfaces)
    csvfile.close()



def Organize(Interfaces):
    RightInterfaces = []# Create empty list
    LeftInterfaces = [] # Create empty list
    for Interface in Interfaces:
        #For every item in the loop

        if Interface[1][0:2] == "Gi": # make sure that its an ethernet port, not fiber based
        #    print(int(Interface[1][4:]))
            # Get the last Number on the end of the Port Number, no matter how many slashes there are
            PortNum = Interface[1].split("/")[-1]
            #
            #
            #print(PortNum)
            if int(PortNum) > 24: # if the port is on higher than port 24
            #Add it to the right list, others (If lower than 24, add to left)
                RightInterfaces.append(Interface)
            else:
                LeftInterfaces.append(Interface)

    Sides = [RightInterfaces, LeftInterfaces] # Combine the two lists for return
    return Sides


def GetNewPort(Sides): # New active devies
    RightInterfaces = Sides[0]
    LeftInterfaces = Sides[1]
    i = 24 # Start out at interface 24, or the right side
    d = 1 # start on the first device
    for Interface in RightInterfaces:
        i += 1 # iterate the list
        Interface.append(str(d) +"/0/" + str(i)) # Add to the end of each interface
        # the new port name, based off device, and the interface id
        if i == 48: # if we reach port 48, then go to the next device
            i = 24
            d += 1
    i = 0 # repeat same process as above, for the range of 1-24 or left side interfaces
    d = 1
    for Interface in LeftInterfaces:
        i += 1
        Interface.append(str(d) +"/0/" + str(i))
        if i == 24:
            i = 0
            d += 1


    return [RightInterfaces,LeftInterfaces]



def OutputCommands(Sides,Filename): # Write the HPE commands to a Txt file
    RightInterfaces = Sides[0] # Get right side
    LeftInterfaces = Sides[1] # get left side
    name = "OutputCommands_" + Filename + ".txt" # create the name of the output file
    out = open(name,'w') # open the file
    i = 24 # Start out at interface 24, or the right side
    d = 1 # start on the first device
    for Interface in RightInterfaces:
        i += 1 # iterate the list
        if Interface[8] == None: # if no vlan defined set it equal to one
            Interface[8] = "1"
        out.write( "int gi "+ str(d) +"/0/" + str(i) + "\n") # Select the new port
        out.write( "port trunk permit vlan " + Interface[8]+ "\n") # command to change the vlan
        out.write( "port trunk pvid vlan " + Interface[8]+ "\n")# second command for the vlan
        out.write( "desc " + Interface[6]+ "\n") # update the discription

        if i == 48: # if port 48 is reached, iterate to the next device
            i = 24
            d += 1

    devices = d # Set device max number
    i = 0
    d = 1
    for Interface in LeftInterfaces: # Do the process that is the same as above again,
    # But in the range of 0-24 instead
        i += 1
        if Interface[8] == None:
            Interface[8] = "1"
        out.write( "int gi "+ str(d) +"/0/" + str(i) + "\n")
        out.write( "port trunk permit vlan " + Interface[8]+ "\n")
        out.write( "port trunk pvid vlan " + Interface[8]+ "\n")
        out.write( "desc " + Interface[6]+ "\n")
        if i == 24:
            i = 0
            d += 1
    out.close()
    if d > devices: # Return which ever device count is greater so we know how many
    #switches to use
        return d
    return devices

def QueryVlans(Name):

    print("Logged In")
    switchUrl = GetSwitchURLFromName(Name)
    print("Got Switch URL ")
    print(switchUrl)
    VlanList = getVlan(switchUrl)
    return VlanList

def GetActiveVlans(ActiveInts,Vlans): #query OpenL2MScrape to get the Vlans for the Device

    VlansList = QueryVlans(ActiveInts[1][0]) #Use Device Name
    i =0
#    print("Updating List")
    for Interfaces in ActiveInts:
    #    print(Interfaces[1])
    #    print(Interfaces[1][0])
        if Interfaces[1][0] == 'G':
            Interfaces[7] = VlansList[i][1] # Updated Vlan value in list to be the text vlan name
            #print(VlansList[i])
            Interfaces.append(VlansList[i][0])
            i += 1
    return ActiveInts


# Main Section Here
def BigFunc(File):

    Filename = File[0:-4]

    print(Filename)
    #File = "Aus-310-vfsw_Source.csv"
    ImportSheet = ReadSheet(File)
    #print(ImportSheet)
    header =  ImportSheet[0]
    del ImportSheet[0] # Remove the header of the sheet
    Vlans = []

    #Return a list of ports that are deemed active based off cut off date, and current status
    #This is from the list of ports on the sheet
    ProcessedInterfaces = GetActiveInterfaces(ImportSheet)
    ActiveInts = ProcessedInterfaces[0]
    DeactivatedInts = ProcessedInterfaces[1]
    #Check if Sheet Has Vlans

    Interfaces =GetActiveVlans(ActiveInts,Vlans)
    #print(tabulate(Interfaces, headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID" ], tablefmt="pretty"))

    Sides = Organize(Interfaces)
    Sides = GetNewPort(Sides)

    print("Right Side Interfaces")
    print(tabulate(Sides[0], headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID","New Port" ], tablefmt="pretty"))
    print("Left Side Interfaces")
    print(tabulate(Sides[1], headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID", "New Port" ], tablefmt="pretty"))
    Devices = OutputCommands(Sides,Filename)
    # Print out all of the Activated Ports
    name = "OutputActive_" + Filename
    ExportFile(Sides,name,ActiveInts)
    # Print out all of the Deactivated Ports
    name = "Deactivated_" + Filename
    ExportFile(Sides,name,DeactivatedInts)
    print("Num of HPE Switches Needed: " + str(Devices))
