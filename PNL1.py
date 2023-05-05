from Data7 import Data as data
import pandas as pd
import matplotlib as mpl
import mplfinance as mpf
from multiprocessing.pool import Pool
from matplotlib import pyplot as plt
import PySimpleGUI as sg
import matplotlib.ticker as mticker
import datetime
from PIL import Image
import io
import pathlib
import shutil
import os



class PNL():

    def account(self,values):

        pass
    
    def traits(self):
        pos = []
        self.df_log = self.df_log.sort_values(by='Datetime')
        for k in range(len(self.df_log)):
            row = self.df_log.iloc[k].to_list()
            ticker = row[0]
            shares = row[2]
            date = row[1]
            index = None
            for i in range(len(pos)):
                if pos[i][0] == ticker:
                    index = i
                    break
            if index != None:
                prev_share = pos[index][2]
            else:
                prev_share = 0
                pos.append([ticker,date,shares,[]])
                index = len(pos) - 1
            pos[index][3].append(row)
            shares = prev_share + shares
            if shares == 0:
                for i in range(len(pos)):
                    if pos[i][0] == ticker:
                        index = i
                        bar = pos[i]
                        add = pd.DataFrame({
            
                        'Ticker': [bar[0]],
                        'Datetime':[bar[1]],
                        'Trades': [bar[3]]
                        })

                        self.df_traits = pd.concat([self.df_traits,add])
                        self.df_traits.reset_index(inplace = True,drop = True)

                        self.df_traits
                        del pos[i]
                        break
            else:
                
                pos[index][2] = shares



            #print(pos)

        for i in range(len(pos)-1,-1,-1):
           
            index = i
            bar = pos[i]
            add = pd.DataFrame({
            
            'Ticker': [bar[0]],
            'Datetime':[bar[1]],
            'Trades': [bar[3]]
            })

            self.df_traits = pd.concat([self.df_traits,add])
            self.df_traits.reset_index(inplace = True,drop = True)

            self.df_traits
            del pos[i]
            break

        self.df_traits = self.df_traits.sort_values(by='Datetime', ascending = False)
        print(self.df_traits)

        #self.df_traits.to_feather(r"C:\Screener\tmp\pnl\traits.feather")

    def log(self):

        if self.event == "Enter":
            
            ticker = str(self.values['input-ticker'])

            if ticker != "":
                dt = self.values['input-datetime']
                dt  = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
                shares = float(self.values['input-shares'])
                price = float(self.values['input-price'])
                setup = str(self.values['input-setup'])

                add = pd.DataFrame({
            
                    'Ticker': [ticker],
                    'Datetime':[dt],
                    'Shares': [shares],
                    'Price': [price],
                    'Setup': [setup]
                    })

                self.df_log = pd.concat([self.df_log,add])
                self.df_log.reset_index(inplace = True, drop = True)
                self.df_log.to_feather(r"C:\Screener\tmp\pnl\log.feather")
            
            print(self.df_log)
        elif self.event == "Clear":

            self.window["input-ticker"].update("")
            self.window["input-shares"].update("")
            self.window["input-price"].update("")
            self.window["input-setup"].update("")
            self.window["input-datetime"].update("")

        self.df_log = self.df_log.sort_values(by='Datetime')

    def plot(self):
        
        print('gosh')
        if self.event == 'Next' :
            if self.i == len(self.df_traits) - 1:
                return
            self.i += 1
        if self.event == 'Prev':
            if self.i == 0:
                return
            self.i -= 1
        if self.i + self.preloadamount < len(self.df_traits):
            if self.i == 0:
                i = list(range(self.preloadamount))
            else:
                i = [self.i + self.preloadamount - 1]
            pool = self.pool
  
            arglist = []
            for index in i:
                arglist.append([index,self.df_traits])
            pool.map_async(self.create,arglist)

        image1 = None
        image2 = None


        while image1 == None or image2 == None:
            try:
                image1 = Image.open(r"C:\Screener\tmp\pnl\charts" + f"\{self.i}" + "1min.png")
                image2 = Image.open(r"C:\Screener\tmp\pnl\charts" + f"\{self.i}" + "d.png")
            except:
                pass
        bio1 = io.BytesIO()
        image1.save(bio1, format="PNG")
        bio2 = io.BytesIO()
        image2.save(bio2, format="PNG")
        
        self.window["-IMAGE1-"].update(data=bio1.getvalue())
        self.window["-IMAGE2-"].update(data=bio2.getvalue())
        self.window["-number-"].update(str(f"{self.i + 1} of {len(self.df_traits)}"))

        
    def create(bar):

        tflist = ['1min','d']

        i = bar[0]
        
        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        fw = 30
        fh = 6
        fs = .9
        df = bar[1]
        
        ticker = df.iat[i,0]
        


        for tf in tflist:
            string1 = str(i) + str(tf) + ".png"
            p1 = pathlib.Path("C:/Screener/tmp/pnl/charts") / string1

        
            try:
                datelist = []
                colorlist = []
                for k in range(len(df.iat[i,2])):
                    
                    if tf == 'd':
                        date = df.iat[i,2][k][1].date()
                    else:
                        date = df.iat[i,2][k][1]
                    val = df.iat[i,2][k][2]
                    if val > 0:
                        colorlist.append('g')
                    else:
                        colorlist.append('r')
                    datelist.append(date)
            
                
                df1 = data.get(ticker,tf)
                startdate = df.iat[i,2][0][1]
                enddate = df.iat[i,2][-1][1]
                l1 = data.findex(df1,startdate) - 50
                r1 = data.findex(df1,enddate) + 50
                df1 = df1[l1:r1]
            
                fig, axlist = mpf.plot(df1, type='candle', volume=True, title=str(f'{ticker} , {tf}'), style=s, warn_too_much_data=100000,returnfig = True,figratio = (fw,fh),figscale=fs, panel_ratios = (5,1), mav=(10,20), 
                                       tight_layout = True,vlines=dict(vlines=datelist, colors = colorlist, alpha = .2,linewidths=1))
                ax = axlist[0]    
                ax.set_yscale('log')
                ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                    
                plt.savefig(p1, bbox_inches='tight')
            except:
                shutil.copy(r"C:\Screener\tmp\blank.png",p1)


    def update(self):
        if self.menu == None:
            sg.theme('DarkGrey')
            try:
                self.df_log = pd.read_feather(r"C:\Screener\tmp\pnl\log.feather")
            except:
                self.df_log = pd.DataFrame()
            try:
                self.df_traits = pd.read_feather(r"C:\Screener\tmp\pnl\traits.feather")
            except:
                self.df_traits = pd.DataFrame()
            try:
                self.df_pnl = pd.read_feather(r"C:\Screener\tmp\pnl\pnl.feather")
            except:
                self.df_pnl = pd.DataFrame()
            self.menu = "Log"
        else:
            self.window.close()
        print(self.menu)
        if self.menu == "Log":
            layout = [  
            [(sg.Text("Ticker    ")),sg.InputText(key = 'input-ticker')],
            [(sg.Text("Datetime")),sg.InputText(key = 'input-datetime')],
            [(sg.Text("Shares   ")),sg.InputText(key = 'input-shares')],
            [(sg.Text("Price     ")),sg.InputText(key = 'input-price')],
            [(sg.Text("Setup    ")),sg.InputText(key = 'input-setup')],
            [sg.Button('Clear'),sg.Button('Enter')],
            [sg.Button('Account'), sg.Button('Log'),sg.Button('Traits'),sg.Button('Plot')]]
            self.window = sg.Window(self.menu, layout,margins = (10,10),finalize = True)
        if self.menu == "Account":
            self.window = sg.Window(self.menu, layout,margins = (10,10),finalize = True)
        if self.menu == "Traits":
            layout = [
            [sg.Button('Account'), sg.Button('Log'),sg.Button('Traits'),sg.Button('Plot')]]
            self.window = sg.Window(self.menu, layout,margins = (10,10),finalize = True)
            self.traits(self)
        if self.menu == "Plot":
            layout = [  
             [sg.Image(key = '-IMAGE2-')],
             [sg.Image(key = '-IMAGE1-')],
             [(sg.Text((str(f"{self.i + 1} of {len(self.df_traits)}")), key = '-number-'))],
            [(sg.Text("Ticker  ")),sg.InputText(key = 'input-ticker')],
            [(sg.Text("Date   ")),sg.InputText(key = 'input-datetime')],
            [(sg.Text("Setup  ")),sg.InputText(key = 'input-setup')],
            [(sg.Text("Sort    ")),sg.InputText(key = 'input-sort')],
            [[sg.Button('Prev'),sg.Button('Next'),sg.Button('Load')]],
            [sg.Button('Account'), sg.Button('Log'),sg.Button('Traits'),sg.Button('Plot')]]
            self.window = sg.Window(self.menu, layout,margins = (10,10),finalize = True)
            self.plot(self)


    def loop(self):

        with Pool(6) as self.pool:
            if os.path.exists("C:/Screener/tmp/pnl/charts"):
                shutil.rmtree("C:/Screener/tmp/pnl/charts")
            os.mkdir("C:/Screener/tmp/pnl/charts")
            self.preloadamount = 15
            self.i = 0
            self.menu = None
            self.update(self)
            while True:
                self.event, self.values = self.window.read()
                if self.event == "Traits" or self.event == "Plot" or self.event == "Account" or self.event == "Log":
                    self.menu = self.event
                    self.update(self)
                elif self.event != "":
                    #print(self.menu)
                    if self.menu == "Traits":

                        self.traits(self)
                    elif self.menu == "Plot":
                        self.plot(self)
                    elif self.menu == "Account":
                        self.account(self)
                    elif self.menu == "Log":
                        self.log(self)
if __name__ == "__main__":
    PNL.loop(PNL)




