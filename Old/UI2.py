import PySimpleGUI as sg
import os 
import pandas as pd
import pathlib
import mplfinance as mpf
from PIL import Image
import datetime
import io
from multiprocessing import Process, Queue
import multiprocessing as mp
from time import sleep
import concreent.futures




#ui.Window(title="Hello World", layout=[[]], margins=(1000, 1000)).read()

class UI:

    def preload(q):
        
        

        ip = q.get(0)
        preloadamount = q.get(1)
        images = q.get(2)
        setups_data = q.get(3)
        
        if len(images) < preloadamount * 2:

            print("preloading")
            # needs self.i    self.setups_data   self.images        self.preloadamount
            i = ip + int(len(images)/2)


            date = str(setups_data.iloc[i][0])
            ticker = str(setups_data.iloc[i][1])
            setup = str(setups_data.iloc[i][2])
            z= str(setups_data.iloc[i][3])
            zs = float(z)
            #self.window['-setup-'].update(str(self.setups_data.iloc[self.i][2]))
            #self.window['-ticker-'].update(str(self.setups_data.iloc[self.i][1]))
            #self.window['-date-'].update(str(self.setups_data.iloc[self.i][0]))
       
            chartsize = 80
            chartsize2 = 500
            chartoffset = 20



            if(os.path.exists("C:/Screener/data_csvs/" + ticker + "_data.csv")):
                data_daily = pd.read_csv(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
                rightedge = sfindIndex(data_daily,date) + chartoffset
                leftedge = rightedge - chartsize
                leftedge2 = rightedge - chartsize2

                if leftedge2 < 0:
                    leftedge2 = 0

                data_daily['Datetime'] = pd.to_datetime(data_daily['datetime'])
                data_daily = data_daily.set_index('Datetime')
                data_daily = data_daily.drop(['datetime'], axis=1)
            
                mc = mpf.make_marketcolors(up='g',down='r')
                s  = mpf.make_mpf_style(marketcolors=mc)
        

                df = data_daily[(leftedge):(rightedge)]
                df2 = data_daily[(leftedge2):(rightedge)]
            
                ourpath = pathlib.Path("C:/Screener/tmp") / "databaseimage.png"
                ourpath2 = pathlib.Path("C:/Screener/tmp") / "databaseimage2.png"
                if date == "0":
                    pmPrice = (setups_data.iloc[i][4])
                    mpf.plot(df, type='candle', volume=True, title=str(ticker + "  " + date + "  " + setup + "  " + str(round(zs,2))), style=s, savefig=ourpath, figratio = (32,18), mav=(10,20), tight_layout = True, hlines=dict(hlines=[pmPrice], alpha = .25))
                    mpf.plot(df2, type='candle', volume=True, style=s, savefig=ourpath2, figratio = (32,18), mav=(10,20), tight_layout = True, hlines=dict(hlines=[pmPrice], alpha = .25))
                else:
                    mpf.plot(df, type='candle', volume=True, title=str(ticker + "  " + date + "  " + setup + "  " + str(round(zs,2))), style=s, savefig=ourpath, figratio = (32,18), mav=(10,20), tight_layout = True,vlines=dict(vlines=[date], alpha = .25))
                    mpf.plot(df2, type='candle', volume=True, style=s, savefig=ourpath2, figratio = (32,18), mav=(10,20), tight_layout = True,vlines=dict(vlines=[date], alpha = .25))

                image = Image.open(r"C:\Screener\tmp\databaseimage.png")
                image.thumbnail((3500, 2000))
                bio = io.BytesIO()
                image.save(bio, format="PNG")

                image2 = Image.open(r"C:\Screener\tmp\databaseimage2.png")
                image2.thumbnail((3500, 2000))
                bio2 = io.BytesIO()
                image2.save(bio2, format="PNG")

                images.append(bio)
                images.append(bio2)
                q.put([ip,preloadamount,images,setups_data])
                

        else:
            print("donepreloading")


    def loop(self):
        self.i = -1
        self.full_setups_data = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
        self.setups_data = self.full_setups_data
        historical = True
        self.preloadamount = 5
        self.images = []

        i = mp.value('i',-1)
        preloadamount = mp.value('i',5)

        
        mp.set_start_method('spawn')

        p = mp.Pool(initializer=init, initargs=(i, v))
        self.q.put([self.i,self.preloadamount,self.images,self.setups_data])
        
        self.lookup(self,"","","")
       
    
        
        p = Process(target=self.preload, args=(self.q,))
        
        p.start()
        print("2")
       
        #sleep(10)
        

        self.update(self,True)

        
        
        
        while True:
            event, values = self.window.read()
            print('working')
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
                
            if event == 'Toggle':
                if historical:
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
                        self.images.clear() #####################
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
                        self.images.clear() ################
                    except pd.errors.EmptyDataError:
                        sg.Popup('No Setups Found')

            
            self.qpush(self)

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
            
            self.i = -1
            self.setups_data = scan
            self.images.clear() #####################
            self.qpush(self)



    def qpush(self):
        self.q.put([self.i,self.preloadamount,self.images,self.setups_data])

    def qpull(self):
        self.images = self.q[3]


    def update(self, init):
        self.qpush(self)
        
        print("3")
        while len(self.images) < 2:
            self.qpull(self)
        #(self.images)

        if init:
            
            layout = [  
            [sg.Image(self.images[0].getvalue(),key = '-IMAGE-'),sg.Image(self.images[1].getvalue(),key = '-IMAGE2-')],
            #[(sg.Text(ticker,key = '-ticker-')), (sg.Text(date, key = '-date-')),(sg.Text(setup,key = '-setup-'))],
            [(sg.Text("Historical", key = "-hist-"))],
            [(sg.Text((str(f"{self.i + 2} of {len(self.setups_data)}")), key = '-number-'))],
            [(sg.Text("Ticker")),sg.InputText(key = 'input-ticker')],
            [(sg.Text("Date")),sg.InputText(key = 'input-date')],
            [(sg.Text("Setup")),sg.InputText(key = 'input-setup')],
                    [sg.Button('Prev'), sg.Button('Next'),sg.Button('Load'), sg.Button('Toggle')] 
            ]
            sg.theme('DarkBlack')
            self.window = sg.Window('Window Title', layout,margins = (10,10))
        else:
            self.qpull(self)
            self.images.pop(0)
            self.images.pop(0)
            self.qpush(self)
           
            self.window["-IMAGE-"].update(self.images[0].getvalue())
            self.window["-IMAGE2-"].update(self.images[1].getvalue())
            self.window['-number-'].update(str(f"{self.i + 2} of {len(self.setups_data)}"))
            
            
            
    def sfindIndex(df, dateTo):
        if dateTo == "0":
            return len(df)
        lookforSplit = dateTo.split("-")
        middle = int(len(df)/2)
        middleDTOD = str(df.iloc[middle]['datetime'])
        middleSplit = middleDTOD.split("-")      
        yearDifference = int(middleSplit[0]) - int(lookforSplit[0])
        monthDifference = int(middleSplit[1]) - int(lookforSplit[1])
        if(monthDifference < 0):
            yearDifference = yearDifference + 1
            monthDifference = -12 + monthDifference
        addInt = (yearDifference*-252) + (monthDifference*-21)
        newRef = middle + addInt
        dateTo = dateTo + " 05:30:00"
        if(newRef < 0):
            return 99999
        if( ((len(df) - newRef) < 20) or (newRef > len(df))):
            for i in range(35):
                dateTimeofDayAhead = str(df.iloc[len(df)-35 + i]['datetime'])
                if(dateTimeofDayAhead == dateTo):
                    return int(len(df) - 35 + i)
        else:
            for i in range(35):
                dateTimeofDayBehind = str(df.iloc[newRef - i]['datetime'])
                if(dateTimeofDayBehind == dateTo):
                    return (newRef - i)
                dateTimeofDayAhead = str(df.iloc[newRef + i]['datetime'])
                if(dateTimeofDayAhead == dateTo):
                    return (newRef + i)
        return 99999

if __name__ == "__main__":
    UI.loop(UI)
