import os 
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
    def Intraday():
        options = Options()
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
        FireFoxDriverPath = os.path.join(os.getcwd(), 'Drivers', 'geckodriver.exe')
        FireFoxProfile = webdriver.FirefoxProfile()
        FireFoxProfile.set_preference("General.useragent.override", user_agent)
        browser = webdriver.Firefox(options=options, executable_path=FireFoxDriverPath)
        browser.implicitly_wait(7)
        browser.maximize_window()
        url = "https://www.tradingview.com/screener/"
        browser.get(url)
        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        #creating the csv file
        browser.find_element(By.XPATH, '//div[@data-name="screener-refresh"]').click()
        browser.find_element(By.XPATH, '//div[@data-name="screener-refresh"]').click()
        download_screener_data = browser.find_element(By.XPATH, '//div[@data-name="screener-export-data"]')
        download_screener_data.click()
        time.sleep(2)
        today = str(datetime.date.today())
        downloaded_file = r"C:\Downloads\america_" + today + ".csv"
        new_name = r"C:\Downloads\screener_data_intraday.csv"
        os.rename(downloaded_file, new_name)
        os.replace(r"C:\Downloads\screener_data_intraday.csv", r"C:\Screener\tmp\screener_data_intraday.csv")
        screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data_intraday.csv")
        time.sleep(0.1)

        numTickers = len(screener_data)
        #Changing ARCA into AMEX
        screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
        numTickers = len(screener_data)
        for i in range(numTickers):
            if str(screener_data.iloc[i]['Exchange']) == "NYSE ARCA":
                screener_data.at[i, 'Exchange'] = "AMEX"

        #Loop stocks in screen
        for i in range(numTickers):
            tick = str(screener_data.iloc[i]['Ticker'])
            exchange = str(screener_data.iloc[i]['Exchange'])
            change = round(screener_data.iloc[i]["Change 1m, %"], 2)
            dayChange = round(screener_data.iloc[i]['Change %'], 2)
            changeFromOpen = screener_data.iloc[i]['Change from Open']
            openValue = screener_data.iloc[i]['Open']
            currPrice = screener_data.iloc[i]['Price']
            volume = screener_data.iloc[i]['Volume']
            Gainers()
            time.sleep(60)
            #dM("NEW BATCH !", "Time: " + str(datetime.datetime.now()))
            counter = counter + 1
    
            if(change > 2.5 and volume > 250000 and volume*currPrice > 750000 and currPrice > 1.2):
                data_minute_100 = tv.get_hist(tick, exchange, interval=Interval.in_1_minute, n_bars=100)
                print(data_minute_100.head(1))
                ourpath = pathlib.Path("C:/Screener/tmp") / "test3.png"
                openCandlePrice = float(data_minute_100.iloc[len(data_minute_100)-1][1])
                changePrice = round(float(currPrice - openCandlePrice), 2)
                marketCap = float(screener_data.iloc[i]['Market Capitalization'])
                marketCapText = round((marketCap / 1000000000), 2)
                relativeVolAtTime = round(screener_data.iloc[i]['Relative Volume at Time'], 1)
                mpf.plot(data_minute_100, type='candle', volume=True, title=tick, style=s, savefig=ourpath)
                dM.sendDiscordEmbedIntraday(tick + f" {openCandlePrice} >> Current: {currPrice} ▲ {changePrice} ({change}%)", f"Intraday % Gaining Setup, Volume: {volume}, RelVol: {relativeVolAtTime}x, MCap: ${marketCapText}B")
                dM.sendDiscordIntradayPost('tmp/test3.png')
            if(dayChange > 15 and volume > 500000 and volume*currPrice > 7500000 and currPrice > 1.2 and (counter % 5 == 0)): 
                data_minute_100 = tv.get_hist(tick, exchange, interval=Interval.in_1_minute, n_bars=250)
                print(data_minute_100.head(1))
                ourpath = pathlib.Path("C:/Screener/tmp") / "test3.png"
                
                marketCap = float(screener_data.iloc[i]['Market Capitalization'])
                marketCapText = round((marketCap / 1000000000), 2)
                relativeVolAtTime = round(screener_data.iloc[i]['Relative Volume at Time'], 1)
                mpf.plot(data_minute_100, type='candle', volume=True, title=tick, style=s, savefig=ourpath)
                dM.sendDiscordEmbedGainers(tick + f" {openValue} >> {currPrice} ▲ {changeFromOpen} ({dayChange}%)", f"Top Gainer, Volume: {volume}, RelVol: {relativeVolAtTime}x, MCap: ${marketCapText}B")
                dM.sendDiscordGainersPost('tmp/test3.png')
    screen.Daily 
    Intraday()


