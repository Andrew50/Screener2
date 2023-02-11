import PySimpleGUI as sg
import os 
import pandas as pd
import pathlib




#ui.Window(title="Hello World", layout=[[]], margins=(1000, 1000)).read()

class UI:






    def display(self):

        setups_data = pd.read_csv(r"C:\Screener\tmp\copy of setups.csv", header = None)
        date = str(setups_data.iloc[0][0])
        ticker = str(setups_data.iloc[0][1])
        setup = str(setups_data.iloc[0][2])
        

        sg.theme('Black')  
        

       

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

    def pullData(ticker,date,setup):


        mpf.plot(df, type='candle', volume=True, title=tick, hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
        ourpath = pathlib.Path("C:/Screener/tmp") / "test.png"







if __name__ == "__main__":
    UI.display(UI)


