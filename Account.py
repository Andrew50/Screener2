
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
import numpy
import statistics
from tqdm import tqdm

class Account:

    def update(self,date):


        del_index = data.findex(self.df_pnl,date) 
        df2 = self.df_pnl[:del_index]
        df = Account.calcaccount(self,date)
      
        self.df_pnl = pd.concat([df2.reset_index(),df]).sort_values(by='datetime')
        
        #df.to_feather(r"C:\Screener\tmp\pnl\pnl.feather")
        self.df_pnl = self.df_pnl.set_index('datetime',drop = True)
       





    def calcaccount(self,date = None):
        df_aapl = data.get('AAPL','1min')

        #initial conditions
        if date != None:
            
            index = data.findex(self.df_pnl,date)
            #index = 0
            
            bar = self.df_pnl.iloc[index]

            pnl = bar['close']
            deposits = bar['deposits']
            positions = bar['positions'].split(',')
            shares = bar['shares'].split(',')
            pos = []
            for i in range(len(shares)):
                ticker = positions[i]
                share = float(shares[i])
                df = data.get(ticker,'1min')
                pos.append([ticker,share,df])


            log_index = data.findex(self.df_log.set_index('Datetime'),date) 
            nex = self.df_log.iloc[log_index]['Datetime']
          
            

        else:
            date = self.df_log.iat[0,1]
            
            pnl = 0
            deposits = 0
            pos = []
            index = 0
            log_index = 0
            nex = date
 
        start_index = data.findex(df_aapl,date)
        date_list = df_aapl[start_index:].index.to_list()
  
        df_list = []
        pbar = tqdm(total=len(date_list))

        for date in date_list:

            pnlvol = 0
            pnlo = pnl
            
            while date > nex:
                remove = False
                skip = False
                ticker = self.df_log.iat[log_index,0]
                shares = self.df_log.iat[log_index,2]
                price = self.df_log.iat[log_index,3]

                if ticker == 'Deposit':
                    deposits += price

                else:
                    pos_index = None
                    for i in range(len(pos)):

                        if pos[i][0] == ticker:
                            
                        
                            pos_index = i
                            pos[i][1] += shares
                       
                            if pos[i][1] == 0:
                                remove = True

                    if pos_index == None:
                        try:
                            df = data.get(ticker,'1min')
                            pos_index = len(pos)
                            data.findex(df,date) + 1
                            pos.append([ticker,shares,df])
                            
                        except:
                            skip = True
                            pass
                    if not skip:
                        df = pos[pos_index][2]
                        ind = data.findex(df,date) - 1
                        c1 = df.iat[ind,3]
                        gosh = (c1 - price)*shares
                        pnl += gosh
                     
                        pnlvol += abs(shares*price)

                        if remove:
                            del pos[pos_index]

                log_index += 1
                try:
                    nex = self.df_log.iat[log_index,1]
                except: 
                    nex = datetime.datetime.now()


            pnlh = pnl
            pnll = pnl
            
            positions = ""
            god_shares = ""
            for i in range(len(pos)):
                ticker = pos[i][0]
                shares = pos[i][1]
                df = pos[i][2]
                index = data.findex(df,date)
                prevc = df.iat[index - 1,3]
                c = df.iat[index,3] 
                o = df.iat[index,0]
                h = df.iat[index,1]
                l = df.iat[index,2]
              
                pnl += (c - prevc) * shares
                pnlh += (h - prevc) * shares
                pnll += (l - prevc) * shares
                pnlo += (o - prevc) * shares
                if i >= 1:
                    positions += "," + (str(ticker))
                    god_shares += "," + (str(shares))
                else:
                    positions += str(ticker)
                    god_shares += str(shares)
            

            add = pd.DataFrame({
                'datetime':[date],
                'open':[pnlo],
                'high':[pnlh],
                'low':[pnll],
                'close':[pnl],
                'volume':[pnlvol],
                'deposits':[deposits],
                'account':[deposits + pnl],
                'positions':[positions],
                'shares':[god_shares]
                })


            #self.df_pnl = pd.concat([self.df_pnl,add])
            df_list.append(add)
            pbar.update(1)


        
        df = pd.concat(df_list).reset_index(drop = True)
     
        #self.df_pnl.set_index('Datetime',drop = True)
        return df 
        

    def account(self,date = None):

        if self.event == "Load":
            tf = self.values['input-timeframe']
            date = self.values['input-datetime']

        else:
            date = None
            tf = 'd'

        if self.df_pnl.empty or self.event == "Recalc":
            df = Account.calcaccount(self)
            df.to_feather(r"C:\Screener\sync\pnl.feather")
            self.df_pnl = df.set_index('datetime',drop = True)

      
        df = self.df_pnl
        if tf == '':
            tf = 'd'
        if tf != "1min":
            logic = {'open'  : 'first','high'  : 'max','low'   : 'min','close' : 'last','volume': 'sum' }
            df = df.resample(tf).apply(logic).dropna()

        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        if os.path.exists("C:/Screener/laptop.txt"): #if laptop
            fw = 30
            fh = 13.8
            fs = 3.4
        else:
            fw = 30
            fh = 18
            fs = 1.8
        string1 = "pnl.png"
        p1 = pathlib.Path("C:/Screener/tmp/pnl") / string1

        fig, axlist = mpf.plot(df, type='candle', volume=True, style=s, warn_too_much_data=100000,returnfig = True,figratio = (fw,fh),figscale=fs, panel_ratios = (5,1), mav=(10,20), tight_layout = True)

        plt.savefig(p1, bbox_inches='tight')
        #plt.show()
        
        bio1 = io.BytesIO()
        image1 = Image.open(r"C:\Screener\tmp\pnl\pnl.png")
        image1.save(bio1, format="PNG")
        self.window["-CHART-"].update(data=bio1.getvalue())






        