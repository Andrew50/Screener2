

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
import matplotlib.ticker as mticker

from Data7 import Data as data
import time as ttime
import shutil
from time import sleep

#from pathos.multiprocessing import ProcessingPool as Pool

from multiprocessing.pool import Pool





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
        self.preloadbuffer = self.preloadamount - 4
        self.lookup(self,"","","","","","")
        #results = self.preload(self, True)
        
        #(self,True)
        self.update(self,True,None,0)
        while True:
            
            event, values = self.window.read()


            if event == 'Next': 

                if self.i < len(self.setups_data) - 1:
                 
                    previ = self.i
                    self.i += 1
                   
                    self.update(self,False,values,previ)
                    self.window.refresh()
                    
                    process = self.preload(self,False)
                   # sleep(5)
                    while not process.ready():
                        pass

                    

            if event == 'Prev':
                
                if self.i > 0:
                    previ = self.i
                    self.i -= 1
                   
                    self.update(self,False,values,previ)


    
            if event == 'Load':
                red = values['input-redate']
                if red != "":
                    self.redate(self,self.i,values['input-redate'])

                    i = self.i
                    #print(f'redating {i}')
                    for thing in range(4):

                        if os.path.exists(f"C:/Screener/tmp/charts/{thing + 1}{i}.png"):
                            os.remove(f"C:/Screener/tmp/charts/{thing + 1}{i}.png")
                    
                    self.preload(self, True,i)
               
                    self.update(self,False,values,i)
                else:
                    timeframe = values['input-timeframe']
                    ticker = values["input-ticker"]
                    date = values["input-date"]
                    setup = values["input-setup"]
                    keyword = values["input-keyword"]
                    previ = 0
           
                
                    sortinput = values["input-trait"]
                    self.lookup(self,ticker,date,setup,keyword,sortinput,timeframe)
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
                #self.update(self,False,values,self.i)fd
                break
            
        self.window.close()
    def redate(self,previ,new):
        df = pd.read_feather(r"C:\Screener\tmp\setups.feather")
        index = self.setups_data.index[previ]
        #print('saved annotation')

        ap = data.get()
        date = (self.setups_data.iat[previ,0])
        

        new_index = data.findex(ap,date) + int(new)

        newdate = ap.index[new_index]

       # print(f'{date} , {newdate}')

        df.at[index, 'Date'] = newdate
        self.setups_data.at[index, 'Date'] = newdate
                
        df.to_feather(r"C:\Screener\tmp\setups.feather")
        

    def lookup(self,ticker,date,setup,keyword,sortinput,timeframe):
        
        print(f'searching for "{keyword}"')
        scan = pd.read_feather(r"C:\Screener\tmp\setups.feather")

        if timeframe  != "":
            scan = scan[scan['timeframe'] == timeframe]
            
        if ticker  != "":
            scan = scan[scan["Ticker"] == ticker]

        if date  != "":
            scan = scan[scan['Date'] == date]
     
        if setup  != "":
            scan = scan[scan['Setup'] == setup]
      
        if keyword  != "":
            lis = keyword.split(',')
            for keyword in lis:
                scan = scan[scan['annotation'].str.contains(keyword)]   
        else:
            scan = scan[scan['annotation'] == "" ]
            
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
        print(i)
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
            cd = 100
            cm = 0


            sh = 200
            sd = 150
            sm = 300

            fw = 20
            fh = 7

            fs = .8

            try:
                if 'h' in tf1:
                    c1 = ch
                    d1 = datehourly
                    s1 = sh
                elif 'min' in tf1:
                    d1 = dateminute
                    c1 = cm
                    s1 = sm
                else:
                    c1 = cd
                    d1 = datedaily
                    s1 = sd
                df1 = data.get(ticker,tf1,date)
                l1 = data.findex(df1,date) - c1
                r1 = l1 + s1
                if l1 < 0:
                    l1 = 0
                df1 = df1[l1:r1]
                string1 = "1" + iss + ".png"
                p1 = pathlib.Path("C:/Screener/tmp/charts") / string1
                if data.isToday(date):
                    fig, axlist  =  mpf.plot(df1, type='candle', volume=True, title=str(f'{ticker}   {setup}   {round(zs,2)}   {tf1}'), style=s, returnfig = True, figratio = (fw,fh), mav=(10,20),figscale=fs, panel_ratios = (5,1), tight_layout = True)#, hlines=dict(hlines=[pmPrice], alpha = .25))
                    ax = axlist[0]
                 
                    ax.set_yscale('log')
                    ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                   
                    plt.savefig(p1, bbox_inches='tight')
                    
                else:
                    #mpf.plot(df1, type='candle', volume=True, title=str(f'{ticker}   {date}   {setup}   {round(zs,2)}   {tf1}'), style=s, savefig=p1,figratio = (fw,fh),figscale=fs, panel_ratios = (5,1), mav=(10,20), tight_layout = True,vlines=dict(vlines=[d1], alpha = .25))
                    fig, axlist = mpf.plot(df1, type='candle', volume=True, title=str(f'{ticker}   {date}   {setup}   {round(zs,2)}   {tf1}'), style=s, returnfig = True,figratio = (fw,fh),figscale=fs, panel_ratios = (5,1), mav=(10,20), tight_layout = True,vlines=dict(vlines=[d1], alpha = .25))
                    ax = axlist[0]
                  
                    ax.set_yscale('log')
                    ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                    #ax.ticklabel_format(style='plain', axis = 'y')
                    
                    plt.savefig(p1, bbox_inches='tight')
            except:
                pass
                #print(ticker)
               
                


            try:
                if 'h' in tf2:
                    c2 = ch
                    d2 = datehourly
                    s2 = sh
                elif 'min' in tf2:
                    d2 = dateminute
                    c2 = cm
                    s2 = sm
                else:
                    d2 = datedaily
                    c2 = cd
                    s2 = sd
                df2 = data.get(ticker,tf2)
                l2 = data.findex(df2,date) - c2
                r2 = l2 + s2
                if l2 < 0:
                    l2 = 0
                df2 = df2[l2:r2]
                string2 = "2" + iss + ".png"
                p2 = pathlib.Path("C:/Screener/tmp/charts") / string2
                if data.isToday(date):
                    fig, axlist = mpf.plot(df2, type='candle', volume=True, title = str(tf2), style=s,  returnfig = True, figratio = (fw,fh), mav=(10,20),figscale=fs, panel_ratios = (5,1), tight_layout = True)#, hlines=dict(hlines=[pmPrice], alpha = .25))
                    ax = axlist[0]
                 
                    ax.set_yscale('log')
                    ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                   
                    plt.savefig(p2, bbox_inches='tight')
                else:
                    fig, axlist =  mpf.plot(df2, type='candle', volume=True, title=str(tf2), style=s, returnfig = True, figratio = (fw,fh), mav=(10,20),figscale=fs, panel_ratios = (5,1), tight_layout = True,vlines=dict(vlines=[d2], alpha = .25))
                    ax = axlist[0]
                 
                    ax.set_yscale('log')
                    ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                   
                    plt.savefig(p2, bbox_inches='tight')
            except:
                pass
             

            string3 = "3" + iss + ".png"
            p3 = pathlib.Path("C:/Screener/tmp/charts") / string3
            try:
                if 'h' in tf3:
                    d3 = datehourly
                    c3 = ch
                    s3 = sh
                elif 'min' in tf3:
                    d3 = dateminute
                    c3 = cm
                    s3 = sm
                else:
                    c3 = cd
                    d3 = datedaily
                    s3 = sd
                df3 = data.get(ticker,tf3)
                l3 = data.findex(df3,date) - c3
                r3 = l3 + s3
                if l3 < 0:
                    l3 = 0
                df3 = df3[l3:r3]
                
                if data.isToday(date):
                    fig, axlist = mpf.plot(df3, type='candle', volume=True, title = str(tf3),style=s,  returnfig = True, figratio =(fw,fh), mav=(10,20),figscale=fs, panel_ratios = (5,1), tight_layout = True)#, hlines=dict(hlines=[pmPrice], alpha = .25))
                    ax = axlist[0]
                    
                    ax.set_yscale('log')
                    ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                   
                    plt.savefig(p3, bbox_inches='tight')
                else:
                    fig, axlist = mpf.plot(df3, type='candle', volume=True, title = str(tf3),style=s,  returnfig = True, figratio = (fw,fh), mav=(10,20),figscale=fs, panel_ratios = (5,1), tight_layout = True,vlines=dict(vlines=[d3], alpha = .25))
                    ax = axlist[0]
                   
                    ax.set_yscale('log')
                    ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                   
                    plt.savefig(p3, bbox_inches='tight')
            except:
                shutil.copy(r"C:\Screener\tmp\blank.png",p3)
      


            string4 = "4" + iss + ".png"
            p4 = pathlib.Path("C:/Screener/tmp/charts") / string4
            try:
                if 'h' in tf4:
                    c4 = ch
                    d4 = datehourly
                    s4 = sh
                elif 'min' in tf4:
                    c4 = cm
                    d4 = dateminute
                    s4 = sm
                else:
                    c4 = cd
                    d4 = datedaily
                    s4 = sd
                df4 = data.get(ticker,tf4)
                l4 = data.findex(df4,date) - c4
                r4 = l4 + s4
                if l4 < 0:
                    l4 = 0
                df4 = df4[l4:r4]
                
                
                if data.isToday(date):
                    plot, axlist =  mpf.plot(df4, type='candle', volume=True, title = str(tf4),style=s, returnfig = True, figratio = (fw,fh),figscale=fs, panel_ratios = (5,1), mav=(10,20), tight_layout = True)#, hlines=dict(hlines=[pmPrice], alpha = .25))
                    ax = axlist[0]
                    
                    ax.set_yscale('log')
                    ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                   
                    plt.savefig(p4, bbox_inches='tight')
                else:
                    plot, axlist = mpf.plot(df4, type='candle', volume=True, title = str(tf4),style=s, returnfig = True, figratio = (fw,fh),figscale=fs, panel_ratios = (5,1), mav=(10,20), tight_layout = True,vlines=dict(vlines=[d4], alpha = .25))
                    ax = axlist[0]
                    
                    ax.set_yscale('log')
                    ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                   
                    plt.savefig(p4, bbox_inches='tight')
            except:
                shutil.copy(r"C:\Screener\tmp\blank.png",p4)
        
                       
    def preload(self,init,force = None):
        arglist = []
        c = 0
        #tm = datetime.datetime.now()
        if init:
       # if not init:
        #    c = self.preloadbuffer

            if force == None:
                for x in range(self.preloadamount - c):
            
                    v = (x + self.i + c)
                    
                    if v < len(self.setups_data):
                        arglist.append([self.setups_data,v])
            else:
                arglist.append([self.setups_data,force])
            
            with Pool() as pool:
               
                pool.map(self.plot, arglist)
                pool.close()
                pool.join
              
        else:
            v = self.i + self.preloadamount - 1
            with Pool() as pool:
            
                process = pool.apply_async(self.plot,args = ([self.setups_data,v],))
                return(process)
                #pool.close()
            #pool.join()
            
        #print(datetime.datetime.now() - tm)

    def update(self, init,values,previ):



        image1 = None
        image2 = None
        image3 = None
        image4 = None
        start = datetime.datetime.now()
        while True:
            if datetime.datetime.now() - start < 5:
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
                self.preload(self,self.i)
                
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
                [(sg.Text("Ticker      ")),sg.InputText(key = 'input-ticker')],
                [(sg.Text("Date        ")),sg.InputText(key = 'input-date')],
                [(sg.Text("Setup      ")),sg.InputText(key = 'input-setup')],
                [(sg.Text("Keyword  ")),sg.InputText(key = 'input-keyword')],
                [(sg.Text("Trait        ")),sg.InputText(key = 'input-trait')],
                [(sg.Text("Redate    ")),sg.InputText(key = 'input-redate')],
               
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
                [sg.Button('Prev'), sg.Button('Next'),sg.Button('Load')]# , sg.Button('Toggle')]#, sg.Button('Sort')] 
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
                self.window["input-redate"].update("")
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

