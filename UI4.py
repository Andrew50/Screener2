

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
from multiprocessing.pool import Pool
import statistics


class UI:

    def loop(self,current = False):
        '''
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
        '''
        self.historical = not current
       
        self.preloadamount = 20
        self.traitlist = []

        with Pool(6) as self.pool:
            self.lookup(self,"","","","","","")
            self.update(self,True,None,0)

            while True:
            
                event, values = self.window.read()
                if event == 'Next': 
                    if self.i < len(self.setups_data) - 1:
                        previ = self.i
                        self.i += 1
                        self.update(self,False,values,previ)
                        self.window.refresh()
                        self.preload(self,self.i + self.preloadamount)
    
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
                        for thing in range(4):

                            if os.path.exists(f"C:/Screener/tmp/charts/{thing + 1}{i}.png"):
                                os.remove(f"C:/Screener/tmp/charts/{thing + 1}{i}.png")
                    
                        self.preload(self,i)
               
                        self.update(self,False,values,i)
                    else:
                        timeframe = values['input-timeframe']
                        ticker = values["input-ticker"]
                        date = values["input-date"]
                        setup = values["input-setup"]
                        keyword = values["input-keyword"]
                        previ = 0
                        sortinput = ""
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
                    break
            self.window.close()

    def preload(self,i):
        pool = self.pool
        if type(i) == int:
            i = [i]
      
        arglist = []
        for index in i:
            arglist.append([self.setups_data,index])
        pool.map_async(self.plot,arglist)

    def redate(self,previ,new):
        df = pd.read_feather(r"C:\Screener\tmp\setups.feather")
        index = self.setups_data.index[previ]
        ap = data.get()
        date = (self.setups_data.iat[previ,0])
        new_index = data.findex(ap,date) + int(new)
        newdate = ap.index[new_index]
        df.at[index, 'Date'] = newdate
        self.setups_data.at[index, 'Date'] = newdate
                
        df.to_feather(r"C:\Screener\tmp\setups.feather")
        

    def lookup(self,ticker,date,setup,keyword,sortinput,timeframe):

        if self.historical:
        
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
             
                idex = 0
                if sortinput == 'z':
                    idex = 'Z'
                if sortinput == 'gap':
                    idex = 'gap'
                if sortinput == 'adr':
                    idex = 'adr'
                if sortinput == 'vol':
                    idex = 'vol'
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

        else:
            scan = pd.read_feather(r"C:\Screener\tmp\todays_setups.feather")

        if len(scan) < 1:
            sg.Popup('No Setups Found')
        else:
            
            self.i = 0
            self.setups_data = scan
            if os.path.exists("C:/Screener/tmp/charts"):
                shutil.rmtree("C:/Screener/tmp/charts")
            os.mkdir("C:/Screener/tmp/charts")
           
            self.preload(self, list(range(self.preloadamount)))

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
                    fig, axlist = mpf.plot(df1, type='candle', volume=True, title=str(f'{ticker}   {date}   {setup}   {round(zs,2)}   {tf1}'), style=s, returnfig = True,figratio = (fw,fh),figscale=fs, panel_ratios = (5,1), mav=(10,20), tight_layout = True,vlines=dict(vlines=[d1], alpha = .25))
                    ax = axlist[0]
                  
                    ax.set_yscale('log')
                    ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                    
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
        
      
        
    def update(self, init,values,previ):
        image1 = None
        image2 = None
        image3 = None
        image4 = None

        gosh = 1
        start = datetime.datetime.now()
        while True:
            if (datetime.datetime.now() - start).seconds < gosh or init:
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
                start = datetime.datetime.now()
                print('reloading image')
                gosh = 10
                
        bio1 = io.BytesIO()
        image1.save(bio1, format="PNG")
        bio2 = io.BytesIO()
        image2.save(bio2, format="PNG")
        bio3 = io.BytesIO()
        image3.save(bio3, format="PNG")
        bio4 = io.BytesIO()
        image4.save(bio4, format="PNG")
        
        if self.historical:

            date = self.setups_data.iat[self.i,0]
            ticker = self.setups_data.iat[self.i,1]
            '''
            gap = str(self.setups_data.iloc[self.i][5])
            adr = str(self.setups_data.iloc[self.i][6])
            vol = str(self.setups_data.iloc[self.i][7])
            q = str(self.setups_data.iloc[self.i][8])
            one = str(self.setups_data.iloc[self.i][9])
            two = str(self.setups_data.iloc[self.i][10])
            three = str(self.setups_data.iloc[self.i][11])
            ten = str(self.setups_data.iloc[self.i][12])
            annotation = str(self.setups_data.iloc[self.i][13])



            '''
           
            
            traits = UI.traits(ticker,date)

         

            

            gap = traits[0]
            adr = traits[1]
            vol = traits[2]
            q = traits[3]
            one = traits[4]
            two = traits[5]
            three = traits[6]
            ten = traits[7]
            time = traits[8]
            vol1 = traits[9]
            



 
            if init:
                
                annotation = self.setups_data.iat[self.i,5]
            
                sg.theme('DarkGrey')
                layout = [  
                [sg.Image(bio1.getvalue(),key = '-IMAGE-'),sg.Image(bio2.getvalue(),key = '-IMAGE2-')],
                [sg.Image(bio3.getvalue(),key = '-IMAGE3-'),sg.Image(bio4.getvalue(),key = '-IMAGE4-')],
                [ (sg.Text("gap")),(sg.Text(gap, key = '-gap-')),
                (sg.Text("|   adr")),(sg.Text(adr, key = '-adr-')),
                (sg.Text("|   vol")),(sg.Text(vol, key = '-vol-')),
                (sg.Text("|   vol1")),(sg.Text(vol1, key = '-vol1-')),
                (sg.Text("|   q")),(sg.Text(q, key = '-q-')),
                (sg.Text("|   1")),(sg.Text(one, key = '-one-')),
                (sg.Text("|   2")),(sg.Text(two, key = '-two-')),
                (sg.Text("|   3")),(sg.Text(three, key = '-three-')),
                (sg.Text("|   10")),(sg.Text(ten, key = '-ten-')),
                (sg.Text("|   time")),(sg.Text(time, key = '-time-'))],
                [sg.Multiline(annotation,size=(150, 5), key='annotation')],
                [(sg.Text("Timeframe")),sg.InputText(key = 'input-timeframe')],
                [(sg.Text("Ticker      ")),sg.InputText(key = 'input-ticker')],
                [(sg.Text("Date        ")),sg.InputText(key = 'input-date')],
                [(sg.Text("Setup      ")),sg.InputText(key = 'input-setup')],
                [(sg.Text("Keyword  ")),sg.InputText(key = 'input-keyword')],
              #  [(sg.Text("Trait        ")),sg.InputText(key = 'input-trait')],
                [(sg.Text("Redate    ")),sg.InputText(key = 'input-redate')],
                [(sg.Text((str(f"{self.i + 1} of {len(self.setups_data)}")), key = '-number-'))],
                [sg.Button('Prev'), sg.Button('Next'),sg.Button('Load')]]
                self.window = sg.Window('Screener', layout,margins = (10,10))
            else:
                df = pd.read_feather(r"C:\Screener\tmp\setups.feather")
                index = self.setups_data.index[previ]
                df.at[index, 'annotation'] = values["annotation"]
                self.setups_data.at[index, 'annotation'] = values["annotation"]   
                df.to_feather(r"C:\Screener\tmp\setups.feather")
                
                annotation = self.setups_data.iat[self.i,5]
                self.window['-number-'].update(str(f"{self.i + 1} of {len(self.setups_data)}"))
                self.window["-gap-"].update(gap)
                self.window["-adr-"].update(adr)
                self.window["-vol-"].update(vol)
                self.window["-vol1-"].update(vol1)
                self.window["-q-"].update(q)
                self.window["-one-"].update(one)
                self.window["-two-"].update(two)
                self.window["-three-"].update(three)
                self.window["-ten-"].update(ten)
                self.window["-time-"].update(time)
                self.window["annotation"].update(annotation)
                self.window["input-redate"].update("")
                self.window["-IMAGE-"].update(data=bio1.getvalue())
                self.window["-IMAGE2-"].update(data=bio2.getvalue())
                self.window["-IMAGE3-"].update(data=bio3.getvalue())
                self.window["-IMAGE4-"].update(data=bio4.getvalue())
   
        else:
            if init:
                sg.theme('DarkGrey')
                
                layout = [  
                [sg.Image(bio1.getvalue(),key = '-IMAGE-'),sg.Image(bio2.getvalue(),key = '-IMAGE2-')],
                [sg.Image(bio3.getvalue(),key = '-IMAGE3-'),sg.Image(bio4.getvalue(),key = '-IMAGE4-')],
                [(sg.Text((str(f"{self.i + 1} of {len(self.setups_data)}")), key = '-number-'))],
                [sg.Button('Prev'), sg.Button('Next')] ]
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
           


    def traits(ticker,date):

        df = data.get(ticker,'d')
        df_m = data.get(ticker,'1min')


        currentday = data.findex(df,date)
        currentmin = data.findex(df_m,date)

        gap = round( (df.iat[currentday,0]/df.iat[currentday-1,3] - 1)*100,2)

        volma = []
        for i in range(10):
            volma.append(df.iat[currentday-1-i,4])
        vol = round((df.iat[currentday,4]/statistics.mean(volma) ),2) * 100

        try:
            vol1 = round(( df_m.iat[currentmin,4]/statistics.mean(volma)),2) * 100
        except:
            vol1 = 'NA'

        q_data = data.get('QQQ')
        qcurrentday = data.findex(q_data, date)
        q10 = []
        q20 = []

        for i in range(21):
            close = q_data.iat[qcurrentday - 1-i,3]

            q20.append(close)
            if i >= 9:
                q10.append(close)

            if i == 19:
                prev10 = statistics.mean(q10)
                prev20 = statistics.mean(q20)

        current10 = statistics.mean(q10)
        current20 = statistics.mean(q20)
            
        if current10 > prev10 and current20 > prev20 and current10 > current20:
            q = True
        else:
            q = False
            
        one = round((df.iat[currentday,3] / df.iat[currentday,0] - 1) * 100,2)
        two =   round((df.iat[currentday+1,3] / df.iat[currentday,0] - 1) * 100,2)
        three =  round((df.iat[currentday+2,3] / df.iat[currentday,0] - 1) * 100,2)
        four = round((df.iat[currentday+3,3] / df.iat[currentday,0] - 1) * 100,2)
        five = round((df.iat[currentday+4,3] / df.iat[currentday,0] - 1) * 100,2)

        change10 = 0
        change20 = 0
        change60 = 0
        change250 = 0

        try:
            change10 = round((df.iat[currentday-1,3] / df.iat[currentday-11,3] - 1) * 100,2)

            change20 = round((df.iat[currentday-1,3] / df.iat[currentday-21,3] - 1) * 100,2)
            change60 = round((df.iat[currentday-1,3] / df.iat[currentday-61,3] - 1) * 100,2)
            change250 = round((df.iat[currentday-1,3] / df.iat[currentday-251,3] - 1) * 100,2)
        except:
            pass
                            
              


        adr = []
        for j in range(20): 
            high = df.iat[currentday-j-1,1]
            low = df.iat[currentday-j-1,2]
            val = (high/low - 1) * 100
            adr.append(val)
                        
        adr = round(statistics.mean(adr) ,2)
           
        i = 0

                
        while True:

            ma10 = []
            for j in range(10):
                ma10.append((df.iat[currentday-j+i,3]))
            ma10 = statistics.mean(ma10)
            close = df.iat[currentday+i,3]

            if i == 0:
                if close > ma10:
                    short = False
                else:
                    short = True

            if short:
                if close > ma10:
                    break
            else:
                if ma10 > close:
                    break
                   
                    
            if i == len(df):
                break

            i += 1
                

        ten = round( (df.iat[currentday+i,3] / df.iat[currentday,0] - 1)*100,2)
        time = i 

        return [gap,adr,vol,q,one,two,three,ten,time,vol1]




if __name__ == "__main__":
    UI.loop(UI,False)


