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
        #print(appleDf.iloc[appleIndex])
        accdata = appleDf[appleIndex-1:]
        accdata = accdata.drop(axis=1, labels=['open', 'high', 'low', 'close', 'volume'])
        print(orderDf)
        accdata.loc[appleDf.index[appleIndex-1], cols] = ['0', '0', '0', '0', '0', 
                                '0', '0', '', '', '']
        print(accdata)
        for i in range(len(orderDf)-1):
            firstIndex, secondIndex = accountcalculator.sectionIndexes(orderDf, accdata, i)
            if(i == 0): 
                firstIndex = 0
            accountcalculator.nextSection(accdata, firstIndex, secondIndex, orderDf, i)
            
    def sectionIndexes(orderDf, accDf, currentOrderIndex):
        df = orderDf
        firstIndex = data.findex(accDf, orderDf.at[currentOrderIndex, 'Datetime'])
        secondIndex = data.findex(accDf, orderDf.at[currentOrderIndex+1, 'Datetime'])
        return firstIndex, secondIndex

    def nextSection(accdata, index1, index2, orderDf, orderIndex):
        if(orderDf.at[orderIndex, 'Ticker'] == 'Deposit'):
            accdata.at[index1, 'Cash'] = float(accdata.at[index1, 'Cash']) + float(orderDf.at[orderIndex, 'Price'])
            print('test')
    def nextRow():
        pass
    







if __name__ == "__main__":
    accountcalculator().initializeAccount()
