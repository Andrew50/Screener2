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


class Plot:
    def plot(self):
        
        if self.event == 'Load':
            scan = pd.read_feather(r"C:\Screener\sync\traits.feather")
            dt = self.values['input-datetime']

            ticker = self.values['input-ticker']
            
            setup = self.values['input-setup']
            sort = self.values['input-sort']
            print(dt)

            if ticker  != "":
                scan = scan[scan['Ticker'] == ticker]
            
            

            if setup  != "":
                scan = scan[scan['Setup'] == setup]
     
            if len(scan) < 1:
                sg.Popup('No Setups Found')
                return
            

            if sort != "":
                try:
                    scan = scan.sort_values(by=[sort], ascending=False)
                except KeyError:
                    sg.Popup('Not a Trait')
                    return

            self.df_traits = scan
            if os.path.exists("C:/Screener/tmp/pnl/charts"):
                shutil.rmtree("C:/Screener/tmp/pnl/charts")
            os.mkdir("C:/Screener/tmp/pnl/charts")
            
            if dt != "":

                self.i = data.findex(self.df_traits.set_index('datetime',drop = True),dt,-1)
            else:
                self.i = 0
            print(self.df_traits)
        if self.event == 'Next' :
            if self.i == len(self.df_traits) - 1:
                self.i = 0
            else:
                self.i += 1
        if self.event == 'Prev':
  
            if self.i == 0:
                self.i = len(self.df_traits) - 1
            else:
                self.i -= 1

        
            #i = list(range(len(self.df_traits)))
            #i = list(range(self.preloadamoun))
            


        
        i = list(range(self.i,self.preloadamount+self.i))
        if self.i < 5:
            i += list(range(len(self.df_traits) - 1,len(self.df_traits) - self.preloadamount - 1,-1))
        else:
            i += list(range(self.i,self.i - self.preloadamount,-1))
                

        
  
        arglist = []
        for index in i:
            arglist.append([index,self.df_traits])
        pool = self.pool
        pool.map(Plot.create,arglist)

        image1 = None
        image2 = None


        while image1 == None or image2 == None:
            try:
                image1 = Image.open(r"C:\Screener\tmp\pnl\charts" + f"\{self.i}" + "1min.png")
                image2 = Image.open(r"C:\Screener\tmp\pnl\charts" + f"\{self.i}" + "d.png")
                image3 = Image.open(r"C:\Screener\tmp\pnl\charts" + f"\{self.i}" + "h.png")
            except:
                pass


        #########table shit



        table = []
        bar = self.df_traits.iat[self.i,3]

        maxsize = 0
        size = 0
        for k in range(len(bar)):
            shares = float(bar[k][2]) 

            size += shares
           
            if abs(size) > abs(maxsize):
               
                maxsize = size
      
        for k in range(len(bar)):
                     
            startdate = datetime.datetime.strptime(bar[0][1], '%Y-%m-%d %H:%M:%S')
            date  = datetime.datetime.strptime(bar[k][1], '%Y-%m-%d %H:%M:%S')
            
            shares = round(float(bar[k][2]))
            price = float(bar[k][3])
            try:
                size = round(shares / maxsize * 100)
            except:
                size = 'NA'
            timedelta = (date - startdate)
            if k == 0:
                percent = ""
            else:
                percent = round(float(bar[0][2])*((price / float(bar[0][3])) - 1) * 100 / abs(float(bar[0][2])),2)
            
            table.append([date,shares,price,percent,timedelta,size])

        #tabel2
        table2 = [[],[]]
        print(self.df_traits.iloc[self.i])
        for i in range(6,14):
            table2[0].append(round(self.df_traits.iat[self.i,i],2))
        for i in range(14,22):
            table2[1].append(round(self.df_traits.iat[self.i,i],2))
        '''
        pnl = 0
        for i in range(len(bar)):
            price = float(bar[k][3])
            shares = float(bar[k][2])
            dollars = price*shares
            pnl -= dollars
        '''








        bio1 = io.BytesIO()
        image1.save(bio1, format="PNG")
        bio2 = io.BytesIO()
        image2.save(bio2, format="PNG")
        bio3 = io.BytesIO()
        image3.save(bio3, format="PNG")

        self.window["-IMAGE1-"].update(data=bio1.getvalue())
        self.window["-IMAGE2-"].update(data=bio2.getvalue())
        self.window["-IMAGE3-"].update(data=bio3.getvalue())
        self.window["-number-"].update(str(f"{self.i + 1} of {len(self.df_traits)}"))
        self.window["-table2-"].update(table2)
        self.window["-table-"].update(table)

        
    def create(bar):
        i = bar[0]

        if True: #(os.path.exists(r"C:\Screener\tmp\pnl\charts" + f"\{i}" + "1min.png") == False):

        

            tflist = ['1min','h','d']

            i = bar[0]
            #print(i)
            mc = mpf.make_marketcolors(up='g',down='r')
            s  = mpf.make_mpf_style(marketcolors=mc)

            if os.path.exists("C:/Screener/laptop.txt"): #if laptop
                fw = 24
                fh = 13
                fs = 1.95

            else:
                fw = 15
                fh = 6
                fs = .85
            df = bar[1]
        
            ticker = df.iat[i,0]
        


            for tf in tflist:
                string1 = str(i) + str(tf) + ".png"
                p1 = pathlib.Path("C:/Screener/tmp/pnl/charts") / string1

        
                try:
                    datelist = []
                    colorlist = []
                    trades = []
                    for k in range(len(df.iat[i,3])):
                        date = datetime.datetime.strptime(df.iat[i,3][k][1], '%Y-%m-%d %H:%M:%S')
                        if tf == 'd':
                            date = date.date()
                    
                        val = float(df.iat[i,3][k][2])
                        if val > 0:
                            colorlist.append('g')
                            add = pd.DataFrame({
                                    'Datetime':[df.iat[i,3][k][1]], 
                                    'Symbol':[df.iat[i,3][k][0]],
                                    'Action':"Buy",
                                    'Price':[float(df.iat[i,3][k][3])]
                                    })
                            trades.append(add)
                        else:
                            colorlist.append('r')
                            add = pd.DataFrame({
                                    'Datetime':[df.iat[i,3][k][1]], 
                                    'Symbol':[df.iat[i,3][k][0]],
                                    'Action':"Sell",
                                    'Price':[float(df.iat[i,3][k][3])]
                                    })
                            trades.append(add)
                        datelist.append(date)
              
                
                    df1 = data.get(ticker,tf)
                    startdate = df.iat[i,3][0][1]
                    enddate = df.iat[i,3][-1][1]
                    l1 = data.findex(df1,startdate) - 50
                    r1 = data.findex(df1,enddate) + 50
                    df1 = df1[l1:r1]

                    
                    tradeDf = pd.concat(trades).reset_index(drop = True)
                    tradeDf['Datetime'] = pd.to_datetime(tradeDf['Datetime'])
                    times = df1.index.to_list()
                    tradelist = []
                    for t in range(len(tradeDf)):
                        tradeTime = tradeDf.iloc[t]['Datetime']
                        for q in range(len(times)):
                        
                            if(q+1 != len(times)):
                                if(times[q+1] > tradeTime):
                                    add = pd.DataFrame({
                                        'Datetime':[times[q]],
                                        'Symbol':[tradeDf.iloc[t]['Symbol']],
                                        'Action':[tradeDf.iloc[t]['Action']],
                                        'Price':[tradeDf.iloc[t]['Price']]
                                        })
                                    tradelist.append(add)
                                    break
                    df2 = pd.concat(tradelist).reset_index(drop = True)
                    buy = df2[df2['Action'] == 'Buy']
                    buy['Datetime'] = pd.to_datetime(buy['Datetime'])
                    buy = buy.sort_values(by=['Datetime'])
                    sell = df2[df2['Action'] == 'Sell']
                    sell['Datetime'] = pd.to_datetime(sell['Datetime'])
                    sell = sell.sort_values(by=['Datetime'])
                    buy["TradeDate_count"] = buy.groupby("Datetime").cumcount() + 1
                    sell["TradeDate_count"] = sell.groupby("Datetime").cumcount() + 1
                    newbuys = (buy.pivot(index='Datetime', columns='TradeDate_count', values="Price")
                            .rename(columns="price{}".format)
                            .rename_axis(columns=None))
                    newsells = (sell.pivot(index='Datetime', columns='TradeDate_count', values="Price")
                            .rename(columns="price{}".format)
                            .rename_axis(columns=None))
                    timesdf = []
                    test = df1.index.to_list()
                    for _ in range(len(df1)):
                         ad = pd.DataFrame({
                                'Datetime':[test[_]]
                                })
                         timesdf.append(ad)
                    mainindidf = pd.concat(timesdf).reset_index(drop = True)
                    mainindidf = mainindidf.set_index('Datetime', drop=True)
                    buyseries = mainindidf.merge(newbuys, how='left', left_index=True, right_index=True)[newbuys.columns]
                    sellseries =  mainindidf.merge(newsells, how='left', left_index=True, right_index=True)[newsells.columns]
                    for rr in range(len(buyseries)):
                        print(buyseries.iloc[rr])
                    
                    apds = [mpf.make_addplot(mainindidf)]
                    if buyseries.isnull().values.all(axis=0)[0]:  ## test if all cols have null only
                        pass
                    else:  
                        apds.append(mpf.make_addplot(buyseries,type='scatter',markersize=20,marker='^', color='g'))
                        print("W")
                    if sellseries.isnull().values.all(axis=0)[0]:  ## test if all cols have null only
                        pass
                    else:  
                        apds.append(mpf.make_addplot(sellseries,type='scatter',markersize=20,marker='v', color='r'))
                    
                    fig, axlist = mpf.plot(df1, type='candle', volume=True, 
                                           title=str(f'{ticker} , {tf}'), 
                                           style=s, warn_too_much_data=100000,returnfig = True,figratio = (fw,fh),
                                           figscale=fs, panel_ratios = (5,1), mav=(10,20), 
                                           tight_layout = True, addplot=apds)
                    # vlines=dict(vlines=datelist, colors = colorlist, alpha = .2,linewidths=1)
                    ax = axlist[0]
                    #for k in range(len(df.iat[i,2])):
                     #   ax.text()




                    ax.set_yscale('log')
                    ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                    
                    plt.savefig(p1, bbox_inches='tight')
                except TimeoutError:
                    shutil.copy(r"C:\Screener\tmp\blank.png",p1)
                    print("lolol")
                    
