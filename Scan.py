
import os 
import time 
import selenium
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By 
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException, NoSuchElementException
import pandas as pd
import datetime
from tvDatafeed import TvDatafeed

from Data6 import Data as data




class Scan:

    def get(date, tf, browser = None):
        
        if data.isToday(date):

            if tf == 'd' or tf == 'w' or tf == 'm':
                Scan.runDailyScan(None)
                return pd.read_csv(r"C:\Screener\tmp\screener_data.csv")

            else:
                while True:
                    try:
                    
                        browser = Scan.runIntradayScan(browser)
                        return pd.read_csv(r"C:\Screener\tmp\screener_data_intraday.csv")
                        
                    except:
                        
                        Scan.tryCloseLogout(browser)

        else:
            Scan.updateList()
            return pd.read_csv(r"C:\Screener\tmp\full_ticker_list.csv")

    
    def runDailyScan(brows):
        browser = brows
        if(browser == None):
            browser = Scan.startFirefoxSession()

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

        screener_data.to_csv(r"C:\Screener\tmp\screener_data.csv")
    
    def runIntradayScan(brows):
        browser = brows

        if(browser == None):
            browser = Scan.startFirefoxSession()
        try:
            if(str(browser.current_url) != "https://www.tradingview.com/screener/"):
                browser.close()
                browser = Scan.startFirefoxSession()
        except selenium.common.exceptions.WebDriverException:
            browser = Scan.startFirefoxSession()

        #creating the csv file
        browser.find_element(By.XPATH, '//div[@data-name="screener-refresh"]').click()
        browser.find_element(By.XPATH, '//div[@data-name="screener-refresh"]').click()
        download_screener_data = browser.find_element(By.XPATH, '//div[@data-name="screener-export-data"]')
        download_screener_data.click()
        time.sleep(2)
        today = str(datetime.date.today())
        downloaded_file = r"C:\Downloads\america_" + today + ".csv"
        #new_name = r"C:\Downloads\screener_data_intraday.csv"



        #os.rename(downloaded_file, new_name)
        #os.replace(r"C:\Downloads\screener_data_intraday.csv", r"C:\Screener\tmp\screener_data_intraday.csv")

        #pull df
        df = pd.read_csv(downloaded_file)
        os.remove(downloaded_file)


        percent = .03

        length = len(df) - 1
        left = 0
        right =  int(length* (percent))
        df = df[left:right]
        numTickers = len(df)
        for i in range(numTickers):
            if str(df.iloc[i]['Exchange']) == "NYSE ARCA":
                df.at[i, 'Exchange'] = "AMEX"
            if df.iloc[i]['Pre-market Change'] is None:
                    df.at[i, 'Pre-market Change'] = 0
        df.to_csv(r"C:\Screener\tmp\screener_data_intraday.csv")
        time.sleep(0.1)

        return browser

    def logInScrapper():
        tv = TvDatafeed(username="cs.benliu@gmail.com",password="tltShort!1")
        return tv
    def startFirefoxSession():
        options = Options()
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        options.headless = True
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
        FireFoxDriverPath = os.path.join(os.getcwd(), 'Drivers', 'geckodriver.exe')
        FireFoxProfile = webdriver.FirefoxProfile()
        FireFoxProfile.set_preference("General.useragent.override", user_agent)
        browser = webdriver.Firefox(options=options, executable_path=FireFoxDriverPath)
        browser.implicitly_wait(7)
        #browser.maximize_window()
        browser.set_window_size(1920, 1080)
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
        Scan.clickFilters(browser)
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
            pass
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
    def tryCloseLogout(browser):
        if browser != None:
            try:
                
                browser.find_element(By.XPATH, '//button[@class="close-button-aR0iEGbS closeButton-GLTtix84 defaultClose-GLTtix84"]').click()
            except AttributeError:
                pass
            except selenium.common.exceptions.NoSuchElementException:
                pass



    def updateList():
        df = pd.read_csv("C:/Screener/tmp/screener_data.csv")
        df = df.set_index('Ticker')
        df2 = pd.read_csv("C:/Screener/tmp/full_ticker_list.csv")
        df2 = df2.set_index('Ticker')
        df3 = df.merge(df2, left_index = True , right_index = True, how = 'outer')
        #df3 = df3.reset_index()  
        df3.to_csv("C:/Screener/tmp/trest.csv")

        


