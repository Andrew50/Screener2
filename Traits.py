
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

class Traits:

    def traits(self):
        
        if self.df_traits.empty:

            self.df_traits = pd.DataFrame()
            pos = []
            self.df_log = self.df_log.sort_values(by='Datetime')
            for k in range(len(self.df_log)):
                row = self.df_log.iloc[k].to_list()
                ticker = row[0]
                if ticker != 'Deposit':
                    shares = row[2]
                    date = row[1]
                    #print(type(date))
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
            

            #traits///////////////////////////////////////////////////////////////////////////////////////

            df_list = []
            pbar = tqdm(total=len(self.df_traits))
            for k in range(len(self.df_traits)):
                bar = self.df_traits.iloc[k]
                ticker = bar[0]
                date = bar[1]
                trades = bar[2]
                #print(trades)
                price = float(trades[0][3])

                ##size
                size = 0
                maxsize = 0
                for i in range(len(trades)):
                    size += float(trades[i][2])*float(trades[i][3])
                    if abs(size) > abs(maxsize):
                        maxsize = abs(size)

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
                #print(type(date))
                account_val = self.df_pnl.iat[data.findex(self.df_pnl,date),7]

                pnl_pcnt = ((pnl / size) ) *100
                #print(f'{pnl} , {size} , {pnl_pcnt}')
                pnl_account = (pnl/ account_val ) * 100


                #theoretical exits
                h10 = 0
                h20 = 0
                h50 = 0
                d5 = 0
                d10 = 0
                h10time = 0
                h20time = 0
                h50time = 0
                d5time = 0
                d10time = 0
                
                try:
                    hourly = data.get(ticker,'h')
                    start = data.findex(hourly,date)
                    prices = []
                    if start != None:
                        for i in range(50):
                            prices.append(hourly.iat[i + start - 50,3])
                

                        i = 0
                        while True:
                            close = hourly.iat[start+i,3]
                            low = hourly.iat[start + 1,3]

                            #print(f"{close} , {statistics.mean(prices[-10:])}")
                            
                            if direction * close < direction * statistics.mean(prices[-10:]) and h10 == 0:
                                #print(f'{type(direction)} , {type(close)} , {type(price)}')
                                h10 = direction*(close/price - 1)*100
                                h10time = (hourly.index[start + i + 1] - date).total_seconds() / 3600
                            if direction * close < direction * statistics.mean(prices[-20:]) and h20 == 0:
                                h20 = direction*(close/price - 1)*100
                                h20time = (hourly.index[start + i + 1] - date).total_seconds() / 3600
                            if direction * close < direction * statistics.mean(prices[-50:]) and h50 == 0:
                                h50 = direction*(close/price - 1)*100
                                h50time = (hourly.index[start + i + 1] - date).total_seconds() / 3600

                            if (h20 != 0 and h10 != 0 and h50 != 0) or direction*(low/price - 1) < -.02:
                                break
                            i += 1
                            prices.append(hourly.iat[start + i,3])

                except FileNotFoundError:
                    pass




                #final concat
                
                add = pd.DataFrame({
                    'Ticker': [ticker],
                'Datetime':[date],
                'Trades': [trades],
                'pnl':[pnl],
                'percent':[pnl_pcnt],
                'account':[pnl_account],
                'p10':[h10],
                't10':[h10time],
                'p20':[h20],
                't20':[h20time],
                'p50':[h50],
                't50':[h50time]
                
                    
                    })
         
                df = df_list.append(add)
                pbar.update(1)




            df = pd.concat(df_list)
            df = df.reset_index(drop = True)
            df.to_feather(r"C:\Screener\tmp\pnl\traits.feather")
            self.df_traits = df
            
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
        bins = 50
        try:
            inp = self.values['input-trait']
        except:
            inp = 'account'
        try:
            plt.clf()
            fifty = self.df_traits[inp].to_list()
            plt.hist(fifty, bins, alpha=1, ec='black',label='Percent') 
            plt.gcf().set_size_inches(28, 14)
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

    
