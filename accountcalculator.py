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

class accountcalculator(): 
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

        appleDf = pd.read_feather(r"" + path + "/minute/AAPL.feather")
        orderDf = pd.read_feather("C:/Screener/tmp/log.feather")
        orderDf = orderDf.sort_values(by='Datetime', ascending =True)
        orderDf = orderDf.reset_index()
        firstDateTime = orderDf.at[0, 'Datetime']
        appleIndex = data.findex(appleDf, firstDateTime)
        accdata = appleDf[appleIndex-1:]
        accdata = accdata.drop(axis=1, labels=['open', 'high', 'low', 'close', 'volume'])
        #print(orderDf)
        accdata.loc[appleDf.index[appleIndex-1], cols] = [0, 0, 0, 0, 0, 
                                0, 0, "!", "!", "!"]
        print(accdata)

        for i in range(len(orderDf)-1):
            firstIndex, secondIndex = accountcalculator.sectionIndexes(orderDf, accdata, i)
            accountcalculator.nextSection(accdata, firstIndex, secondIndex, orderDf, i)
            
    def sectionIndexes(orderDf, accDf, currentOrderIndex):
        df = orderDf
        firstIndex = data.findex(accDf, orderDf.at[currentOrderIndex, 'Datetime'])
        secondIndex = data.findex(accDf, orderDf.at[currentOrderIndex+1, 'Datetime'])
        #print(f"{firstIndex} {secondIndex}")
        return firstIndex, secondIndex

    def nextSection(accdata, index1, index2, orderDf, orderIndex):
        if(orderDf.at[orderIndex, 'Ticker'] == 'Deposit'):
            index1time = accdata.index[index1]
            accdata.at[index1time, 'Cash'] = float(accdata.iloc[(index1)-1]['Cash']) + float(orderDf.iloc[orderIndex]['Price'])
        else:
            if(accdata.iloc[(index1)-1]['Positions'] == "!"):
                print("TEST")
                index1time = accdata.index[index1]
                accdata.at[index1time, 'Positions'] = str(orderDf.iloc[orderIndex]['Ticker'])
                accdata.at[index1time, 'Shares'] = orderDf.iloc[orderIndex]['Shares']
                accdata.at[index1time, 'Average'] = orderDf.iloc[orderIndex]['Price']
        #print(accdata[(index1):index1+1])
        for i in range((index2-index1)+1):
            accountcalculator.nextRow()

    def nextRow():
        pass
    







if __name__ == "__main__":
    accountcalculator().initializeAccount()
