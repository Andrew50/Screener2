

from Data7 import Data as data
import matplotlib.pyplot as plt
import random
import mplfinance as mpf
import pandas as pd
import PySimpleGUI as sg
from multiprocessing.pool import Pool
from PIL import Image
import pathlib
import io
import matplotlib.ticker as mticker
import shutil
import os
from Detection2 import Detection as detection



class Trainer:

    
    def log(self):
        for s in self.setup_list:
            path = 'C:/Screener/setups/' + s + '.feather'
            try:
                df = pd.read_feather(path)
            except:
                df = pd.DataFrame()
            if s in self.setup:
                setup = 1
                print(f'{ticker} , {date} , {s}')
            else:
                setup = 0

            ticker = self.dict[self.i][0]
            date = self.dict[self.i][1]
            
            

            add = pd.DataFrame({
                'ticker':[ticker],
                'date':[date],
                'setup':[setup]
                })
            df = pd.concat([df,add]).reset_index(drop = True)
            df.to_feather(path)



       
     

        self.setup = []
        self.window['-text-'].update('')

    def update(self):
        if self.init:
            sg.theme('DarkGrey')
            layout = [
            [sg.Image(key = '-IMAGE-')],
            [sg.Button(s) for s in self.setup_list],
            [sg.Button('Next'), sg.Text(key = '-text-')]]

            self.window = sg.Window('Trainer', layout,margins = (10,10),scaling=self.scale,finalize = True)
            self.init = False
            self.window.maximize()
        
        while True:
            try:
                image1 = Image.open(r'C:/Screener/setups/charts/' + str(self.i) + '.png')
                break
            except:
                pass




        bio1 = io.BytesIO()
        image1.save(bio1, format="PNG")
        self.window["-IMAGE-"].update(data=bio1.getvalue())

    def loop(self):

        with Pool(6) as self.pool:
            if os.path.exists("C:/Screener/setups/charts"):
                shutil.rmtree("C:/Screener/setups/charts")
            os.mkdir("C:/Screener/setups/charts")

            self.setup_list = ['EP', 'NEP' , 'P' , 'NP' , 'MR' , 'F' , 'NF' , 'FB' , 'NFB']
            self.scale = 4
            self.setup = []
            self.i = 0
            self.init = True
            self.dict = []
            self.tickers = pd.read_feather(r"C:\Screener\sync\full_ticker_list.feather")['Ticker'].to_list()


            self.preload(self)
            self.update(self)

 

            while True:
                self.event, self.values = self.window.read()

                if self.event == 'Next':
                    self.log(self)
                    self.i += 1
                    self.update(self)
                    
                    self.preload(self)
                    self.setup = []
                else:
                    self.setup.append(self.event)
                    gud = ''
                    for i in self.setup:
                        gud += (str(i) + " ")
                        
                    self.window['-text-'].update(gud)
                

    def preload(self):

        arglist = []

        if self.i == 0:
            l = list(range(10))
        else:
            l = [9 + self.i]

        for i in l:

            while True:
                try:
                    ticker = self.tickers[random.randint(0,len(self.tickers)-1)]

                    df = data.get(ticker)

                    date_list = df.index.to_list()
            
                    date = date_list[random.randint(0,len(date_list) - 1)]
            
            

            
                    index = data.findex(df,date)
                    #df2 = df[index-200:index]
                    df2 = df[index-200:index + 1]

                    #o = df.iat[index,0]
                    #add = pd.DataFrame({
                    #    'datetime':[date],
                    #    'open':[o],
                    #    'high':[o],
                    #    'low':[o],
                    #    'close':[o],
                    #    'volume':[0]}).set_index('datetime')
                    #df2 = pd.concat([df2,add])

                    #filters
                    if len(df2) > 30:
                        dolVol, adr, pmvol = detection.requirements(df2,len(df2) - 1,2,ticker)
                        if dolVol > 2000000 and adr > 2:
                            break


                except:
                    pass
   

            self.dict.append([ticker,date])
            arglist.append([i,df2])


        self.pool.map_async(self.plot,arglist)

    def plot(bar):

        i = bar[0]
        df = bar[1]

        p = pathlib.Path("C:/Screener/setups/charts") / str(i)
        if os.path.exists("C:/Screener/laptop.txt"): #if laptop

            fw = 22
            fh = 12
            fs = 3
        elif os.path.exists("C:/Screener/ben.txt"):
            fw = 25
            fh = 12
            fs = 1.3
        else:
            fw = 25
            fh = 12
            fs = 2.2

        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)

        fig, axlist = mpf.plot(df, type='candle', volume=True  ,                          
        style=s, warn_too_much_data=100000,returnfig = True,figratio = (fw,fh),
        figscale=fs, panel_ratios = (5,1), 
        tight_layout = True)

        ax = axlist[0]

        ax.set_yscale('log')
        ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                    
        plt.savefig(p, bbox_inches='tight')



if __name__ == '__main__':
    Trainer.loop(Trainer)






