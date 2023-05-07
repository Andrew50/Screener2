from ast import Delete, Str
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


from Data7 import Data as data

class accountcalculator: 


    def account(self):


        if self.event == "Load":
            tf = self.values['input-timeframe']
            date = self.values['input-datetime']

        else:
            date = None
            tf = 'd'


        if self.df_pnl == None:
            self.df_pnl = data.get('COIN','1min')
            #accountcalculator.accountcalcultor(self)

        
        
        
        df = self.df_pnl
        if tf == '':
            tf = 'd'
        if tf != "1min":
            logic = {'open'  : 'first',
                            'high'  : 'max',
                            'low'   : 'min',
                            'close' : 'last',
                            'volume': 'sum' }
            df = df.resample(tf).apply(logic).dropna()

        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        fw = 30
        fh = 12
        fs = 1.8
        string1 = "pnl.png"
        p1 = pathlib.Path("C:/Screener/tmp/pnl") / string1

        fig, axlist = mpf.plot(df, type='candle', volume=True, style=s, warn_too_much_data=100000,returnfig = True,figratio = (fw,fh),figscale=fs, panel_ratios = (5,1), mav=(10,20), 
                tight_layout = True)

        
        plt.savefig(p1, bbox_inches='tight')
        bio1 = io.BytesIO()
        image1 = Image.open(r"C:\Screener\tmp\pnl\pnl.png")
        image1.save(bio1, format="PNG")
        self.window["-CHART-"].update(data=bio1.getvalue())

    def accountcalcultor(self):


        path = ""
        cols = ['Net Open', 'Net High', 'Net Low', 'Net Close',
        'Dollar Vol', 'Acc Value', 'Cash', 'Positions', 'Shares',
        'Average']
        if os.path.exists("F:/Screener/Ffile.txt"):
            path = "F:/Screener"
        else: 
            path = "C:/Screener"
        def initializeAccount(self): 
            cols = accountcalculator.cols
            path = accountcalculator.path
            accdata = None
            if os.path.exists("C:/Screener/pnlData.feather") is True:
                accdata = pd.read_feather("C:/Screener/pnlData.feather")
            else:
                accdata = pd.DataFrame()

        appleDf = data.get('AAPL','1min')
        orderDf = pd.read_feather("C:/Screener/tmp/log.feather").sort_values(by='Datetime', ascending =True).reset_index()
      
        firstDateTime = orderDf.at[0, 'Datetime'] 
        appleIndex = data.findex(appleDf, firstDateTime)
        accdata = appleDf[appleIndex-1:]
        accdata = accdata.drop(axis=1, labels=['open', 'high', 'low', 'close', 'volume'])
        #print(orderDf)
        accdata.loc[appleDf.index[appleIndex-1], cols] = [0, 0, 0, 0, 0, 
                                0, 0, "!", "!", "!"]
        #print(accdata)

        for i in range(len(orderDf)-1):
            firstIndex, secondIndex = accountcalculator.sectionIndexes(orderDf, accdata, i)
            accdata = accountcalculator.nextSection(accdata, firstIndex, secondIndex, orderDf, i)
            if(i % 2 == 0):
                accdata.to_csv(path + '/' + "testest" + ".csv")
            
    def sectionIndexes(orderDf, accDf, currentOrderIndex):
        df = orderDf
        print(df)
        firstIndex = data.findex(accDf, orderDf.at[currentOrderIndex, 'Datetime'])
        secondIndex = data.findex(accDf, orderDf.at[currentOrderIndex+1, 'Datetime'])
        #print(f"{firstIndex} {secondIndex}")
        return firstIndex, secondIndex

    def nextSection(accdata, index1, index2, orderDf, orderIndex):
        path = accountcalculator.path

        if(orderDf.at[orderIndex, 'Ticker'] == 'Deposit'):
            print(f"{index1} {index2}")
            for i in range(index2-index1):
                indextime = accdata.index[index1+i]
                accdata.at[indextime, 'Cash'] = float(accdata.iloc[(index1)-1]['Cash']) + float(orderDf.iloc[orderIndex]['Price'])
                accdata.at[indextime, 'Positions'] = accdata.iloc[(index1)-1]['Positions']
                accdata.at[indextime, 'Shares'] = accdata.iloc[(index1)-1]['Shares']
                accdata.at[indextime, 'Average'] = accdata.iloc[(index1)-1]['Average']
        else:
            prevCash = float(accdata.iloc[(index1)-1]['Cash'])
            newCash = prevCash - (orderDf.iloc[orderIndex]['Shares'] * orderDf.iloc[orderIndex]['Price'])
            for i in range(index2-index1):
                indextime = accdata.index[index1+i]
                accdata.at[indextime, 'Cash'] = newCash
            if(accdata.iloc[(index1)-1]['Positions'] == "!"):
                for j in range((index2-index1)):
                    indextime = accdata.index[index1+j]
                    accdata.at[indextime, 'Positions'] = str(orderDf.iloc[orderIndex]['Ticker']) 
                    accdata.at[indextime, 'Shares'] = str(orderDf.iloc[orderIndex]['Shares']) 
                    accdata.at[indextime, 'Average'] = str(orderDf.iloc[orderIndex]['Price']) 
        
            else:
                positions = accdata.iloc[(index1)-1]['Positions'].split(":")
                shares = str(accdata.iloc[(index1)-1]['Shares']).split(":")
                for i in range(len(positions)):
                    if(positions[i] == ""): 
                        del positions[i]
                        del shares[i]
                print(positions)
                print(shares)

                ticker = orderDf.iloc[orderIndex]['Ticker']
                if ticker in positions: 
                    index = positions.index(ticker)
                    shares[index] = float(shares[index]) + orderDf.iloc[orderIndex]['Shares']
                    if(shares[index] == 0):
                        del positions[index]
                        del shares[index]
    
       
                else: 
                    positions.append(ticker)
                    shares.append(orderDf.iloc[orderIndex]['Shares'])
                placeholderP = ""
                placeholderS = ""
                for i in range(len(positions)):
                    placeholderP = placeholderP + positions[i] + ":"
                    placeholderS = placeholderS + str(shares[i]) + ":"
                for i in range((index2-index1)):
                    indextime = accdata.index[index1+i]
                    accdata.at[indextime, 'Positions'] = placeholderP
                    accdata.at[indextime, 'Shares'] = placeholderS
                    accdata.at[indextime, 'Average'] = "Test"           
        if(accdata.iloc[(index1)]['Positions'] != "!"):
            positionsDataFrames = []
            positions = str(accdata.iloc[(index1)]['Positions']).split(":")
            for i in range(len(positions)-1):
                print(positions[i] + "WERWER")
                if(os.path.exists(path + '/minute/' + positions[i] + ".feather")):
                    posDf = pd.read_feather(r"" + path + '/minute/' + positions[i] + ".feather")
                    positionsDataFrame = positionsDataFrames.append(posDf)
            for k in range((index2-index1)):
                accountcalculator.nextRow(accdata, positionsDataFrames, index1+k)
        return accdata

    def nextRow(accdata, positionsDataFrames, index):
        pass
    







if __name__ == "__main__":
    accountcalculator.account().initializeAccount()
