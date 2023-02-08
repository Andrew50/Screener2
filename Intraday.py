﻿import os 
import time 
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from tvDatafeed import TvDatafeed, Interval
import statistics
import mplfinance as mpf
import matplotlib as mpl
import pathlib
import math
from Screen import Screen as screen
from discordManager import discordManager as dM
class Intraday:
    def runIntraday(tvlog, brows):
        br = brows
        #screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
        tvr = tvlog
        if(tvr == None):
            tvr = screen.logInScrapper()
        br = screen.runIntradayScan(br)
        screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data_intraday.csv")
        numTickers = len(screener_data)
        for i in range(numTickers):
            tick = str(screener_data.iloc[i]['Ticker'])
            exchange = str(screener_data.iloc[i]['Exchange'])
            change = round(screener_data.iloc[i]["Change 1m, %"], 2)
            dayChange = round(screener_data.iloc[i]['Change %'], 2)
            changeFromOpen = screener_data.iloc[i]['Change from Open']
            openValue = screener_data.iloc[i]['Open']
            currPrice = screener_data.iloc[i]['Price']
            volume = screener_data.iloc[i]['Volume']
            tick = str(screener_data.iloc[i]['Ticker'])
            pmChange = screener_data.iloc[i]['Pre-market Change']
            currPrice = screener_data.iloc[i]['Price']
            volume = screener_data.iloc[i]['Volume']
            dolVol = screener_data.iloc[i]['Volume*Price']
            marketCap = float(screener_data.iloc[i]['Market Capitalization'])
            relativeVolAtTime = round(screener_data.iloc[i]['Relative Volume at Time'], 1)
            print(tick)
            Intraday.Gainers(tvr, tick, dolVol, volume, currPrice, marketCap, relativeVolAtTime,change,dayChange,openValue, changeFromOpen, exchange)
            
        return tvr, br
            #dM("NEW BATCH !", "Time: " + str(datetime.datetime.now()))

    def Gainers(tvlogt, tick, dolVol, volume, currPrice, marketCap, relativeVolAtTime,change,dayChange,openValue,changeFromOpen, exchange):
        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        if(change > 2.5 and volume > 250000 and dolVol > 750000 and currPrice > 1.2):
            data_100 = tvlogt.get_hist(tick, exchange, interval=Interval.in_1_minute, n_bars=100)
            ourpath = pathlib.Path("C:/Screener/tmp") / "test3.png"
            openCandlePrice = float(data_100.iloc[len(data_100)-1][1])
            changePrice = round(float(currPrice - openCandlePrice), 2)
            
            marketCapText = round((marketCap / 1000000000), 2)
            
            mpf.plot(data_100, type='candle', volume=True, title=tick, style=s, savefig=ourpath)
            dM.sendDiscordEmbedIntraday(tick + f" {openCandlePrice} >> Current: {currPrice} ▲ {changePrice} ({change}%)", f"Intraday % Gaining Setup, Volume: {volume}, RelVol: {relativeVolAtTime}x, MCap: ${marketCapText}B")
            dM.sendDiscordIntradayPost('tmp/test3.png')

        if(dayChange > 15 and volume > 500000 and dolVol > 7500000 and currPrice > 1.2 ):#and (counter % 5 == 0)): 
            data_100 = tvlogt.get_hist(tick, exchange, interval=Interval.in_1_minute, n_bars=100)
            ourpath = pathlib.Path("C:/Screener/tmp") / "test3.png"
            marketCapText = round((marketCap / 1000000000), 2)
            
            mpf.plot(data_100, type='candle', volume=True, title=tick, style=s, savefig=ourpath)
            dM.sendDiscordEmbedGainers(tick + f" {openValue} >> {currPrice} ▲ {changeFromOpen} ({dayChange}%)", f"Top Gainer, Volume: {volume}, RelVol: {relativeVolAtTime}x, MCap: ${marketCapText}B")
            dM.sendDiscordGainersPost('tmp/test3.png')
    
    def Pops()
    #screen.Daily 
    #Intraday()

tradingView, br = Intraday.runIntraday(None, None)
print(tradingView)
print(br)
