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
    if os.path.exists("F:/Screener/Ffile.txt"):
        path = "F:/Screener"
    else: 
        path = "C:/Screener"
    def initializeAccount(): 
        data = None
        if os.path.exists("C:/Screener/pnlData.feather") is True:
            data = pd.read_feather("C:/Screener/pnlData.feather")
        else:
            data = pd.DataFrame()

        appleDf = pd.read_feather(r"" + path + "/minute/AAPL.feather")
        orderDf = None
        try:
            orderDf = pd.read_feather("C:/Screener/tmp/log.feather")
        except:
            print("No log file found!!")

        firstDateTime = orderDf.iloc[0]['Datetime']







if __name__ == "__main__":

