import PySimpleGUI as sg
import os 
import pandas as pd
import pathlib
import mplfinance as mpf
from PIL import Image
import io
import datetime
import multiprocessing
from time import sleep
from Datav4 import Data as data
import shutil




#ui.Window(title="Hello World", layout=[[]], margins=(1000, 1000)).read()

class UI:

    

    def loop(self,current):
        if os.path.exists("C:/Screener/tmp/charts"):
            shutil.rmtree("C:/Screener/tmp/charts")
        os.mkdir("C:/Screener/tmp/charts")
        self.i = 0
        if current:
        
            self.full_setups_data =pd.read_csv(r"C:\Screener\tmp\todays_setups.csv", header = None)
            self.historical = False
    
        else:
            self.full_setups_data =pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
            self.historical = True

        self.setups_data = self.full_setups_data
        
        
        self.preloadamount = 10
        self.preloadbuffer = self.preloadamount - 1

        self.preload(self,True)

       
        
       
        
        self.update(self,True)


        timepreload = False
        
        while True:
            event, values = self.window.read()
            if event == 'Next': # if user closes window or clicks cancel
                if self.i < len(self.setups_data) - 1:
                    self.i += 1
                    self.update(self,False)
                    timepreload = True
                    
                    
                
                
            if event == 'Prev':
                if self.i > 0:
                    self.i -= 1
                    self.update(self,False)
                    timepreaload = True
                    
            if event == 'Load':
                ticker = values["input-ticker"]
                date = values["input-date"]
                setup = values["input-setup"]
                self.lookup(self,ticker,date,setup)
                self.update(self,False)
                timepreload = True
               

            if timepreload:
                self.preload(self,False)
                timepreload = False
                
            if event == 'Toggle':
                if self.historical:
                    try:
                        holder = pd.read_csv(r"C:\Screener\tmp\todays_setups.csv", header = None)
                        self.full_setups_data  = holder
                        historical = False
                        self.window["-hist-"].update('Today')
                        ticker = values["input-ticker"]
                        date = values["input-date"]
                        setup = values["input-setup"]
                        self.lookup(self,ticker,date,setup)
                        self.update(self,False)
                    except pd.errors.EmptyDataError:
                        sg.Popup('No Setups Found')
   
                else:
                    try: 
                        holder = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
                        self.full_setups_data  = holder
                        historical = True
                        self.window["-hist-"].update('Historical')
                        ticker = values["input-ticker"]
                        date = values["input-date"]
                        setup = values["input-setup"]
                        self.lookup(self,ticker,date,setup)
                        self.update(self,False)
                    except pd.errors.EmptyDataError:
                        sg.Popup('No Setups Found')
                   
                        
                
                


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
        
  

        if len(scan) < 1:
            sg.Popup('No Setups Found')
        else:
            
            self.i = 0
            self.setups_data = scan
            if os.path.exists("C:/Screener/tmp/charts"):
                shutil.rmtree("C:/Screener/tmp/charts")
            os.mkdir("C:/Screener/tmp/charts")
            self.preload(self, True)
           

    
    def preload(self,init):
        c = 0
        if not init:
            c = self.preloadbuffer
            
        for x in range(self.preloadamount - c):
            
            v = (x + self.i + c)
            
            p = multiprocessing.Process(target = self.plot, args = [self.setups_data,v])

            p.start()

       


    def plot(setups_data, i):

        
        
        iss = str(i)
        if (os.path.exists("C:/Screener/tmp/charts/databasesmall" + iss + ".png") == False):
            print(f"fetching {i}")
            date = str(setups_data.iloc[i][0])
            ticker = str(setups_data.iloc[i][1])
            setup = str(setups_data.iloc[i][2])
            z= str(setups_data.iloc[i][3])
            zs = float(z)

            chartsize = 80
            chartsize2 = 500
            chartoffset = 20

            if(os.path.exists("C:/Screener/data_csvs/" + ticker + "_data.csv")):
                data_daily = pd.read_csv(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
                mc = mpf.make_marketcolors(up='g',down='r')
                s  = mpf.make_mpf_style(marketcolors=mc)
                #print(date)
                rightedge = data.findIndex(data_daily,date,False) + chartoffset
                leftedge = rightedge - chartsize
                leftedge2 = rightedge - chartsize2
                if leftedge2 < 0:
                    leftedge2 = 0
                
                string1 = "databasesmall" + iss + ".png"
                string2 = "databaselarge" + iss + ".png"
                ourpath = pathlib.Path("C:/Screener/tmp/charts") / string1
                ourpath2 = pathlib.Path("C:/Screener/tmp/charts") / string2
            
            
                data_daily['Datetime'] = pd.to_datetime(data_daily['Date'])
                data_daily = data_daily.set_index('Datetime')
                data_daily = data_daily.drop(['Date'], axis=1)
                df = data_daily[(leftedge):(rightedge)]
                df2 = data_daily[(leftedge2):(rightedge)]


                if date == "0":
                    pmPrice = (setups_data.iloc[i][4])
                    mpf.plot(df, type='candle', volume=True, title=str(ticker + "   " + setup + "   " + str(round(zs,2))), style=s, savefig=ourpath, figratio = (32,18), mav=(10,20), tight_layout = True, hlines=dict(hlines=[pmPrice], alpha = .25))
                    mpf.plot(df2, type='candle', volume=True, style=s, savefig=ourpath2, figratio = (32,18), mav=(10,20), tight_layout = True, hlines=dict(hlines=[pmPrice], alpha = .25))
                else:
                    mpf.plot(df, type='candle', volume=True, title=str(ticker + "   " + date + "   " + setup + "   " + str(round(zs,2))), style=s, savefig=ourpath, figratio = (32,18), mav=(10,20), tight_layout = True,vlines=dict(vlines=[date], alpha = .25))
                    mpf.plot(df2, type='candle', volume=True, style=s, savefig=ourpath2, figratio = (32,18), mav=(10,20), tight_layout = True,vlines=dict(vlines=[date], alpha = .25))



    def update(self, init):
       

        #print(datetime.datetime.now())
        
        date = str(self.setups_data.iloc[self.i][0])
        ticker = str(self.setups_data.iloc[self.i][1])
        setup = str(self.setups_data.iloc[self.i][2])
        z= str(self.setups_data.iloc[self.i][3])
        zs = float(z)
        #self.window['-setup-'].update(str(self.setups_data.iloc[self.i][2]))
        #self.window['-ticker-'].update(str(self.setups_data.iloc[self.i][1]))
        #self.window['-date-'].update(str(self.setups_data.iloc[self.i][0]))
       
        
        #print(datetime.datetime.now())

        if(os.path.exists("C:/Screener/data_csvs/" + ticker + "_data.csv")):
        
            

            
            #print(datetime.datetime.now())
            

           
           

            while True:
                try:
                    image = Image.open(r"C:\Screener\tmp\charts\databasesmall" + str(self.i) + ".png")
                    image.thumbnail((3500, 2000))
                    bio = io.BytesIO()
                    image.save(bio, format="PNG")
           
                    image2 = Image.open(r"C:\Screener\tmp\charts\databaselarge" + str(self.i) + ".png")
                    image2.thumbnail((3500, 2000))
                    bio2 = io.BytesIO()
                    image2.save(bio2, format="PNG")
                    break
                except OSError:
                    pass
           
            
            if init:
                if self.historical:
                    histstr = "Historical"
                else:
                    histstr = "Current"
                
                layout = [  
                [sg.Image(bio.getvalue(),key = '-IMAGE-'),sg.Image(bio2.getvalue(),key = '-IMAGE2-')],
                #[(sg.Text(ticker,key = '-ticker-')), (sg.Text(date, key = '-date-')),(sg.Text(setup,key = '-setup-'))],
                [(sg.Text(histstr, key = "-hist-"))],
                [(sg.Text((str(f"{self.i + 1} of {len(self.setups_data)}")), key = '-number-'))],
                [(sg.Text("Ticker")),sg.InputText(key = 'input-ticker')],
                [(sg.Text("Date")),sg.InputText(key = 'input-date')],
                [(sg.Text("Setup")),sg.InputText(key = 'input-setup')],
                      [sg.Button('Prev'), sg.Button('Next'),sg.Button('Load'), sg.Button('Toggle')] 
                ]
                sg.theme('DarkBlack')
                self.window = sg.Window('Window Title', layout,margins = (10,10))
            else:
                self.window["-IMAGE-"].update(data=bio.getvalue())
                self.window["-IMAGE2-"].update(data=bio2.getvalue())
                self.window['-number-'].update(str(f"{self.i + 1} of {len(self.setups_data)}"))

           # print(datetime.datetime.now())
           # print("dddddddddddddddddddddddddddddddddddddddddd")
            
    

if __name__ == "__main__":
    
    


    UI.loop(UI,True)

