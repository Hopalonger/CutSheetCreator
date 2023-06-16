import PySimpleGUI as sg
import os


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

sg.theme('DefaultNoMoreNagging')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Welcome to Cutsheet Creator:')],
          [sg.Text('Please enter your username and password for OPENL2M')],
          [sg.Text('Username:', size = (15, 1)), sg.InputText('',key='username')],
          [sg.Text('Password', size=(15, 1)), sg.InputText('', key='Password', password_char='*')],
          [[sg.In(), sg.FileBrowse(file_types=(("AKIPS FIles", "*.csv"),))]],
          [sg.Text('Recursively process the files in the "input" folder only'),sg.Checkbox("", key='s1')],
          [sg.Text('ELE Number (if you want to add an ELE to Every Port EX: 35112):')],
          [sg.InputText('',key='ELE')],
          [sg.Button('Ok'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('CutSheet Creator', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    Error = False 
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    #print(values)
    print('Your Username was:', values['username'])
    print('Your password was:', values['Password'])
    print('Your File Selection:', values['Browse'])

    # Error Checking for Null Values on required values 
    if values['username'] == '' or values['Password'] == '':
        print("Please Enter a username and password")
        sg.popup_ok("Please make sure you have entered your username and password")
        Error = True

    if values['Browse'] == '' and values['s1'] == False:
        print("Please make sure you have selected a file for AKIPS")
        sg.popup_ok("Please make sure you have selected a file for AKIPS")
        Error = True

    Command = f"py loop.py  -u {values['username']} -p {values['Password']}"

    # If the user didnt put files in the input directoy then pass on the file they uploaded
    fileArgs = ""
    if values['s1'] == False:
        fileArgs = f" --file {values['Browse']}"

    # Check to see if the ELE Value is numeric or not
    
    ELE = values['ELE']
    if ELE != "": 
        try: 
            if is_number(int(ELE)) != True:
                print("Please make sure you have Entered a numeric value for ELE")
                sg.popup_ok("Please make sure you have Entered a numeric value for ELE")
                Error = True
            else: 
                # If the user put in a ELE Number 
                if int(ELE) > 9999 and int(ELE) < 100000:
                    fileArgs = fileArgs +  f" --ELE {values['ELE']}"
                else: 
                    print("Please make sure you have Entered a Valid ELE ")
                    sg.popup_ok("Please make sure you have Entered a Valid ELE")
                    Error = True
        except ValueError:
            print("Please make sure you have Entered a numeric value for ELE")
            sg.popup_ok("Please make sure you have Entered a numeric value for ELE")
            Error = True

    Command = Command + fileArgs
    print(Command)

    # IF there have been any errors thrown then dont run the command
    if Error != True: 
        # Run the COmmand 
        os.system(Command)

window.close()