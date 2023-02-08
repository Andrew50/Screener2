import os 
import time 
import selenium
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

from discordManager import discordManager as dM


class Screen:
    def runDailyScan():

        browser = Screen.startFirefoxSession()

        time.sleep(0.5) 
        browser.find_element(By.XPATH, '//div[@data-name="screener-filter-sets"]').click()
        time.sleep(0.25)
        browser.find_element(By.XPATH, '//span[@class="js-filter-set-name"]').click()
        time.sleep(0.25)
        sortRVol = browser.find_element(By.XPATH, '//div[@data-field="relative_volume_intraday.5"]')
        sortRVol.click()

        #creating the csv file
        download_screener_data = browser.find_element(By.XPATH, '//div[@data-name="screener-export-data"]')
        download_screener_data.click()
        time.sleep(1.5)
        today = str(datetime.date.today())
        downloaded_file = r"C:\Downloads\america_" + today + ".csv"
        new_name = r"C:\Downloads\screener_data.csv"
        os.rename(downloaded_file, new_name)
        os.replace(r"C:\Downloads\screener_data.csv", r"C:\Screener\tmp\screener_data.csv")
        tv = TvDatafeed(username="password",password="password")
        screener_data = pd.read_csv(r"C:\Screener\tmp\screener_data.csv")
        time.sleep(0.1)

        numTickers = len(screener_data)
        #Changing ARCA into AMEX
        for i in range(numTickers):
            if str(screener_data.iloc[i]['Exchange']) == "NYSE ARCA":
                screener_data.at[i, 'Exchange'] = "AMEX"
            if screener_data.iloc[i]['Pre-market Change'] is None:
                    screener_data.at[i, 'Pre-market Change'] = 0
    
    def runIntradayScan(brows):
        browser = brows

        if(browser == None):
            browser = Screen.startFirefoxSession()
        try:
            if(str(browser.current_url) != "https://www.tradingview.com/screener/"):
                browser.close()
                browser = Screen.startFirefoxSession()
        except selenium.common.exceptions.WebDriverException:
            browser = Screen.startFirefoxSession()

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
        time.sleep(0.1)
        
        return browser

    def logInScrapper():
        tv = TvDatafeed(username="cs.benliu@gmail.com",password="tltShort!1")
        data_apple = tv.get_hist('AAPL', 'NASDAQ', n_bars=2)
        return tv
    def startFirefoxSession():
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
        time.sleep(1.5)
        browser.find_element(By.XPATH, '//div[@data-set="performance"]').click()
        time.sleep(.5)
        element_tab = browser.find_element(By.XPATH, '//div[@data-set="overview"]').click()

        #Logging into trading view
        login_page = browser.find_element(By.XPATH, '//button[@aria-label="Open user menu"]')
        login_page.click()
        time.sleep(1)
        login_page = browser.find_element(By.XPATH, '//button[@data-name="header-user-menu-sign-in"]')
        login_page.click()
        time.sleep(1)
        login_page = browser.find_element(By.XPATH, '//span[@class="tv-signin-dialog__social tv-signin-dialog__toggle-email js-show-email"]')
        login_page.click()
        username = browser.find_element(By.XPATH, '//input[@name="username"]')
        username.send_keys("cs.benliu@gmail.com")
        time.sleep(0.5)
        password = browser.find_element(By.XPATH, '//input[@name="password"]')
        password.send_keys("tltShort!1")
        time.sleep(0.5)
        login_button = browser.find_element(By.XPATH, '//button[@class="tv-button tv-button--size_large tv-button--primary tv-button--loader"]')
        login_button.click()
        time.sleep(7)
        Screen.clickFilters(browser)
        return browser
    def clickFilters(browser):
        #setting default scanner settings
        browser.find_element(By.XPATH, '//div[@data-name="screener-field-sets"]').click()
        time.sleep(0.1)
        browser.find_element(By.XPATH, '//div[@data-set="overview"]').click()

        #seting filters
        filter_tab = browser.find_element(By.XPATH, '//div[@class="tv-screener-sticky-header-wrapper__fields-button-wrap"]')
        try:
            filter_tab.click()
        except ElementNotInteractableException:
            print('test')
        time.sleep(0.5)
        #Setting up the TV screener parameters
        tab1 = browser.find_element(By.XPATH, '//label[@data-field="earnings_per_share_basic_ttm"]')
        tab2 = browser.find_element(By.XPATH, '//label[@data-field="number_of_employees"]')
        tab3 = browser.find_element(By.XPATH, '//label[@data-field="sector"]')
        tab4 = browser.find_element(By.XPATH, '//label[@data-field="Recommend.All"]')
        tab6 = browser.find_element(By.XPATH, '//label[@data-field="price_earnings_ttm"]')
        tab7 = browser.find_element(By.XPATH, '//label[@data-field="relative_volume_intraday.5"]')
        tab8 = browser.find_element(By.XPATH, '//label[@data-field="change.1"]')
        tab9 = browser.find_element(By.XPATH, '//label[@data-field="change.5"]')
        tab10 = browser.find_element(By.XPATH, '//label[@data-field="change_from_open"]')
        tab11 = browser.find_element(By.XPATH, '//label[@data-field="exchange"]')
        tab12 = browser.find_element(By.XPATH, '//label[@data-field="premarket_change_abs"]')
        tab13 = browser.find_element(By.XPATH, '//label[@data-field="open"]')
        tab14 = browser.find_element(By.XPATH, '//label[@data-field="change_from_open_abs"]')
        tab15 = browser.find_element(By.XPATH, '//label[@data-field="change_from_open"]')
        tab1.click()
        tab2.click()
        tab3.click()
        tab4.click()
        tab6.click()
        tab7.click()
        tab8.click()
        tab9.click()
        tab10.click()
        tab11.click()
        tab12.click()
        tab13.click()
        tab14.click()
        tab15.click()

        time.sleep(0.5) 
        browser.find_element(By.XPATH, '//div[@data-name="screener-filter-sets"]').click()
        time.sleep(0.25)
        browser.find_element(By.XPATH, '//span[@class="js-filter-set-name"]').click()
        time.sleep(0.25)
        sortRVol = browser.find_element(By.XPATH, '//div[@data-field="relative_volume_intraday.5"]')
        sortRVol.click()
