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


df = pd.read_csv("F:/Screener/11-26-21 orders.csv")
df = df.drop([0, 1, 2])
print(df.head())
dfnew = []
for i in range(len(df)):
    if "FILLED" in df.iloc[i][1]:
        if "-" not in df.iloc[i][0]:
            dfnew.append(df.iloc[i])
dfnew = pd.DataFrame(dfnew)
print(dfnew.head())
dfn = []
dfn = pd.DataFrame(dfn)
for i in range(len(dfnew)):
    ticker = dfnew.iloc[i][0]
    price = dfnew.iloc[i][1].split("$")[1]
    shareSplit = dfnew.iloc[i][3].split(" ")
    shares = None
    for j in range(len(shareSplit)):
        if(shareSplit[j].isnumeric() == True):
            shares = shareSplit[j]
    dateSplit = dfnew.iloc[i][4].split(" ")
    dateS = dateSplit[1].split("\n")
    print(dfnew.iloc[i][4])
    date = dateS[1] + " " + dateSplit[0]
    date = pd.to_datetime(date)
    le = len(dfn)
    dfn.at[le, 'Ticker'] = str(ticker)
    dfn.at[le, 'Datetime'] = date
    dfn.at[le, 'Shares'] = float(shares)
    dfn.at[le, 'Price'] = float(price)
    
    
dfn = pd.DataFrame(dfn)
print(dfn)

dfn.to_feather('C:/Screener/tmp/pnl/log.feather')

