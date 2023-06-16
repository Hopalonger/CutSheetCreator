import csv
from tabulate import tabulate
from datetime import datetime
from OpenL2MScrape import *


#Todo
#  Rebuild the Search feature based off names - Completed
#Export Vlans as List of Name and Number - Completed
# in main check if vlans exist from report - Scrapped, getting vlans from open l2m from all of them
# if not get from the Scraper
# Start by matching ports with the Gi ports # Completed, code is in main
# Have Table be written as a csv and text file - Completed
# Have Program output the ports that need to be removed as a CutFile, Also as a text and Csv file - Completed
# Add In Vlan Name and input - Completed
# Set Default Vlan for all ports based off most common one - Completed 
# Fix the Dot Env Password system - Completed - 
# Remove disabeld Vlans and set as Default Vlan
# have Output Commands be In Numeric Order
# Update the Readme 
# Check if all of the ports is greater than 48 
# Allow command line arguments
# Upload to box
# Create Trunk Commands List
# Re-write whole program - need to do
# Download AKIPS reports from List of Names, Csv
# Rename Akips File to Name - Completed 
# Run Cutsheet System based off the files - Completed 
# ADd ability to specify the ELEs - Completed 

# Access Port Vlans - List of vlans that should by default be acess ports instead
# of trunk ports
AccessVlans = [1134,504]

# Define the cutoff time
CutoffDate = datetime.strptime("2020-01-01", "%Y-%m-%d")

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






def ExportFile(Sides,name,Interfaces): #Write both left and right tables to a text file, Side 0 is Right, Side 1 is left

    #For Each Active Int
    # For Each for Right side Cycle through until Interface ID is the same
    # Then Append the Interface Value
    # Repeat Above steps for left side
    for Port in Interfaces:
        for Device in Sides[0]:
            if Device[1] == Port[1]:
            #    print(Device) if the port doesnt have a vlan but is active give them vlan 500
                if Device[7] == "":
                    Device.append(Device[8])
                    Device[8] == "500"
                    Device[7] == "MNGT:500"
                Port.append(Device[9])
                #print(Port)
        for Device in Sides[1]:
            if Device[1] == Port[1]:
            #    print(Device) If for some reason that the port doenst have a vlan, give them 500
                if Device[7] == "":
                    Device.append(Device[8])
                    Device[8] == "500"
                    Device[7] == "MNGT:500"
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

def BasicExport(name,Interfaces): #Write both left and right tables to a text file, Side 0 is Right,
    header = ["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID","New Port" ]
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

def AddELE(InputInterfaces,ELE):
    for Interface in InputInterfaces:
    # If there is an ele that was passed in the command line argument, and there is no ELE On the port
     # then add the Specified ELE to it
        if ELE != 'none':
            if "###" not in Interface[6]:
                # update the discription
                Interface[6] = Interface[6] + " ###" + ELE
    
    return InputInterfaces



def OutputCommands(Sides, Filename):  # Write the HPE commands to a Txt file
    RightInterfaces = Sides[0]  # Get right side
    LeftInterfaces = Sides[1] # get left side

    #Vlans On the Device
    OnSwitchVlanNum = []
    OnSwitchVlanName =[]
    name = "OutputCommands_" + Filename + ".txt" # create the name of the output file
    out = open(name,'w') # open the file

    i = 24 # Start out at interface 24, or the right side
    d = 1 # start on the first device
    for Interface in RightInterfaces:
        i += 1 # iterate the list
        if Interface[8] == None: # if no vlan defined set it equal to one
            Interface[8] = "1"

        # Vlan Check Goes Here
        # If the Vlan number is not in the list of vlans that will be added to switch
        # Then Add it to the list, along with the Vlan Name
        if Interface[8] not in OnSwitchVlanNum:
            OnSwitchVlanNum.append(Interface[8])
            OnSwitchVlanName.append(Interface[7])


        if int(Interface[8]) in AccessVlans: # if The port is in a list of acess ports
            print("Genereating Access Port ")
            out.write( "int gi "+ str(d) +"/0/" + str(i) + "\n") # Select the new port
            out.write("port link-type access \n") # Set the port to be an acess port
            out.write("port access vlan "+ Interface[8]+ "\n") # Set the acess port vlan
        else:
            out.write( "int gi "+ str(d) +"/0/" + str(i) + "\n") # Select the new port
            out.write("undo port trunk permit vlan 999 \n") # Remove vlan 999 as a supported vlan
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

        # Vlan Check Goes Here
        # If the Vlan number is not in the list of vlans that will be added to switch
        # Then Add it to the list, along with the Vlan Name
        if Interface[8] not in OnSwitchVlanNum:
            OnSwitchVlanNum.append(Interface[8])
            OnSwitchVlanName.append(Interface[7])

        # Write out the commands
        if Interface[8] in AccessVlans: # if The port is in a list of acess ports
            out.write( "int gi "+ str(d) +"/0/" + str(i) + "\n") # Select the new port
            out.write("port link-type access \n") # Set the port to be an acess port
            out.write("port acess vlan "+ Interface[8]+ "\n") # Set the acess port vlan
        else:
            out.write( "int gi "+ str(d) +"/0/" + str(i) + "\n") # Select the new port
            out.write("undo port trunk permit vlan 999 \n") # Remove vlan 999 as a supported vlan
            out.write( "port trunk permit vlan " + Interface[8]+ "\n") # command to change the vlan
            out.write( "port trunk pvid vlan " + Interface[8]+ "\n")# second command for the vlan

        out.write( "desc " + Interface[6]+ "\n") # update the discription


        if i == 24:
            i = 0
            d += 1

    # Write out the Vlan configuration
    i = 0
    for VlanNum in OnSwitchVlanNum:
        out.write("Vlan " + VlanNum + " \n")
        out.write("name " + OnSwitchVlanName[i] + " \n")
        i += 1
    out.close()
    if d > devices: # Return which ever device count is greater so we know how many
    #switches to use
        return d
    return devices

def PortPatch(Sides,Filename):
    File = "Port_Patch_"+Filename+".csv" # Create File Name
    out = open(File,'w') # open the file

    RightInterfaces = Sides[0] # Get right side
    LeftInterfaces = Sides[1] # get left side

    i = 24 # Start out at interface 24, or the right side
    d = 1 # start on the first device
    for Interface in RightInterfaces:
        i += 1 # iterate the list

        out.write( Interface[6]+ ","+  str(d) +"/0/" + str(i) + ",\n") # Create a pointer that Matches Description with Port

        if i == 48: # if port 48 is reached, iterate to the next device
            i = 24
            d += 1
    i = 0
    d = 1
    for Interface in LeftInterfaces:
        i += 1 # iterate the list

        out.write( Interface[6]+ ","+  str(d) +"/0/" + str(i) + ",\n") # Create a pointer that Matches Description with Port

        if i == 24: # if port 48 is reached, iterate to the next device
            i = 0
            d += 1


def QueryVlans(Name):

    print("Logged In")
    print("Got Switch URL ")
    switchUrl = GetSwitchURLFromName(Name)
    Combined_List = getVlan(switchUrl)
    #print(VlanList)
    return Combined_List

def GetVlans(Interfaces,Vlans): #query OpenL2MScrape to get the Vlans for the Device
    # Get a list of vlans for each port from OpenL2M
    Combined_List = QueryVlans(Interfaces[1][0]) #Use Device Name

    # Combined list: Interface Number, Vlan Number, Vlan Name
    i = 0
#    print("Updating List")
    for Interface in Interfaces:

    # Check if the Port is an standard Edge Port
        try:
            # Get the Interfaces Inteface Number and check if its first letter starts
            # With G
            if Interface[1][0] == 'G':
            #    print(VlansList)
            #    print(i)
                #print(Interfaces)
                # Go through Combined List of Vlans and Ports
                Vlan_Name = ""
                for Tray in Combined_List:
                    # Find the combined Interface
                    if Tray[0] == Interface[1]:
                        print(Tray)
                        # if the Vlan for the interface is Disabled or not set, set it to vlan 1270
                        if Tray[1] == 999 or Tray[1] == 1:
                            PortVlan = 1270
                            Vlan_Name = "CAS-Wks_W"
                        else:
                            #If not a disabled vlan set portVLan to be
                            PortVlan = Tray[1]
                            Vlan_Name = Tray[2]


                Interface[7] = Vlan_Name # Updated Vlan value in list to be the text vlan name
                #Append The Vlan Number to the Specific Interface List
                Interface.append(PortVlan)
                i += 1
        except IndexError:
            return Interfaces
    return Interfaces




# Main Section Here
def BigFunc(File,ELE):


    #File = "Aus-310-vfsw_Source.csv"
    ImportSheet = ReadSheet(File)
    #print(ImportSheet)
    header =  ImportSheet[0]
    del ImportSheet[0] # Remove the header of the sheet
    Vlans = []
    Interfaces = ImportSheet

    # Get The Name of the file we want for output
    Filename = ImportSheet[0][0] # Get the name of the switch file. 

    print(f"The Devices Name is: {Filename} and all of the files will be output to its folder")

    AddELE(Interfaces, ELE)
    #Return a list of ports that are deemed active based off cut off date, and current status
    #This is from the list of ports on the sheet

    Interfaces = GetVlans(Interfaces,Vlans) ## Append Vlans from OpenL2M onto the ports

    Backup = Interfaces
    ProcessedInterfaces = GetActiveInterfaces(Interfaces)
    ActiveInts = ProcessedInterfaces[0]
    DeactivatedInts = ProcessedInterfaces[1]
    #Check if Sheet Has Vlans

#    Interfaces =GetActiveVlans(ActiveInts,Vlans)


    #print(tabulate(Interfaces, headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID" ], tablefmt="pretty"))

    Sides = Organize(ActiveInts)
    Sides = GetNewPort(Sides)

    print("Right Side Interfaces Have Been Organized and generated") 
   # print(tabulate(Sides[0], headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID","New Port" ], tablefmt="pretty"))
    print("Left Side Interfaces have been organized and generated")
    #print(tabulate(Sides[1], headers=["Device","Interface ID","Speed","Status","State","Last Change","Desc","Vlan Name","Vlan ID", "New Port" ], tablefmt="pretty"))
    Devices = OutputCommands(Sides,Filename)
    PortPatch(Sides,Filename)

    # Create an export of the files so that we can review them later
    BackupFileName = "Backup_" + Filename
    BasicExport(BackupFileName,Backup)


    # Print out all of the Activated Ports
    name = "OutputActive_" + Filename
    ExportFile(Sides,name,ActiveInts)
    # Print out all of the Deactivated Ports
    name = "Deactivated_" + Filename
    ExportFile(Sides,name,DeactivatedInts)
    print("Num of HPE Switches Needed: " + str(Devices))
    return Filename
