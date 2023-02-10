import PySimpleGUI as sg
import os 




#ui.Window(title="Hello World", layout=[[]], margins=(1000, 1000)).read()


import PySimpleGUI as sg

sg.theme('Black')   # Add a touch of color
# All the stuff inside your window.

ticker = "NUE"
date = "2/10/23"
setup = "EP"

#[sg.Text('Next'), sg.InputText()],

layout = [  [sg.Text(ticker)],
          [sg.Text(date)],
          [sg.Text(setup)],
            
          [sg.Button('Prev'), sg.Button('Next')] ]

# Create the Window
window = sg.Window('Window Title', layout,margins = (1000,500))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Next': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()



