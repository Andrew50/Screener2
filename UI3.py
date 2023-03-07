from cmath import isnan
from re import L
import PySimpleGUI as sg
import os 
import pandas as pd
import pathlib
import mplfinance as mpf
from PIL import Image
import io
import datetime
import math
import multiprocessing
from time import sleep
from Datav4 import Data as data
import time as ttime
import shutil
import concurrent.futures
from pathos.multiprocessing import ProcessingPool as Pool




class UI:

    

    def loop(self,current):
        if os.path.exists("C:/Screener/tmp/charts"):
            shutil.rmtree("C:/Screener/tmp/charts")
        os.mkdir("C:/Screener/tmp/charts")
        self.i = 0
        self.annotation = False
        if current:
            self.setups_data =pd.read_csv(r"C:\Screener\tmp\todays_setups.csv", header = None)
            self.historical = False
    
        else:
            self.setups_data =pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
            self.historical = True

            

        self.sort = False
        self.preloadamount = 6
        self.preloadbuffer = self.preloadamount - 1
        self.preload(self,True)
        self.update(self,True,None,0)
        while True:
            
            event, values = self.window.read()


            if event == 'Next': 
                if self.i < len(self.setups_data) - 1:
                    previ = self.i
                    self.i += 1
                   
                    self.update(self,False,values,previ)
                    self.window.refresh()
                    self.preload(self,False)
                    

            if event == 'Prev':
                
                if self.i > 0:
                    previ = self.i
                    self.i -= 1
                   
                    self.update(self,False,values,previ)
    
            if event == 'Load':
                ticker = values["input-ticker"]
                date = values["input-date"]
                setup = values["input-setup"]
                keyword = values["input-keyword"]
                previ = 0
                #print(previ)
                
                sortinput = values["input-trait"]
                self.lookup(self,ticker,date,setup,keyword,sortinput)
                self.update(self,False,values,previ)
           

            if event == 'Sort' and False:

                if self.sort:
                    self.sort = False
                else:
                    self.sort = True
                ticker = values["input-ticker"]
                date = values["input-date"]
                setup = values["input-setup"]
                keyword = values["input-keyword"]
                
                previ = 0
                #print(previ)
                sortinput = values["input-trait"]
                self.lookup(self,ticker,date,setup,keyword,sortinput)
                self.update(self,False,values,previ)
                
            if event == 'Toggle':
                previ = self.i
                if self.annotation:
                    try:
                        self.annotation = False
                        
                        ticker = values["input-ticker"]
                        date = values["input-date"]
                        setup = values["input-setup"]
                        keyword = values["input-keyword"]
                        sortinput = values["input-trait"]
                        self.lookup(self,ticker,date,setup,keyword,sortinput)
                        self.update(self,False,values,previ)
                    except pd.errors.EmptyDataError:
                        sg.Popup('No Setups Found')
   
                else:
                    try: 
                        
                        self.annotation = True
                       
                        ticker = values["input-ticker"]
                        date = values["input-date"]
                        setup = values["input-setup"]
                        keyword = values["input-keyword"]
                        sortinput = values["input-trait"]
                        self.lookup(self,ticker,date,setup,keyword,sortinput)
                        self.update(self,False,values,previ)
                    except pd.errors.EmptyDataError:
                        sg.Popup('No Setups Found')
    

            if event == sg.WIN_CLOSED:
                #self.update(self,False,values,self.i)
                break
            
        self.window.close()
    

    def lookup(self,ticker,date,setup,keyword,sortinput):
        
        print(f"searching for {keyword}")
        scan = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
        
        
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
        if keyword  != "":
            scanholder = pd.DataFrame()
            for k in range(len(scan)):
                if  str(keyword) in str(scan.iloc[k][12]) :
                    scanholder = pd.concat([scanholder,scan.iloc[[k]]])
            scan = scanholder
        if self.annotation:
            scanholder = pd.DataFrame()
            for k in range(len(scan)):
               
                if scan.iloc[k][12] !=  scan.iloc[k][12]: # == "" or scan.iloc[k][12] == None:
                    scanholder = pd.concat([scanholder,scan.iloc[[k]]])
            scan = scanholder
        
        if sortinput != "":
          
            idex = 0
            if sortinput == 'z':
                idex = 3
            if sortinput == 'gap':
                idex = 4
            if sortinput == 'adr':
                idex = 5
            if sortinput == 'vol':
                idex = 6
            #if sortinput == 'q':
               # idex = 7
            if sortinput == '1':
                idex = 8
            if sortinput == '2':
                idex = 9
            if sortinput == '3':
                idex = 10
            if sortinput == '10':
                idex = 11
            if sortinput == 'time':
                idex = 13


            if idex != 0:

                scan = scan.sort_values(by=[idex], ascending=False)

            else:
                sg.Popup('Not A Trait')

        else:
            scan = scan.sample(frac=1)

        if len(scan) < 1:
            sg.Popup('No Setups Found')
        else:
            
            self.i = 0
            self.setups_data = scan
            if os.path.exists("C:/Screener/tmp/charts"):
                shutil.rmtree("C:/Screener/tmp/charts")
            os.mkdir("C:/Screener/tmp/charts")
            self.preload(self, True)

            
           
    def plot(slist):
        i = slist[1]
        setups_data = slist[0]
        
        
        
        iss = str(i)
        if (os.path.exists("C:/Screener/tmp/charts/databasesmall" + iss + ".png") == False):
            print(f"fetching {i}")
            date = str(setups_data.iloc[i][0])
            ticker = str(setups_data.iloc[i][1])
            setup = str(setups_data.iloc[i][2])
            z= str(setups_data.iloc[i][3])
            zs = float(z)

            chartsize = 80
            chartsize2 = 80
            chartoffset = 20
            chartoffset2 = 20

            if(os.path.exists("C:/Screener/data_csvs/" + ticker + "_data.csv")):
                data_daily = pd.read_csv(r"C:/Screener/data_csvs/" + ticker + "_data.csv")
                dfw = data.toWeekly(data_daily)




                mc = mpf.make_marketcolors(up='g',down='r')
                s  = mpf.make_mpf_style(marketcolors=mc)
              

                index = data.findIndex(data_daily,date,False)
                rightedge = index + chartoffset


                
                

                rightedge2 = data.findWeeklyIndex(dfw,index) + chartoffset2

                
              

                leftedge = rightedge - chartsize
                leftedge2 = rightedge2 - chartsize2
                if leftedge2 < 0:
                    leftedge2 = 0
                
                string1 = "databasesmall" + iss + ".png"
                string2 = "databaselarge" + iss + ".png"
                #string3 = "databaseintraday" + iss + ".png"
                ourpath = pathlib.Path("C:/Screener/tmp/charts") / string1
                ourpath2 = pathlib.Path("C:/Screener/tmp/charts") / string2
                #ourpath3 = pathlib.Path("C:/Screener/tmp/charts") / string3
            
            

              

                data_daily['Datetime'] = pd.to_datetime(data_daily['Date'])
                data_daily = data_daily.set_index('Datetime')
                data_daily = data_daily.drop(['Date'], axis=1)

               
                dfw = dfw.set_index('Datetime')


                df = data_daily[(leftedge):(rightedge)]
                #df2 = data_daily[(leftedge2):(rightedge)]

                df2 = dfw[(leftedge2):(rightedge2)]

               
                if date == "0":
                    pmPrice = (setups_data.iloc[i][4])
                    mpf.plot(df, type='candle', volume=True, title=str(ticker + "   " + setup + "   " + str(round(zs,2))), style=s, savefig=ourpath, figratio = (32,18), mav=(10,20), tight_layout = True, hlines=dict(hlines=[pmPrice], alpha = .25))
                    mpf.plot(df2, type='candle', volume=True, style=s, savefig=ourpath2, figratio = (32,18), mav=(10,20), tight_layout = True, hlines=dict(hlines=[pmPrice], alpha = .25))
                else:


                    # dfintraday_full = pd.read_csv(r"C:/Screener/intraday_data/" + ticker + "_intradaydata.csv")

                    #dfintraday = intraday.findIndex(dfintraday_full,date)


                    try:
                    #print(df2)
                        mpf.plot(df, type='candle', volume=True, title=str(ticker + "   " + date + "   " + setup + "   " + str(round(zs,2))), style=s, savefig=ourpath, figratio = (32,18), mav=(10,20), tight_layout = True,vlines=dict(vlines=[date], alpha = .25))
                        mpf.plot(df2, type='candle', volume=True, style=s, savefig=ourpath2, figratio = (32,18), mav=(10,20), tight_layout = True,vlines=dict(vlines=[date], alpha = .25))
                        # mpf.plot(dfintraday, type='candle', volume=True, style=s, savefig=ourpath3, figratio = (32,18),  tight_layout = True )
                    except:
                       # mpf.plot(df, type='candle', volume=True, title=str(ticker + "   " + date + "   " + setup + "   " + str(round(zs,2))), style=s, savefig=ourpath, figratio = (32,18), mav=(10,20), tight_layout = True)
                       # mpf.plot(df2, type='candle', volume=True, style=s, savefig=ourpath2, figratio = (32,18), mav=(10,20), tight_layout = True)
                       
                        print("chart failed")
                
            

    
    def preload(self,init):
        arglist = []
        c = 0
        if not init:
            c = self.preloadbuffer
        for x in range(self.preloadamount - c):
        #for x in range(len(self.setups_data)):
            
            v = (x + self.i + c)
            if v < len(self.setups_data):
                arglist.append([self.setups_data,v])

        with Pool(nodes=6) as pool:
            pool.map(self.plot, arglist)
      
        
       
            
          

       


    

    def update(self, init,values,previ):
       
        
        lasttime = ttime.time()
        while True:
            laptime = round((ttime.time() - lasttime), 2)
            if laptime < 2:
                try:
                    image = Image.open(r"C:\Screener\tmp\charts\databasesmall" + str(self.i) + ".png")
                    #image.thumbnail((930, 570))
                    bio = io.BytesIO()
                    image.save(bio, format="PNG")
           
                    image2 = Image.open(r"C:\Screener\tmp\charts\databaselarge" + str(self.i) + ".png")
                   # image2.thumbnail((930, 570))
                    bio2 = io.BytesIO()
                    image2.save(bio2, format="PNG")
                    break

                except OSError:
                    pass
                
                except:
                    break
            else:
                print("image timed out")
                break
            
           
     

        if self.historical:
            gap = str(self.setups_data.iloc[self.i][4])
            adr = str(self.setups_data.iloc[self.i][5])
            vol = str(self.setups_data.iloc[self.i][6])
            q = str(self.setups_data.iloc[self.i][7])
            one = str(self.setups_data.iloc[self.i][8])
            two = str(self.setups_data.iloc[self.i][9])
            three = str(self.setups_data.iloc[self.i][10])
            ten = str(self.setups_data.iloc[self.i][11])
            annotation = str(self.setups_data.iloc[self.i][12])
            #rating = str(self.setups_data.iloc[self.i][13])
            time = str(self.setups_data.iloc[self.i][13])
                
            if annotation == "nan":
                annotation = ""
            #if rating == "nan":
                #rating = ""



            if init:
                histstr = "Historical"
                sg.theme('DarkGrey')
                layout = [  
                [sg.Image(bio.getvalue(),key = '-IMAGE-'),sg.Image(bio2.getvalue(),key = '-IMAGE2-')],

                [ (sg.Text("gap")),(sg.Text(gap, key = '-gap-')),
                (sg.Text("|   adr")),(sg.Text(adr, key = '-adr-')),
                (sg.Text("|   vol")),(sg.Text(vol, key = '-vol-')),
                (sg.Text("|   q")),(sg.Text(q, key = '-q-')),
                (sg.Text("|   1")),(sg.Text(one, key = '-one-')),
                (sg.Text("|   2")),(sg.Text(two, key = '-two-')),
                (sg.Text("|   3")),(sg.Text(three, key = '-three-')),
                (sg.Text("|   10")),(sg.Text(ten, key = '-ten-')),
                (sg.Text("|   time")),(sg.Text(time, key = '-time-'))],
                 #[(sg.Text("Rating ")),sg.InputText(rating,key = 'rating')],
                [sg.Multiline(annotation,size=(150, 5), key='annotation')],
                
               
                [(sg.Text("Ticker    ")),sg.InputText(key = 'input-ticker')],
                [(sg.Text("Date      ")),sg.InputText(key = 'input-date')],
                [(sg.Text("Setup    ")),sg.InputText(key = 'input-setup')],
                [(sg.Text("Keyword")),sg.InputText(key = 'input-keyword')],
                [(sg.Text("Trait      ")),sg.InputText(key = 'input-trait')],
                [(sg.Text((str(f"{self.i + 1} of {len(self.setups_data)}")), key = '-number-'))],
                #[(sg.Text("Gap")),(sg.Text(gap, key = '-gap-'))] , 
                #[(sg.Text("ADR")),(sg.Text(adr, key = '-adr-'))] , 
                #[(sg.Text("Vol")),(sg.Text(vol, key = '-vol-'))] , 
                #[(sg.Text("QQQ")),(sg.Text(q, key = '-q-'))] , 
                #[(sg.Text("One")),(sg.Text(one, key = '-one-'))] , 
                #[(sg.Text("Two")),(sg.Text(two, key = '-two-'))] , 
                #[(sg.Text("Three")),(sg.Text(three, key = '-three-'))] , 
                #[(sg.Text("Ten")),(sg.Text(ten, key = '-ten-'))] ,
                #[(sg.Text("Time")),(sg.Text(time, key = '-time-'))] , 
                [sg.Button('Prev'), sg.Button('Next'),sg.Button('Load'), sg.Button('Toggle')]#, sg.Button('Sort')] 
                ]
                
                self.window = sg.Window('Screener', layout,margins = (10,10))
            else:
               
                df = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
                
                index = self.setups_data.index[previ]
                  
                print('saved annotation')
              
                df.at[index, 12] = values["annotation"]
                self.setups_data.at[index, 12] = values["annotation"]
                   
                    
                df.to_csv(r"C:\Screener\tmp\setups.csv",header = False, index = False)
                
                
                    
                self.window['-number-'].update(str(f"{self.i + 1} of {len(self.setups_data)}"))
                self.window["-gap-"].update(gap)
                self.window["-adr-"].update(adr)
                self.window["-vol-"].update(vol)
                self.window["-q-"].update(q)
                self.window["-one-"].update(one)
                self.window["-two-"].update(two)
                self.window["-three-"].update(three)
                self.window["-ten-"].update(ten)
                self.window["-time-"].update(time)
                self.window["annotation"].update(annotation)
                #self.window["rating"].update(rating)
                try:

                    self.window["-IMAGE-"].update(data=bio.getvalue())
                    self.window["-IMAGE2-"].update(data=bio2.getvalue())
                except:
                    print("image load failed")
                    
                
                    

        else:
            if init:
                sg.theme('DarkGrey')
                histstr = "Current"
                
                layout = [  
                [sg.Image(bio.getvalue(),key = '-IMAGE-'),sg.Image(bio2.getvalue(),key = '-IMAGE2-')],
              
                    
                [(sg.Text((str(f"{self.i + 1} of {len(self.setups_data)}")), key = '-number-'))],
                   
                        [sg.Button('Prev'), sg.Button('Next')] 
                ]


                
                self.window = sg.Window('Window Title', layout,margins = (10,10))


            else:
                self.window["-IMAGE-"].update(data=bio.getvalue())
                self.window["-IMAGE2-"].update(data=bio2.getvalue())
                self.window['-number-'].update(str(f"{self.i + 1} of {len(self.setups_data)}"))
           

if __name__ == "__main__":
    
  
    UI.loop(UI,False)

