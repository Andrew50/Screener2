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
        self.i = -1
        self.full_setups_data = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
        self.setups_data = self.full_setups_data
        

        self.update(self,True)


        
       
        while True:
            event, values = self.window.read()
            if event == 'Next': # if user closes window or clicks cancel
                if self.i < len(self.setups_data) - 2:
                    self.i += 1
                    self.update(self,False)
                
                
            if event == 'Prev':
                if self.i > -1:
                    self.i -= 1
                    self.update(self,False)
            if event == 'Load':
                ticker = values["input-ticker"]
                date = values["input-date"]
                setup = values["input-setup"]
                self.lookup(self,ticker,date,setup)
                self.update(self,False)
                

            if event == sg.WIN_CLOSED:
                break
            
        self.window.close()
    

    def lookup(self,ticker,date,setup):
        
      
        scan = self.full_setups_data
        
        if ticker  != "":
            scanholder = pd.DataFrame()
            for k in range(len(scan)):
                if scan.iloc[k][1] == ticker:
                    scanholder = pd.concat([scanholder,scan.iloc[[k]]])
            scan = scanholder
        if date  != "":
            scanholder = pd.DataFrame()
            for k in range(len(scan)):
                if scan.iloc[k][0] == date:
                    scanholder = pd.concat([scanholder,scan.iloc[[k]]])
            scan = scanholder
        if setup  != "":
            scanholder = pd.DataFrame()
            for k in range(len(scan)):
                if scan.iloc[k][2] == setup:
                    scanholder = pd.concat([scanholder,scan.iloc[[k]]])
            scan = scanholder
        
       
       

        if len(scan) == 0:
            sg.Popup('No Setups Found')
        else:
            self.i = -1
            self.setups_data = scan


       


    def update(self, init):

        
        date = str(self.setups_data.iloc[self.i][0])
        ticker = str(self.setups_data.iloc[self.i][1])
        setup = str(self.setups_data.iloc[self.i][2])
        #self.window['-setup-'].update(str(self.setups_data.iloc[self.i][2]))
        #self.window['-ticker-'].update(str(self.setups_data.iloc[self.i][1]))
        #self.window['-date-'].update(str(self.setups_data.iloc[self.i][0]))
       
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
            mpf.plot(df, type='candle', volume=True, title=str(ticker + "  " + date + "  " + setup), style=s, savefig=ourpath, figratio = (32,18), mav=(10,20), tight_layout = True)

            image = Image.open(r"C:\Screener\tmp\databaseimage.png")
            image.thumbnail((3500, 2000))
            bio = io.BytesIO()
            # Actually store the image in memory in binary 
            image.save(bio, format="PNG")
            # Use that image data in order to 
            if init:
                
                layout = [  
                [sg.Image(bio.getvalue(),key = '-IMAGE-')],
                #[(sg.Text(ticker,key = '-ticker-')), (sg.Text(date, key = '-date-')),(sg.Text(setup,key = '-setup-'))],
                [(sg.Text((str(f"{self.i + 2} of {len(self.setups_data)}")), key = '-number-'))],
                [(sg.Text("Ticker")),sg.InputText(key = 'input-ticker')],
                [(sg.Text("Date")),sg.InputText(key = 'input-date')],
                [(sg.Text("Setup")),sg.InputText(key = 'input-setup')],
                      [sg.Button('Prev'), sg.Button('Next'),sg.Button('Load')] 
                ]
                sg.theme('DarkBlack')
                self.window = sg.Window('Window Title', layout,margins = (10,10))
            else:
                self.window["-IMAGE-"].update(data=bio.getvalue())
                self.window['-number-'].update(str(f"{self.i + 2} of {len(self.setups_data)}"))

            
        
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

