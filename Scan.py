
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






class Scan:
    def convert_date(dt):
        if type(dt) == str:
            try:
                dt = datetime.datetime.strptime(dt, '%Y-%m-%d')
            except:
                dt = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        if type(dt) == datetime.date:
            time = datetime.time(9,30,0)
            dt = datetime.datetime.combine(dt,time)
        if dt.time() == datetime.time(0):
            time = datetime.time(9,30,0)
            dt = datetime.datetime.combine(dt.date(),time)
        return(dt)

    def isToday(dt):
        if dt == None:
            return False
        if dt == 'Today' or dt == '0' or dt == 0:
            return True
        time = datetime.time(0,0,0)
        today = datetime.date.today()
        today = datetime.datetime.combine(today,time)
        dt = Scan.convert_date(dt)
        if dt >= today:
            return True
        return False




    def get(date = None, tf = None, refresh = False, browser = None):
        



        if Scan.isToday(date):

            if tf == 'd' or tf == 'w' or tf == 'm':
                
                if refresh:
                    
                    Scan.runDailyScan(None)
                
                return pd.read_feather(r"C:\Screener\tmp\screener_data.feather").set_index('Ticker')

            else:
                if not  refresh:
                    return pd.read_feather(r"C:\Screener\tmp\screener_data_intraday.feather").set_index('Ticker')
                while True:
                    try:
                    
                        browser = Scan.runIntradayScan(browser)
                        return pd.read_feather(r"C:\Screener\tmp\screener_data_intraday.feather").set_index('Ticker')
                        
                    except:
                        
                        Scan.tryCloseLogout(browser)

        else:
            
            Scan.updateList(refresh)
            return pd.read_feather(r"C:\Screener\tmp\full_ticker_list.feather").set_index('Ticker')#.dropna()

    
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

        screener_data.to_feather(r"C:\Screener\tmp\screener_data.feather")
    
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


        percent = .045

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
        df.to_feather(r"C:\Screener\tmp\screener_data_intraday.feather")
        time.sleep(0.1)

        return browser

    def logInScrapper():
        tv = TvDatafeed(username="cs.benliu@gmail.com",password="tltShort!1")
        return tv
    def startFirefoxSession():
        options = Options()
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
        #options.headless = True
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
        FireFoxDriverPath = os.path.join(os.getcwd(), 'Drivers', 'geckodriver.exe')
        FireFoxProfile = webdriver.FirefoxProfile()
        FireFoxProfile.set_preference("General.useragent.override", user_agent)
        browser = webdriver.Firefox(options=options, executable_path=FireFoxDriverPath)
        browser.implicitly_wait(7)
        #browser.maximize_window()
        browser.set_window_size(2560, 1440)
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
        except:
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

        '''
        //*[@id="close"]
        //*[@id="picker-header"]
        '''

        #//*[@id="close"]
        browser.find_element(By.XPATH, '//div[@id="close"]').click()
        
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



    def updateList(refresh = False):
        df1 = pd.read_feather("C:/Screener/tmp/screener_data.feather")
        df1 = df1.set_index('Ticker')
        df2 = pd.read_feather("C:/Screener/tmp/full_ticker_list.feather")
        
        df2 = df2.set_index('Ticker')

       

        #df3 = df.merge(df2, left_index = True , right_index = True, how = 'left')
        df3 = pd.concat([df1,df2]).drop_duplicates()
        #print(f"{len(df3)} ppjj")
        #print(f'added {len(df3) - len(df2)} to full ticker list')
        
        if refresh:
            removelist = []
            
            for i in range(len(df3)):
                ticker = str(df3.index[i])
                current = df1.index.to_list()
                if ticker not in current or ticker == None or ticker == 'None':
                    if not os.path.exists("C:/Screener/minute/" + ticker + ".feather"):
                        removelist.append(ticker)
                        

           
            #print(f"{len(removelist)} removed")
            for ticker in removelist:
                try:
                    df3.drop(df3.loc[ticker])
                   # print(f'removed {ticker}')
                except:
                    pass

           
        df3 = df3.reset_index()
        
        df3.to_feather("C:/Screener/tmp/full_ticker_list.feather")

if __name__ == '__main__':
    Scan.updateList(True)
    print(pd.read_feather("C:/Screener/tmp/full_ticker_list.feather")['Ticker'].to_list())
    


