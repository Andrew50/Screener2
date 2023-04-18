

import PySimpleGUI as sg
import os 
import numpy
import pandas as pd
import pathlib
import mplfinance as mpf
from PIL import Image
from matplotlib import pyplot as plt
import io
import datetime


from Data7 import Data as data
import time as ttime
import shutil

from pathos.multiprocessing import ProcessingPool as Pool




class UI:

    

    def loop(self,current = False):
        if os.path.exists("C:/Screener/tmp/charts"):
            shutil.rmtree("C:/Screener/tmp/charts")
        os.mkdir("C:/Screener/tmp/charts")
        self.i = 0
        self.annotation = False
        try:
            if current:
                self.setups_data =pd.read_feather(r"C:\Screener\tmp\todays_setups.feather")
                self.historical = False
    
            else:
                self.setups_data =pd.read_feather(r"C:\Screener\tmp\setups.feather")
                self.historical = True

        except:
            print('There were no setups')
            exit()

        if len(self.setups_data ) == 0: 
            print('There were no setups')
            exit()

        
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
        scan = pd.read_feather(r"C:\Screener\tmp\setups.feather")

        #print(timeframe)
        #print(scan)
        if timeframe  != "":
            scanholder = pd.DataFrame()
            for k in range(len(scan)):
                if scan.iloc[k][4] == timeframe:
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
                if  str(keyword) in str(scan.iloc[k][13]) :
                    scanholder = pd.concat([scanholder,scan.iloc[[k]]])
            scan = scanholder
        if self.annotation:
            scanholder = pd.DataFrame()
            for k in range(len(scan)):
               
                if scan.iloc[k][13] !=  scan.iloc[k][13] or scan.iloc[k][13] != "": # == "" or scan.iloc[k][12] == None:
                    scanholder = pd.concat([scanholder,scan.iloc[[k]]])
            scan = scanholder
        
        if sortinput != "":
            print(scan)
            idex = 0
            if sortinput == 'z':
                idex = 'Z'
            if sortinput == 'gap':
                idex = 'gap'
            if sortinput == 'adr':
                idex = 'adr'
            if sortinput == 'vol':
                idex = 'vol'
            #if sortinput == 'q':
               # idex = 7
            if sortinput == '1':
                idex = '1'
            if sortinput == '2':
                idex = '2'
            if sortinput == '3':
                idex = '3'
            if sortinput == '10':
                idex = '10'
            if sortinput == 'time':
                idex = 'time'

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
        if (os.path.exists("C:/Screener/tmp/charts/1" + iss + ".png") == False):

            print(f'preloading {i}')
               
            mc = mpf.make_marketcolors(up='g',down='r')
            s  = mpf.make_mpf_style(marketcolors=mc)
            date = (setups_data.iloc[i][0])
           
            ticker = setups_data.iloc[i][1]
            setup = setups_data.iloc[i][2]
            z= setups_data.iloc[i][3]
            tf= setups_data.iloc[i][4] 
            zs = z
            
            
            if data.isToday(date):
                if tf == 'd':
                    tf1 = 'd'
                    tf2 = 'w'
                    tf3 = 'h'
                    tf4 = '15min'
                if tf == 'h':
                    tf1 = 'h'
                    df2 = 'd'
                    df3 = '15min'
                    df4 = '1min'
                if tf == '5min':
                    tf1 = '5min'
                    tf2 = 'd'
                    tf3 = 'h'
                    tf4 = '1min'
                if tf == '1min':
                    tf1 = '1min'
                    tf2 = 'd'
                    tf3 = 'h'
                    tf4 = '5min'
            else:
                if tf == 'd':
                    tf1 = 'd'
                    tf2 = 'w'
                    tf3 = 'h'
                    tf4 = '1min'
                if tf == 'h':
                    tf1 = 'h'
                    df2 = 'd'
                    df3 = '15min'
                    df4 = '1min'
                if tf == '5min':
                    tf1 = '5min'
                    tf2 = 'd'
                    tf3 = 'h'
                    tf4 = '1min'
                if tf == '1min':
                    tf1 = '1min'
                    tf2 = 'd'
                    tf3 = 'h'
                    tf4 = '5min'

            datedaily = f"{date}"
            datehourly = f"{date} 09:00"
            dateminute = f"{date} 09:30"

            chartsize = 150
           
            ch = 50
            cd = 110
            cm = 0

            fw = 20
            fh = 7

            fs = .8

            try:
                if 'h' in tf1:
                    c1 = ch
                    d1 = datehourly
                elif 'min' in tf1:
                    d1 = dateminute
                    c1 = cm
                else:
                    c1 = cd
                    d1 = datedaily
                df1 = data.get(ticker,tf1,date)
                l1 = data.findex(df1,date) - c1
                r1 = l1 + chartsize
                if l1 < 0:
                    l1 = 0
                df1 = df1[l1:r1]
                string1 = "1" + iss + ".png"
                p1 = pathlib.Path("C:/Screener/tmp/charts") / string1
                if data.isToday(date):
                    mpf.plot(df1, type='candle', volume=True, title=str(f'{ticker}   {setup}   {round(zs,2)}   {tf1}'), style=s, savefig=p1, figratio = (fw,fh), mav=(10,20),figscale=fs, panel_ratios = (5,1), tight_layout = True)#, hlines=dict(hlines=[pmPrice], alpha = .25))
                else:
                    mpf.plot(df1, type='candle', volume=True, title=str(f'{ticker}   {date}   {setup}   {round(zs,2)}   {tf1}'), style=s, savefig=p1,figratio = (fw,fh),figscale=fs, panel_ratios = (5,1), mav=(10,20), tight_layout = True,vlines=dict(vlines=[d1], alpha = .25))
            except:
                print(ticker)
                
            try:
                if 'h' in tf2:
                    c2 = ch
                    d2 = datehourly
                elif 'min' in tf2:
                    d2 = dateminute
                    c2 = cm
                else:
                    d2 = datedaily
                    c2 = cd
                df2 = data.get(ticker,tf2)
                l2 = data.findex(df2,date) - c2
                r2 = l2 + chartsize
                if l2 < 0:
                    l2 = 0
                df2 = df2[l2:r2]
                string2 = "2" + iss + ".png"
                p2 = pathlib.Path("C:/Screener/tmp/charts") / string2
                if data.isToday(date):
                    mpf.plot(df2, type='candle', volume=True, title = str(tf2), style=s,  savefig=p2, figratio = (fw,fh), mav=(10,20),figscale=fs, panel_ratios = (5,1), tight_layout = True)#, hlines=dict(hlines=[pmPrice], alpha = .25))
                else:
                    mpf.plot(df2, type='candle', volume=True, title=str(tf2), style=s, savefig=p2, figratio = (fw,fh), mav=(10,20),figscale=fs, panel_ratios = (5,1), tight_layout = True,vlines=dict(vlines=[d2], alpha = .25))

            except:
                pass
             
            try:
                if 'h' in tf3:
                    d3 = datehourly
                    c3 = ch
                elif 'min' in tf3:
                    d3 = dateminute
                    c3 = cm
                else:
                    c3 = cd
                    d3 = datedaily
                df3 = data.get(ticker,tf3)
                l3 = data.findex(df3,date) - c3
                r3 = l3 + chartsize
                if l3 < 0:
                    l3 = 0
                df3 = df3[l3:r3]
                string3 = "3" + iss + ".png"
                p3 = pathlib.Path("C:/Screener/tmp/charts") / string3
                if data.isToday(date):
                    mpf.plot(df3, type='candle', volume=True, title = str(tf3),style=s,  savefig=p3, figratio =(fw,fh), mav=(10,20),figscale=fs, panel_ratios = (5,1), tight_layout = True)#, hlines=dict(hlines=[pmPrice], alpha = .25))
                else:
                    mpf.plot(df3, type='candle', volume=True, title = str(tf3),style=s,  savefig=p3, figratio = (fw,fh), mav=(10,20),figscale=fs, panel_ratios = (5,1), tight_layout = True,vlines=dict(vlines=[d3], alpha = .25))

            except:
                pass
      

            try:
                if 'h' in tf4:
                    c4 = ch
                    d4 = datehourly
                elif 'min' in tf4:
                    c4 = cm
                    d4 = dateminute
                else:
                    c4 = cd
                    d4 = datedaily
                df4 = data.get(ticker,tf4)
                l4 = data.findex(df4,date) - c4
                r4 = l4 + chartsize
                if l4 < 0:
                    l4 = 0
                df4 = df4[l4:r4]
                string4 = "4" + iss + ".png"
                p4 = pathlib.Path("C:/Screener/tmp/charts") / string4
                
                if data.isToday(date):
                    mpf.plot(df4, type='candle', volume=True, title = str(tf4),style=s, savefig=p4, figratio = (fw,fh),figscale=fs, panel_ratios = (5,1), mav=(10,20), tight_layout = True)#, hlines=dict(hlines=[pmPrice], alpha = .25))
                else:
                    mpf.plot(df4, type='candle', volume=True, title = str(tf4),style=s,  savefig=p4, figratio = (fw,fh),figscale=fs, panel_ratios = (5,1), mav=(10,20), tight_layout = True,vlines=dict(vlines=[d4], alpha = .25))
            except:
                pass
           
                       
    def preload(self,init):
        arglist = []
        c = 0
        if not init:
            c = self.preloadbuffer
        for x in range(self.preloadamount - c):
            
            v = (x + self.i + c)
            if v < len(self.setups_data):
                arglist.append([self.setups_data,v])

        with Pool(nodes=6) as pool:
            pool.map(self.plot, arglist)

    def update(self, init,values,previ):
       
        
        lasttime = ttime.time()
        image1 = None
        image2 = None
        image3 = None
        image4 = None
        while True:
            laptime = round((ttime.time() - lasttime), 2)
            if laptime < .3:

                
                if image1 == None:
                    try:
                        image1 = Image.open(r"C:\Screener\tmp\charts\1" + str(self.i) + ".png")
                    except:
                        pass
                 
                if image2 == None:
                    try:
                        image2 = Image.open(r"C:\Screener\tmp\charts\2" + str(self.i) + ".png")
                    except :
                        pass
                if image3 == None:
                    try:
                        image3 = Image.open(r"C:\Screener\tmp\charts\3" + str(self.i) + ".png")
                    except:
                        pass
                if image4 == None:
                    try:
                        image4 = Image.open(r"C:\Screener\tmp\charts\4" + str(self.i) + ".png")
                    except:
                        pass

                if image1 != None and image2 != None and image3 != None and image4 != None:
                    break
                
            else:

                #print("image timed out")
                if image1 == None:
                    image1 = Image.open(r"C:\Screener\tmp\blank.png")
               
                if image2 == None:
                    image2 = Image.open(r"C:\Screener\tmp\blank.png")
             
                if image3 == None:
                    image3 = Image.open(r"C:\Screener\tmp\blank.png")
           
                if image4 == None:
                    image4 = Image.open(r"C:\Screener\tmp\blank.png")
               
                break

       # image1.thumbnail((1220, 500))
        bio1 = io.BytesIO()
        image1.save(bio1, format="PNG")
           
        #image2.thumbnail((1220, 500))
        bio2 = io.BytesIO()
        image2.save(bio2, format="PNG")

       # image3.thumbnail((1220, 500))
        bio3 = io.BytesIO()
        image3.save(bio3, format="PNG")

        #image4.thumbnail((1220, 500))
        bio4 = io.BytesIO()
        image4.save(bio4, format="PNG")

        if self.historical:

            gap = str(self.setups_data.iloc[self.i][5])
            adr = str(self.setups_data.iloc[self.i][6])
            vol = str(self.setups_data.iloc[self.i][7])
            q = str(self.setups_data.iloc[self.i][8])
            one = str(self.setups_data.iloc[self.i][9])
            two = str(self.setups_data.iloc[self.i][10])
            three = str(self.setups_data.iloc[self.i][11])
            ten = str(self.setups_data.iloc[self.i][12])
            annotation = str(self.setups_data.iloc[self.i][13])
            #rating = str(self.setups_data.iloc[self.i][13])
            time = str(self.setups_data.iloc[self.i][14])
            
                
            if annotation == "nan":
                annotation = ""
 
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
                df = pd.read_feather(r"C:\Screener\tmp\setups.feather")
                index = self.setups_data.index[previ]
                #print('saved annotation')
                df.at[index, 'annotation'] = values["annotation"]
                self.setups_data.at[index, 'annotation'] = values["annotation"]   
                
                df.to_feather(r"C:\Screener\tmp\setups.feather")
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
                [sg.Image(bio1.getvalue(),key = '-IMAGE-'),sg.Image(bio2.getvalue(),key = '-IMAGE2-')],
                [sg.Image(bio3.getvalue(),key = '-IMAGE3-'),sg.Image(bio4.getvalue(),key = '-IMAGE4-')],
              
                    
                [(sg.Text((str(f"{self.i + 1} of {len(self.setups_data)}")), key = '-number-'))],
                   
                        [sg.Button('Prev'), sg.Button('Next')] 
                ]
                self.window = sg.Window('Screener', layout,margins = (10,10))
            else:
                try:

                    self.window["-IMAGE-"].update(data=bio1.getvalue())
                    self.window["-IMAGE2-"].update(data=bio2.getvalue())
                    self.window["-IMAGE3-"].update(data=bio3.getvalue())
                    self.window["-IMAGE4-"].update(data=bio4.getvalue())
                except:
                    print("image load failed")
                self.window['-number-'].update(str(f"{self.i + 1} of {len(self.setups_data)}"))
           

if __name__ == "__main__":
    UI.loop(UI,False)

