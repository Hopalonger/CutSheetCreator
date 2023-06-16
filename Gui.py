import PySimpleGUI as sg
import os

sg.theme('DefaultNoMoreNagging')   # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('Welcome to Cutsheet Creator:')],
          [sg.Text('Please enter your username and password for OPENL2M')],
          [sg.Text('Username:', size = (15, 1)), sg.InputText('',key='username')],
          [sg.Text('Password', size=(15, 1)), sg.InputText('', key='Password', password_char='*')],
          [[sg.In(), sg.FileBrowse(file_types=(("AKIPS FIles", "*.csv"),))]],
          [sg.Text('Files are in input Directory'),sg.Checkbox("FileInput", key='s1')],
          [sg.Button('Ok'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('CutSheet Creator', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
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

    if values['Browse'] == '' and values['s1'] == False:
        print("Please make sure you have selected a file for AKIPS")
        sg.popup_ok("Please make sure you have selected a file for AKIPS")

    Command = f"py loop.py + -u {values['username']} -p {values['Password']}"

    # If the user didnt put files in the input directoy then pass on the file they uploaded
    fileArgs = ""
    if values['s1'] == False:
        fileArgs = f"--file {values['Browse']}"

    Command = Command + fileArgs
    print(Command)

    # Run the COmmand 
    os.system(Command)

window.close()