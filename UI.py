import PySimpleGUI as sg
import os 
import pandas as pd
import pathlib
import mplfinance as mpf
from PIL import Image
import io




#ui.Window(title="Hello World", layout=[[]], margins=(1000, 1000)).read()

class UI:

    

    def loop(self):
        self.i = 0
        setups_data = pd.read_csv(r"C:\Screener\tmp\copy of setups.csv", header = None)
        date = str(setups_data.iloc[self.i][0])
        ticker = str(setups_data.iloc[self.i][1])
        setup = str(setups_data.iloc[self.i][2])
        layout = [  
            [sg.Image(key = '-IMAGE-')],
            [(sg.Text(ticker,key = '-ticker-')), (sg.Text(date, key = '-date-')),(sg.Text(setup,key = '-setup-'))],
            [(sg.Text("x", key = '-number-'))],
            [(sg.Text("Ticker")),sg.InputText(key = 'input-ticker')],
            [(sg.Text("Date")),sg.InputText(key = 'input-date')],
            [(sg.Text("Setup")),sg.InputText(key = 'input-setup')],
                  [sg.Button('Prev'), sg.Button('Next')] 
            ]

        # Create the Window
        sg.theme('DarkBlack')
        self.window = sg.Window('Window Title', layout,margins = (10,10))
        # Event Loop to process "events" and get the "values" of the inputs
        event, values = self.window.read()
        self.chart(self)
        while True:
            event, values = self.window.read()
            if event == 'Next': # if user closes window or clicks cancel
                self.i += 1
                self.chart(self)
                
                
            if event == 'Prev':
                self.i -= 1
                self.chart(self)


            if event == sg.WIN_CLOSED:
                break
            
        self.window.close()
        

    def chart(self):

        setups_data = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
        date = str(setups_data.iloc[self.i][0])
        ticker = str(setups_data.iloc[self.i][1])
        setup = str(setups_data.iloc[self.i][2])
        self.window['-setup-'].update(str(setups_data.iloc[self.i][2]))
        self.window['-ticker-'].update(str(setups_data.iloc[self.i][1]))
        self.window['-date-'].update(str(setups_data.iloc[self.i][0]))
        self.window['-number-'].update(str(f"{self.i + 2} of {len(setups_data)}"))
        chartsize = 80
        chartoffset = 20


        if(os.path.exists("C:/Screener/data_csvs/" + ticker + "_data.csv")):
            data_daily = pd.read_csv(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
            rightedge = self.sfindIndex(data_daily,date) + chartoffset
            leftedge = rightedge - chartsize
            
            data_daily['Datetime'] = pd.to_datetime(data_daily['datetime'])
            data_daily = data_daily.set_index('Datetime')
            data_daily = data_daily.drop(['datetime'], axis=1)
            
            mc = mpf.make_marketcolors(up='g',down='r')
            s  = mpf.make_mpf_style(marketcolors=mc)
        

            df = data_daily[(leftedge):(rightedge)]
            
            ourpath = pathlib.Path("C:/Screener/tmp") / "databaseimage.png"
            mpf.plot(df, type='candle', volume=True, title=ticker, style=s, savefig=ourpath)

            image = Image.open(r"C:\Screener\tmp\databaseimage.png")
            image.thumbnail((3500, 2000))
            bio = io.BytesIO()
            # Actually store the image in memory in binary 
            image.save(bio, format="PNG")
            # Use that image data in order to 
            self.window["-IMAGE-"].update(data=bio.getvalue())

            
        
    def sfindIndex(df, dateTo):
        if dateTo == "0":
            return len(df)
        for i in range(len(df)):
            dateTimeOfDay = df.iloc[i]['datetime']
            dateSplit = str(dateTimeOfDay).split(" ")
            date = dateSplit[0]
            if(date == dateTo):
                return i
        return 99999

if __name__ == "__main__":
    UI.loop(UI)


