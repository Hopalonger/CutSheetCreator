from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# If you want to open Chrome
driver = webdriver.Chrome()
#The amount of seconds to wait for each webpage to load before executing any scraping commands
page_Delay = 2
# If you want to open Firefox
#driver = webdriver.Firefox()


switchUrl = "https://switches.net.oregonstate.edu/switches/27/391/"


def login(User_cred,Pass_cred):
    print("Got Creds for Username: " + User_cred)
    driver.get("https://switches.net.oregonstate.edu/accounts/login/")
    time.sleep(page_Delay)
    print("Got Login Page")
    username = driver.find_element(By.NAME,'username')
    password = driver.find_element(By.NAME,'password')
    username.send_keys(User_cred)
    password.send_keys(Pass_cred)
    driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    print("Logged In")

# Make sure that the vlan on the switch is a valid vlan, or not set to one that 
# is disabled or not set to any vlan on the switch. 
def CheckIfValidVlan(Row):   
    if Row[0] == "1" or Row[0] == "999":
        Row = ["1100", "CN-UnivAdm_W"]
    return Row

def getVlan(switchUrl): #Get the vlans and write them to a file
    #print(switchUrl)
    driver.get(switchUrl)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    VlanList = []
    for input in soup.find_all('option', selected=True):
        #print(input)
        Words = input.getText() # Get the text, its very long
        #print(Words)
        List = Words.split("\n") # split the new line values into list
        print("Vlan Input Information: ")
        print(List)
        # split the values of Vlan into segments, From ['1114 - CN-StudentAdmin_W'] -> [1114,CN,StudentAdmin_W]
        List = List[0].split("-")
        try:

            # If the Vlan info was seperated into something like this [1114,CN,StudentAdmin_W]
            # Then put the Vlan Name Information Back togehter as one string  [1114,CN,StudentAdmin_W] - > "CN-StudentAdmin_W"
            VlanName = List[1].strip()
            i = 2
            while i < len(List): 
                VlanName = VlanName + "-" + List[i].strip() 
                i += 1 

            # put the Vlan Number and Vlan Name in a list 
            row = [input.get('value'), VlanName]

            row = CheckIfValidVlan(row)


           # print("Final Row Output:")
           # print(row)


            VlanList.append(row)
        #    print(row)
        #    writer.writerow(row)
        except IndexError:
            print("Error parsing Vlans, Please Enter the Vlan Manually:")
            print(List)
            
            row = ["999","Error Parsing Vlan Please edit Manally"]
            VlanList.append(row)

            
    #print(VlanList)

    # Get The Port Description
    table = soup.find('table', class_='table table-hover table-headings w-auto')
    #print(PortTable)
    PortList = []
    Num = 0
    for row in table.tbody.find_all('tr'):

        #print("Row: " + str(Num))
        # Find all data for each column
        columns = row.find_all('td')
        # make sure the collum is not blank
        if(columns != []):

            t = 0
            for data in columns:
                # Get The Interface as raw text
                Interface = data.text.strip()
                # If this is the first colum of the row and the Interface is not a F Type interface
                if(t == 0):
                    if (Interface[0] == "T" or Interface[0] == "G"):
                    #if(Interface[0] == "G"):
                        # Add the Interface to a new list of ports
                        PortList.append(Interface)
                t = t + 1
        Num = 1 + Num


    #print(PortList)
    # Combined the Lists Together
    Combined = []
    i = 0
    for Vlans in VlanList:
        # Set the list to have the Port, Vlan Number, then vlan Name
        #print(PortList[i])
    

        try: 
            print("Merging Vlan: " + Vlans[0]  + " With Port: " + PortList[i])
            Alinged_List = [PortList[i],Vlans[0],Vlans[1]]
            Combined.append(Alinged_List)
            i = i + 1
        except IndexError:
            print("More Vlans than ports Voiding Vlan Info:")
            print(Vlans)
         #print(Combined)



    return Combined

# Check if the port that is provided is valid for a cutsheet
# This would be all gigiabit ports on Models with X/Y/Z format, and all 
# Gigabit Ports in X/Z Format where X is greater than 1 
# IF the Port is not valid return false else return true 
def CheckPort(Port):
    #print(Port[2:3])

    if Port[2:3] == 1: 
        return False 
    
    return True 

def GetTable(switchUrl):
    print(switchUrl)
    driver.get(switchUrl)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # Get all Tables
    tables = soup.findChildren('table')
    # Get the First Table
    PortTable = tables[1]

    print(PortTable)

    rows = my_table.findChildren(['th', 'tr'])

    for row in rows:
         cells = row.findChildren('td')
         for cell in cells:
             value = cell.string
             print("The value in this cell is %s" % value)

def GetSwitchURLFromName(Name):
    driver.get("https://switches.net.oregonstate.edu/switches/")
    Search = driver.find_element(By.NAME,'switchname')
    Search.send_keys(Name)
    driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        if link.getText() == Name.lower():
            link = str("https://switches.net.oregonstate.edu" + link.get('href'))
            print(link)
            return link

    return 0

def Quit():
    #f.close()
    #driver.close()
    return driver.quit()
