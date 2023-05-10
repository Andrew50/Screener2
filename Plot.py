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
            scan = pd.read_feather(r"C:\Screener\tmp\pnl\traits.feather")


            ticker = self.values['input-ticker']
            dt = self.values['input-datetime']
            setup = self.values['input-setup']
            sort = self.values['input-sort']


            if ticker  != "":
                scan = scan[scan['Ticker'] == ticker]
            
            if dt  != "":
                scan = scan[scan["Datetime"] == dt]

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
            self.i = 0
        
        if self.event == 'Next' :
            if self.i == len(self.df_traits) - 1:
                return
            self.i += 1
        if self.event == 'Prev':
            if self.i == 0:
                return
            self.i -= 1

        
            i = list(range(len(self.df_traits)))
            #i = list(range(self.preloadamoun))
            


        if self.i == 0:
            if len(self.df_traits) < self.preloadamount:
                i = list(range(len(self.df_traits)))
            else:
                i = list(range(self.preloadamount))

        else:
            if self.i + self.preloadamount < len(self.df_traits):
                i = []
            else:
                i = [self.i + self.preloadamount - 1]
               
        pool = self.pool
  
        arglist = []
        for index in i:
            arglist.append([index,self.df_traits])
        pool.map_async(Plot.create,arglist)

        image1 = None
        image2 = None


        while image1 == None or image2 == None:
            try:
                image1 = Image.open(r"C:\Screener\tmp\pnl\charts" + f"\{self.i}" + "1min.png")
                image2 = Image.open(r"C:\Screener\tmp\pnl\charts" + f"\{self.i}" + "d.png")
            except:
                pass


        #########table shit



        table = []
        bar = self.df_traits.iat[self.i,3]
        
        for k in range(len(bar)):
                     
            
            date  = datetime.datetime.strptime(bar[k][1], '%Y-%m-%d %H:%M:%S')
            
            shares = float(bar[k][2])
            price = float(bar[k][3])

            if k == 0:
                percent = ""
            else:
                percent = round(float(bar[0][2])*((price / float(bar[0][3])) - 1) * 100 / abs(float(bar[0][2])),2)
            
            table.append([date,shares,price,percent])


        bio1 = io.BytesIO()
        image1.save(bio1, format="PNG")
        bio2 = io.BytesIO()
        image2.save(bio2, format="PNG")

        self.window["-IMAGE1-"].update(data=bio1.getvalue())
        self.window["-IMAGE2-"].update(data=bio2.getvalue())
        self.window["-number-"].update(str(f"{self.i + 1} of {len(self.df_traits)}"))
        self.window["-table-"].update(table)

        
    def create(bar):

        tflist = ['1min','d']

        i = bar[0]
        
        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        fw = 30
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
                for k in range(len(df.iat[i,3])):
                    date = datetime.datetime.strptime(df.iat[i,3][k][1], '%Y-%m-%d %H:%M:%S')
                    if tf == 'd':
                        date = date.date()
                    
                    val = float(df.iat[i,3][k][2])
                    if val > 0:
                        colorlist.append('g')
                    else:
                        colorlist.append('r')
                    datelist.append(date)
            
                
                df1 = data.get(ticker,tf)
                startdate = df.iat[i,3][0][1]
                enddate = df.iat[i,3][-1][1]
                l1 = data.findex(df1,startdate) - 50
                r1 = data.findex(df1,enddate) + 50
                df1 = df1[l1:r1]



                #ap = mpf.make_addplot(0.99*df1['Low'],type='scatter',marker=mymarkers,markersize=45,color=color)
            
                fig, axlist = mpf.plot(df1, type='candle', volume=True, title=str(f'{ticker} , {tf}'), style=s, warn_too_much_data=100000,returnfig = True,figratio = (fw,fh),figscale=fs, panel_ratios = (5,1), mav=(10,20), 
                                       tight_layout = True,vlines=dict(vlines=datelist, colors = colorlist, alpha = .2,linewidths=1))
                ax = axlist[0]
                #for k in range(len(df.iat[i,2])):
                 #   ax.text()




                ax.set_yscale('log')
                ax.yaxis.set_minor_formatter(mticker.ScalarFormatter())
                    
                plt.savefig(p1, bbox_inches='tight')
            except TimeoutError:
                shutil.copy(r"C:\Screener\tmp\blank.png",p1)
