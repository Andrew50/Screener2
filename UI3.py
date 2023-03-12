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
from Data5 import Data as data
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
                timeframe = values['input-timeframe']
                ticker = values["input-ticker"]
                date = values["input-date"]
                setup = values["input-setup"]
                keyword = values["input-keyword"]
                previ = 0
                #print(previ)
                
                sortinput = values["input-trait"]
                self.lookup(self,ticker,date,setup,keyword,sortinput,timeframe)
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
                        timeframe = values['input-timeframe']
                        ticker = values["input-ticker"]
                        date = values["input-date"]
                        setup = values["input-setup"]
                        keyword = values["input-keyword"]
                        sortinput = values["input-trait"]
                        self.lookup(self,ticker,date,setup,keyword,sortinput,timeframe)
                        self.update(self,False,values,previ)
                    except pd.errors.EmptyDataError:
                        sg.Popup('No Setups Found')
   
                else:
                    try: 
                        
                        self.annotation = True
                        timeframe = values['input-timeframe']
                        ticker = values["input-ticker"]
                        date = values["input-date"]
                        setup = values["input-setup"]
                        keyword = values["input-keyword"]
                        sortinput = values["input-trait"]
                        self.lookup(self,ticker,date,setup,keyword,sortinput,timeframe)
                        self.update(self,False,values,previ)
                    except pd.errors.EmptyDataError:
                        sg.Popup('No Setups Found')
    

            if event == sg.WIN_CLOSED:
                #self.update(self,False,values,self.i)
                break
            
        self.window.close()
    

    def lookup(self,ticker,date,setup,keyword,sortinput,timeframe):
        
        print(f"searching for {keyword}")
        scan = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)
        
        if timeframe  != "":
            scanholder = pd.DataFrame()
            for k in range(len(scan)):
                if scan.iloc[k][14] == timeframe:
                    scanholder = pd.concat([scanholder,scan.iloc[[k]]])
            scan = scanholder
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
            mc = mpf.make_marketcolors(up='g',down='r')
            s  = mpf.make_mpf_style(marketcolors=mc)
            chartdate = str(setups_data.iloc[i][0])
            date = datetime.datetime.strptime(chartdate, '%Y-%m-%d')
            ticker = str(setups_data.iloc[i][1])
            setup = str(setups_data.iloc[i][2])
            z= str(setups_data.iloc[i][3])
            zs = float(z)

            chartsize = 80
            chartoffset = 60
            chartoffset2 = 10
            chartoffset3 = 50

            df1 = data.get(ticker,'w')
            df2 = data.get(ticker,'d')
            df3 = data.get(ticker,'h')
            df4 = data.get(ticker,'1min')


            l1 = data.findex(df1,date) - chartoffset
            l2 = data.findex(df2,date) - chartoffset
            l3 = data.findex(df3,date) - chartoffset3
            l4 = data.findex(df4,date) - chartoffset2

            r1 = l1 + chartsize
            r2 = l2 + chartsize
            r3 = l3 + chartsize
            r4 = l4 + chartsize

            if l1 < 0:
                l1 = 0
            if l2 < 0:
                l2 = 0
            if l3 < 0:
                l3 = 0
            if l4 < 0:
                l4 = 0
           


            df1 = df1[l1:r1]
            df2 = df2[l2:r2]
            df3 = df3[l3:r3]
            df4 = df4[l4:r4]

            df1.set_index('datetime', inplace = True)
            df2.set_index('datetime', inplace = True)
            df3.set_index('datetime', inplace = True)
            df4.set_index('datetime', inplace = True)
            

            string1 = "1" + iss + ".png"
            string2 = "2" + iss + ".png"
            string3 = "3" + iss + ".png"
            string4 = "4" + iss + ".png"
            

            p1 = pathlib.Path("C:/Screener/tmp/charts") / string1
            p2 = pathlib.Path("C:/Screener/tmp/charts") / string2
            p3 = pathlib.Path("C:/Screener/tmp/charts") / string3
            p4 = pathlib.Path("C:/Screener/tmp/charts") / string4
            
         

            if date == "0":
                pmPrice = (setups_data.iloc[i][4])
                mpf.plot(df1, type='candle', volume=True, title=str(ticker + "   " + setup + "   " + str(round(zs,2))), style=s, savefig=p1, figratio = (32,14), mav=(10,20), tight_layout = True, hlines=dict(hlines=[pmPrice], alpha = .25))
                mpf.plot(df2, type='candle', volume=True, style=s, title=str('Daily'), savefig=p2, figratio = (32,14), mav=(10,20), tight_layout = True, hlines=dict(hlines=[pmPrice], alpha = .25))
                mpf.plot(df3, type='candle', volume=True, style=s, title=str('Hourly'), savefig=p3, figratio = (32,14), mav=(10,20), tight_layout = True, hlines=dict(hlines=[pmPrice], alpha = .25))
                mpf.plot(df4, type='candle', volume=True, style=s, title=str('1 Minute'), savefig=p4, figratio = (32,14), mav=(10,20), tight_layout = True, hlines=dict(hlines=[pmPrice], alpha = .25))
            else:

                mpf.plot(df1, type='candle', volume=True, title=str(ticker + "   " + chartdate + "   " + setup + "   " + str(round(zs,2))), style=s, savefig=p1, figratio = (32,14), mav=(10,20), tight_layout = True,vlines=dict(vlines=[chartdate], alpha = .25))
                mpf.plot(df2, type='candle', volume=True, style=s, title=str('Daily'), savefig=p2, figratio = (32,14), mav=(10,20), tight_layout = True,vlines=dict(vlines=[chartdate], alpha = .25))
                mpf.plot(df3, type='candle', volume=True, style=s, title=str('Hourly'), savefig=p3, figratio = (32,14), mav=(10,20), tight_layout = True,vlines=dict(vlines=[chartdate], alpha = .25))
                mpf.plot(df4, type='candle', volume=True, style=s, title=str('1 Minute'), savefig=p4, figratio = (32,14), mav=(10,20), tight_layout = True,vlines=dict(vlines=[chartdate], alpha = .25))
                    
                       
        
                
            

    
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
            if laptime < 3:

                


                try:
                    image1 = Image.open(r"C:\Screener\tmp\charts\1" + str(self.i) + ".png")
                    image1.thumbnail((1050, 700))
                    bio1 = io.BytesIO()
                    image1.save(bio1, format="PNG")
           
                    image2 = Image.open(r"C:\Screener\tmp\charts\2" + str(self.i) + ".png")
                    image2.thumbnail((1050, 700))
                    bio2 = io.BytesIO()
                    image2.save(bio2, format="PNG")

                    image3 = Image.open(r"C:\Screener\tmp\charts\3" + str(self.i) + ".png")
                    image3.thumbnail((1050, 700))
                    bio3 = io.BytesIO()
                    image3.save(bio3, format="PNG")

                    image4 = Image.open(r"C:\Screener\tmp\charts\4" + str(self.i) + ".png")
                    image4.thumbnail((1050, 700))
                    bio4 = io.BytesIO()
                    image4.save(bio4, format="PNG")

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
                [sg.Image(bio1.getvalue(),key = '-IMAGE-'),sg.Image(bio2.getvalue(),key = '-IMAGE2-')],
                [sg.Image(bio3.getvalue(),key = '-IMAGE3-'),sg.Image(bio4.getvalue(),key = '-IMAGE4-')],

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
                
                [(sg.Text("Timeframe")),sg.InputText(key = 'input-timeframe')],
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

                    self.window["-IMAGE-"].update(data=bio1.getvalue())
                    self.window["-IMAGE2-"].update(data=bio2.getvalue())
                    self.window["-IMAGE3-"].update(data=bio3.getvalue())
                    self.window["-IMAGE4-"].update(data=bio4.getvalue())
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

