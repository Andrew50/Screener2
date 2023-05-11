
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
    


    def calcaccount(df_pnl,df_log,startdate = None,tf = None,bars = None):





        account = False
        if startdate == 'now':
            account = True

        df_aapl = data.get('AAPL','1min',account = account)
        
        #print(f"{startdate} , {df_aapl.index[-1]}")
        if startdate != 'now' and startdate > df_aapl.index[-1]:
            return df_pnl
        
        if startdate != None:
            if startdate == 'now':
                startdate = df_pnl.index[-1]
                index = -1
            else:
                del_index = data.findex(df_pnl,startdate) 
                df_pnl = df_pnl[:del_index]
                index = data.findex(df_pnl,startdate)
      
        
        

        #initial conditions
       
            
            
            #index = 0
            #print(index)
            if index == None or index >= len(df_pnl):
                index = -1
            bar = df_pnl.iloc[index]

            pnl = bar['close']
            deposits = bar['deposits']
            positions = bar['positions'].split(',')
            shares = bar['shares'].split(',')
            pos = []
         
            for i in range(len(shares)):
               
                ticker = positions[i]
                if ticker != '':
                    share = float(shares[i])
                    df = data.get(ticker,'1min',account = account)
                    pos.append([ticker,share,df])

            try:
                log_index = data.findex(df_log.set_index('Datetime'),startdate) 
                nex = df_log.iloc[log_index]['Datetime']
            except:
                nex = datetime.datetime.now()
          
            

        else:
            date = df_log.iat[0,1]
            
            pnl = 0
            deposits = 0
            pos = []
            index = 0
            log_index = 0
            nex = date
 
        start_index = data.findex(df_aapl,startdate)
        date_list = df_aapl[start_index:].index.to_list()
  
        df_list = []
        pbar = tqdm(total=len(date_list))
        
        for date in date_list:

            pnlvol = 0
            pnlo = pnl
            
            while date > nex:
                remove = False
                skip = False
                ticker = df_log.iat[log_index,0]
                shares = df_log.iat[log_index,2]
                price = df_log.iat[log_index,3]

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
                            df = data.get(ticker,'1min',account = account)
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
                    nex = df_log.iat[log_index,1]
                except: 
                    nex = datetime.datetime.now() + datetime.timedelta(days=10)


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


            #df_pnl = pd.concat([df_pnl,add])
            df_list.append(add)
            pbar.update(1)


        
        df = pd.concat(df_list)
     
        #df_pnl.set_index('Datetime',drop = True)
        if date != None:
            df = pd.concat([df_pnl.reset_index(),df]).sort_values(by='datetime')
        
        df = df.reset_index(drop = True).set_index('datetime',drop = True)
        
        if tf == None:
            return df 
        else:
            return [df,tf,bars]
        

    def account(self,date = None):



            


        if self.event == "Load" or self.event == "Recalc":
            tf = self.values['input-timeframe']
            bars = self.values['input-bars']
            if tf == "":
                tf = 'd'
            if bars == "":
                bars = 300
        else:
            tf = 'd'
            bars = 300

        if self.df_pnl.empty or self.event == "Recalc":
            df = Account.calcaccount(self.df_pnl,self.df_log)
            df.to_feather(r"C:\Screener\sync\pnl.feather")
            self.df_pnl = df.set_index('datetime',drop = True)

        
        df = self.df_pnl
        bar = [df,tf,bars]
        Account.account_plot(bar)
        Account.plot_update(self)
        




    def account_plot(bar):


        
        try:
            df = bar[0]
            tf = bar[1]
            bars = int(bar[2])

            print(df)

            if tf == '':
                tf = 'd'
            if tf != "1min":
                logic = {'open'  : 'first','high'  : 'max','low'   : 'min','close' : 'last','volume': 'sum' }
                df = df.resample(tf).apply(logic).dropna()
            df = df[-bars:]
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
            
        except Exception as e: print(e)
        #plt.show()
        
        
        
        
    def plot_update(self):
        bio1 = io.BytesIO()
        image1 = Image.open(r"C:\Screener\tmp\pnl\pnl.png")
        image1.save(bio1, format="PNG")
        self.window["-CHART-"].update(bio1.getvalue())






        