
from lib2to3.pgen2.token import PERCENT
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
from Data7 import Data as data

class Traits:


    def update(self,bar):
      
        date = bar[1]
        ticker = bar[0]
        if ticker != 'Deposit':

            #find all trades with same ticker and greater than or equal to date
            
            df = self.df_traits
            df['index'] = df.index
           
            df =df.set_index('datetime',drop = True)
            df = df[df['ticker'] == ticker]


            if not df.empty:
                cutoff = 0
        
                drop_list = []
                for i in range(len(df)):
                    if df.index[i] <= date:
                        cutoff = i
                        break
               
                drop_list = df.reset_index()[:cutoff+1]['index'].to_list()
                i = df.iloc[cutoff]['index']
                gosh = self.df_traits.iloc[i].to_list()
                self.df_traits = self.df_traits.drop(index = drop_list)
                ticker = gosh[0]
                log_date = gosh[1]
                if log_date > date:
                    log_date = date
                logs = self.df_log
                short_logs = logs[logs['Ticker'] == ticker]
                short_logs = short_logs[short_logs['Datetime'] >= log_date]
                short_logs = short_logs.reset_index(drop = True)
 
                df = Traits.calc(self,short_logs)
                self.df_traits = pd.concat([self.df_traits,df])
                self.df_traits = self.df_traits.sort_values(by='Datetime',ascending = False).reset_index(drop = True)
                self.df_traits.to_feather(r"C:\Screener\sync\traits.feather")
   
 
    def calc(self,df):

        pos = []
        df_traits = pd.DataFrame()
        for k in range(len(df)):
            row = df.iloc[k].to_list()
            ticker = row[0]
            if ticker != 'Deposit':
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
                pos[index][3].append([str(x) for x in row])
                shares = prev_share + shares
                if shares == 0:
                    for i in range(len(pos)):
                        if pos[i][0] == ticker:
                            index = i
                            bar = pos[i]
                            add = pd.DataFrame({
            
                            'ticker': [bar[0]],
                            'datetime':[bar[1]],
                            'trades': [bar[3]]
                            
                            })

                            df_traits = pd.concat([df_traits,add])
                            #df_traits.reset_index(inplace = True,drop = True)

                            #self.df_traits
                            del pos[i]
                            break
                else:
                
                    pos[index][2] = shares




        for i in range(len(pos)-1,-1,-1):
           
            index = i
            bar = pos[i]
            add = pd.DataFrame({
            
            'ticker': [bar[0]],
            'datetime':[bar[1]],
            'trades': [bar[3]]
            })

            df_traits = pd.concat([df_traits,add])
            #df_traits.reset_index(inplace = True,drop = True)

           
            del pos[i]
            break

        df_traits = df_traits.sort_values(by='datetime', ascending = False).reset_index(drop = True)
            

        #traits///////////////////////////////////////////////////////////////////////////////////////

        df_list = []
        pbar = tqdm(total=len(df_traits))
        df_vix = data.get('^VIX','d')
        for k in range(len(df_traits)):
            bar = df_traits.iloc[k]
            ticker = bar[0]
            date = bar[1]
            trades = bar[2]
      
           
            openprice = float(trades[0][3])


            #setup
            setup = 'None'
            for i in range(len(trades)):
                if trades[i][4] != 'None':
                    setup = trades[i][4]
                    break

                

            ##size
            size = 0
            maxsize = 0
            shg = 0
            for i in range(len(trades)):
                sh = float(trades[i][2])
                size += sh*float(trades[i][3])
                shg += sh
                if abs(size) > abs(maxsize):
                    maxsize = (size)
                    maxshares = shg

            if shg != 0:
                closed = False
            else:
                closed = True
            

            if closed:
            
                size = maxsize

                ###direction
                if float(trades[0][2]) > 0:
                    direction = 1
                else:
                    direction = -1

                #proift
                pnl = 0
                for i in range(len(trades)):
                    pnl -= float(trades[i][2]) * float(trades[i][3])
             
                try:
                    account_val = self.df_pnl.iloc[data.findex(self.df_pnl,date)]['account']
                except:
                    account_val = self.df_pnl.iloc[-1]['account']
                pnl_pcnt = ((pnl / abs(size)) ) *100
          
                pnl_account = (pnl/ account_val ) * 100


                #theoretical exits

                fb = float(trades[0][3])  *   maxshares
                pnl = -fb
                df = None
                buys = 0
                fs = None
         
                for i in range(len(trades)):
                    price = float(trades[i][3])
                    sh = float(trades[i][2])
                
                    dollars = price * sh
               
                    if dollars*direction < 0:
                        if fs == None:
                            fs = price
                        pnl -= dollars
                    else:
                        buys -= dollars
                    
                fbuy = (pnl/fb) * 100 * direction
                fsell = (fs*maxshares + buys)/size * 100 * direction
                
                   



                if pnl_pcnt < -2:
                    maxloss = pnl_pcnt
                else:
                    maxloss = -2
                h10 = maxloss
                h20 = maxloss
                h50 = maxloss
                d5 = maxloss
                d10 = maxloss
                h10time = 0
                h20time = 0
                h50time = 0
                d5time = 0
                d10time = 0
                run = False



                #arrow list shitt





                arrow_list = []

                for i  in range(len(trades)):

                    sprice = float(trades[i][3])
                    shares = float(trades[i][2])
                    sdate = trades[i][1]
                    if shares > 0:
                        color = 'g'
                        symbol = '^'
                    else:
                        color = 'r'
                        symbol = 'v'

                    arrow_list.append([str(sdate),str(sprice),str(color),str(symbol)])

                if direction > 0:
                    symbol = 'v'
                else:
                    symbol = '^'



                try:
                    hourly = data.get(ticker,'h')
                    daily = data.get(ticker,'d')
                    startd = data.findex(daily,date)
                    if startd != None:
                        run = True
                except FileNotFoundError:
                    pass
                if run:

                    start = data.findex(hourly,date)
                    prices = []
                    if start != None:
                        for i in range(50):
                            prices.append(hourly.iat[i + start - 50,3])
                

                        i = 0
                        while True:
                            close = hourly.iat[start+i,3]
                            low = hourly.iat[start + 1,3]

                            if (h20 != maxloss and h10 != maxloss and h50 != maxloss) or direction*(low/openprice - 1) < -.02:
                                break
                     
                            
                            if direction * close < direction * statistics.mean(prices[-10:]) and h10 == maxloss:
                           
                                h10 = direction*(close/openprice - 1)*100
                                cdate = hourly.index[start + i + 1]
                                h10time = ( cdate- date).total_seconds() / 3600
                                arrow_list.append([str(cdate),str(close),'m',str(symbol)])


                            if direction * close < direction * statistics.mean(prices[-20:]) and h20 == maxloss:
                                cdate = hourly.index[start + i + 1]
                                h20 = direction*(close/openprice - 1)*100
                                h20time = (hourly.index[start + i + 1] - date).total_seconds() / 3600
                                arrow_list.append([str(cdate),str(close),'b',str(symbol)])
                            if direction * close < direction * statistics.mean(prices[-50:]) and h50 == maxloss:
                                cdate = hourly.index[start + i + 1]
                                h50 = direction*(close/openprice - 1)*100
                                h50time = (hourly.index[start + i + 1] - date).total_seconds() / 3600
                                arrow_list.append([str(cdate),str(close),'c',str(symbol)])
                            
                            i += 1
                            prices.append(hourly.iat[start + i,3])



                    
                    start = startd 
                    
                    prices = []
                    for i in range(10):
                        prices.append(daily.iat[i + start - 10,3])
                    i = 0
                    while True:
                        close = daily.iat[start+i,3]
                        low = daily.iat[start+i,3]
                        if (d10 != maxloss and d5 != maxloss) or (direction*(low/openprice - 1) < -.02 and i >= 1):
                            break
                        if direction * close < direction * statistics.mean(prices[-5:]) and d5 == maxloss:
                            cdate = hourly.index[start + i + 1]
                            d5 = direction*(close/openprice - 1)*100
                            d5time = (daily.index[start+i+1] - date).total_seconds() / 3600
                            arrow_list.append([str(cdate),str(close),'y',str(symbol)])
                        if direction * close < direction * statistics.mean(prices[-10:]) and d10 == maxloss:
                            cdate = hourly.index[start + i + 1]
                            d10 = direction*(close/openprice - 1)*100
                            d10time = (daily.index[start+i+1] - date).total_seconds() / 3600
                            arrow_list.append([str(cdate),str(close),'w',str(symbol)])
                        
                        i += 1
                        prices.append(daily.iat[start+i,3])

                
                    df_1min = data.get(ticker,'1min')

                    open_date = daily.index[data.findex(daily,date)]




                    open_index = data.findex(df_1min,open_date)


                    or1 = df_1min.iat[open_index,0]
                    low = 1000000000
                    entered = False
                    i = open_index
                    stopped = False
                    stop = (maxloss/100 + 1) * openprice

                    #theoretical or1 entry and max amount down after trade
                
                    while True:
                        clow = df_1min.iat[i,2]
                        chigh = df_1min.iat[i,1]
                        cdate = df_1min.index[i]
                        #print(f'{cdate} , {open_date}')
                        if (cdate - open_date).days > 2:
                            break
                        if clow < low:
                            low = clow
                        if chigh > or1 and not entered:
                            entered == True
                            risk = (low/or1 - 1) * 100
                            low = 1000000000000
                        #independent from all this other shit above as this is caclulating if you get therotcically stopped 
                        #based on your actuall entry
                        if cdate > date and  clow < stop and not stopped:
                            stopped = True
                            arrow_list.append([str(cdate),str(stop),'b',symbol])
                        i += 1
                    low = (low/or1 - 1)


                else:
                    low = None
                    risk = None



                
                if h10 < maxloss:
                    h10 = maxloss
                if h20 < maxloss:
                    h20 = maxloss
                if h50 < maxloss:
                    h50 = maxloss
                if d5 < maxloss:
                    d5 = maxloss
                if d10 < maxloss:
                    d10 = maxloss




                r10 = h10 - pnl_pcnt
                r20 = h20 - pnl_pcnt
                r50 = h50 - pnl_pcnt
                r5d = d5 - pnl_pcnt
                r10d = d10 - pnl_pcnt
                rfsell = fsell - pnl_pcnt
                rfbuy = fbuy - pnl_pcnt

                try:
                    ivix = data.findex(df_vix,date)
                    vix = df_vix.iat[ivix,0]
                except:
                    vix = 0

                





                add = pd.DataFrame({
                    'ticker': [ticker],
                'datetime':[date],
                'setup':[setup],
                'trades': [trades],
                'pnl':[pnl],
                'account':[pnl_account],




                'percent':[pnl_pcnt],
                'fsell':[fsell],
                'fbuy':[fbuy],
                'p10':[h10],
                'p20':[h20],
                'p50':[h50],
                'p5d':[d5],
                'p10d':[d10],

                'rpercent':[0],
                'rfsell':[rfsell],
                'rfbuy':[rfbuy],
                'r10':[r10],
                'r20':[r20],
                'r50':[r50],
                'r5d':[r5d],
                'r10d':[r10d],
            


                't10d':[d10time],
                't20':[h20time],
                't10':[h10time],
                't50':[h50time],
                't5d':[d5time],
                'arrows':[arrow_list],

                'vix':[vix],
            

                'low':[low],
                'risk':[risk]
                
                
                    
                    })
         
                df_list.append(add)
                pbar.update(1)




        df = pd.concat(df_list)
        df = df.reset_index(drop = True)
        #df.to_feather(r"C:\Screener\tmp\pnl\traits.feather")
        
        return df.sort_values(by='datetime',ascending = False)









            
            #df.to_feather(r"C:\Screener\tmp\pnl\traits.feather")
        

            #self.df_traits.plot(x=self.event, y="perf", kind="scatter")
        '''
        ten = [i for i in self.df_traits['p10'].to_list() if i > 0]
        twenty = [i for i in self.df_traits['p20'].to_list() if i > 0]
        fifty = [i for i in self.df_traits['p50'].to_list() if i > 0]

        bins = 20#numpy.linspace(-10, 10, 100)
            
        plt.hist(ten, bins,alpha=0.35,ec='black', label='10')
        plt.hist(twenty, bins,alpha=0.35, ec='black',label='20')
        plt.hist(fifty, bins, alpha=0.35, ec='black',label='50') 
        '''


    def traits(self):

        if self.df_traits.empty or self.event == 'Recalc':

            self.df_traits = pd.DataFrame()
            
            #df = self.df_log.sort_values(by='Datetime')
            self.df_traits = Traits.calc(self,self.df_log)
            self.df_traits.to_feather(r"C:\Screener\sync\traits.feather")

        bins = 50
        size = (49,25)
        try:
            inp = self.values['input-trait']
        except:
            inp = 'account'
        try:
            plt.clf()
            fifty = self.df_traits[inp].to_list()
            plt.hist(fifty, bins, alpha=1, ec='black',label='Percent') 
            plt.gcf().set_size_inches(size)
            plt.legend(loc='upper right')
            string1 = "traits.png"
            p1 = pathlib.Path("C:/Screener/tmp/pnl") / string1
                
            plt.savefig(p1,bbox_inches='tight')
                
            bio1 = io.BytesIO()
            image1 = Image.open(r"C:\Screener\tmp\pnl\traits.png")
            image1.save(bio1, format="PNG")
            self.window["-CHART-"].update(data=bio1.getvalue())
            #plt.show()
        except KeyError:
            pass
        

            #for k in range(len(self.df_traits)):



        #self.df_traits.to_feather(r"C:\Screener\tmp\pnl\traits.feather")

    
