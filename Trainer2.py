


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
import math



class Trainer:


    def log(self):

        if self.event == 'Clear':
            for i in range(len(self.current_setups)-1,-1,-1):
                print(f'{self.current_setups[i][0]} == {self.index}')
                if self.current_setups[i][0] == self.index:
                    for k in range(2):
                        self.window["-GRAPH-"].MoveFigure(self.current_setups[i][2][k],5000,0)

                    del self.current_setups[i]

        else:
            setup = self.event

        
            x = self.select_line_x
            y = self.y - 50

            if y < 10:
                y = 110




            text = self.window["-GRAPH-"].draw_text( setup, (x,y) , color='black', font=None, angle=0, text_location='center')

            line = self.window["-GRAPH-"].draw_line((self.select_line_x,0), (self.select_line_x,self.height), color='black', width=2)
        

        

            self.current_setups.append([self.index,setup,[line,text]])

            self.y -= 35


    def save(self):
        
        df1 = self.dict[self.i][2]
        ticker = self.dict[self.i][0]



        for s in self.setup_list:
            df = pd.DataFrame()
            
            df['date'] = df1.index
            df['ticker'] = ticker
            df['setup'] = 0
           
            for bar in self.current_setups:
                
                if bar[1] == s:
                    index = bar[0]
                    df.iat[index,2] = 1

            df = df[self.cutoff:]
            

            add = df[['ticker','date','setup']]


            df = pd.read_feather('C:/Screener/setups/' + s + '.feather')


            df = pd.concat([df,add]).reset_index(drop = True)

            df.to_feather('C:/Screener/setups/' + s + '.feather')

            print(df.to_string())
    
    def click(self):
        df = self.dict[self.i][2]
        ticker = self.dict[self.i][0]
        x = self.values['-GRAPH-'][0]

        self.y = self.values['-GRAPH-'][1]

        
            


        chart_click = x - 10
        chart_size = self.x_size - 20
        percent = chart_click/chart_size


        self.index = math.floor(len(df) * percent)


        if self.index <= -1:
            self.index = 0
        if self.index >= len(df):
            self.index = len(df) - 1
        
        try:

            self.date = df.index[self.index]

            print(ticker)
            print(self.date)
        except:
            return

        round_x = int((self.index + 1)/(len(df)) * (self.x_size - 20)) + 10 - int((chart_size/len(df))/2)
        
        self.window["-GRAPH-"].MoveFigure(self.select_line,round_x - self.select_line_x,0)

        self.select_line_x = round_x

        
        

    def update(self):
        if self.init:
            sg.theme('DarkGrey')


            graph = sg.Graph(
            canvas_size=(self.width, self.height),
            graph_bottom_left=(0, 0),
            graph_top_right=(self.width, self.height),
            key="-GRAPH-",
            change_submits=True,  # mouse click events
            background_color='grey',
            drag_submits=False)
            layout = [
            [graph],
            [sg.Button(s) for s in self.setup_list],

            [sg.Button('Next'), sg.Button('Clear'), sg.Button('Skip')]]

            self.window = sg.Window('Trainer', layout,margins = (10,10),scaling=self.scale,finalize = True)
            
            self.init = False
            self.window.maximize()
        
        while True:
            try:
                image1 = Image.open(r'C:/Screener/setups/charts/' + str(self.i) + '.png')
                break
            except:
                pass



        self.x_size = image1.size[0]
        
        


        bio1 = io.BytesIO()
        image1.save(bio1, format="PNG")


        self.window['-GRAPH-'].erase()
        self.window["-GRAPH-"].draw_image(data=bio1.getvalue(), location=(0, self.height))


        self.select_line_x = -100
        self.select_line = self.window["-GRAPH-"].draw_line((self.select_line_x,0), (self.select_line_x,self.height), color='green', width=2)


        df = self.dict[self.i][2]
        

        chart_size = self.x_size - 20
        round_x = int((self.cutoff)/(len(df)) * (chart_size)) + 10 - int((chart_size/len(df))/2)

        


        self.window["-GRAPH-"].draw_line((round_x,0), (round_x,self.height), color='red', width=2)

        self.current_setups = []

       # graph.draw_image(data=data, location=(0, height))
        #self.window["-IMAGE-"].update(data=bio1.getvalue())

    def loop(self):

        if os.path.exists("C:/Screener/ben.txt"):
            self.height = 800
            self.width = 1700
          
        else:
            self.height = 1200
            self.width = 2500


        self.cutoff = 75

        self.size = 300

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

                    self.save(self)
                    self.i += 1
                    self.update(self)
                    self.preload(self)
                    self.current_setups = []
                elif self.event == 'Skip':
                    self.i += 1
                    self.update(self)
                    self.preload(self)
                    self.current_setups = []
                elif self.event == '-GRAPH-':
                    self.click(self)
                else:
                    self.log(self)

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
                    df2 = df[index-self.size:index + 1]
                    if len(df2) > 30:
                        dolVol, adr, pmvol = detection.requirements(df2,len(df2) - 1,2,ticker)
                        if dolVol > 2000000 and adr > 2:
                            break
                except:
                    pass
            self.dict.append([ticker,date,df2])
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
        tight_layout = True,axisoff=True)
        ax = axlist[0]
        ax.set_yscale('log')
        ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
        plt.savefig(p, bbox_inches='tight')

if __name__ == '__main__':
    Trainer.loop(Trainer)






