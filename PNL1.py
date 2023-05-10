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



#from accountcalculator import accountcalculator as account
from Account import Account as account


from Log import Log as log

from Traits import Traits as traits
from Plot import Plot as plot


class PNL():

   

    def update(self):
        
        if self.menu == None:
            sg.theme('DarkGrey')
            try:
                self.df_log = pd.read_feather(r"C:\Screener\tmp\pnl\log.feather")
            except:
                self.df_log = pd.DataFrame()
            try:
                self.df_traits = pd.read_feather(r"C:\Screener\tmp\pnl\traits.feather").sort_values(by='Datetime',ascending = False)
            except:
                self.df_traits = pd.DataFrame()
            try:
                self.df_pnl = pd.read_feather(r"C:\Screener\tmp\pnl\pnl.feather").set_index('datetime', drop = True)
            except:
                self.df_pnl = pd.DataFrame()
          
            self.menu = "Log"
        else:
            self.window.close()
        print(self.menu)
        if self.menu == "Log":



            toprow = ['Ticker        ','Datetime         ','Shares    ', 'Price      ','Setup    ']
            c1 = [  
            [(sg.Text("Ticker    ")),sg.InputText(key = 'input-ticker')],
            [(sg.Text("Datetime")),sg.InputText(key = 'input-datetime')],
            [(sg.Text("Shares   ")),sg.InputText(key = 'input-shares')],
            [(sg.Text("Price     ")),sg.InputText(key = 'input-price')],
            [(sg.Text("Setup    ")),sg.InputText(key = 'input-setup')],
            [sg.Button('Delete'),sg.Button('Clear'),sg.Button('Enter')],
            [sg.Button('Account'), sg.Button('Log'),sg.Button('Traits'),sg.Button('Plot')]]
    
            c2 = [[sg.Table([],headings=toprow,key = '-table-',auto_size_columns=True,justification='left',enable_events=True,selected_row_colors='red on yellow')]]
         

            layout = [
            [sg.Column(c1),
             sg.VSeperator(),
             sg.Column(c2),]]
            self.window = sg.Window(self.menu, layout,margins = (10,10),finalize = True)
            log.log(self)
        if self.menu == "Account":
            layout =[
            [sg.Image(key = '-CHART-')],
            [(sg.Text("Timeframe")),sg.InputText(key = 'input-timeframe')],
            [(sg.Text("Datetime  ")),sg.InputText(key = 'input-datetime')],
            [sg.Button('Recalc'),sg.Button('Load')],
            [sg.Button('Account'), sg.Button('Log'),sg.Button('Traits'),sg.Button('Plot')]]
            self.window = sg.Window(self.menu, layout,margins = (10,10),finalize = True)
            account.account(self)
        if self.menu == "Traits":
            layout = [
            [sg.Image(key = '-CHART-')],
            [(sg.Text("Trait  ")),sg.InputText(key = 'input-trait')],
            [sg.Button('Recalc'),sg.Button('Enter')],
            [sg.Button('Account'), sg.Button('Log'),sg.Button('Traits'),sg.Button('Plot')]]
            self.window = sg.Window(self.menu, layout,margins = (10,10),finalize = True)
            traits.traits(self)
        if self.menu == "Plot":
            toprow = ['Date             ','Shares   ','Price    ', 'Percent      ',' Timedelta    ','% size    ']
            layout = [  
             [sg.Image(key = '-IMAGE2-')],
             [sg.Image(key = '-IMAGE1-')],
             [(sg.Text((str(f"{self.i + 1} of {len(self.df_traits)}")), key = '-number-')), sg.Table([],headings=toprow,key = '-table-',auto_size_columns=True,justification='left', expand_y = False)],
            [(sg.Text("Ticker  ")),sg.InputText(key = 'input-ticker')],
            [(sg.Text("Date   ")),sg.InputText(key = 'input-datetime')],
            [(sg.Text("Setup  ")),sg.InputText(key = 'input-setup')],
            [(sg.Text("Sort    ")),sg.InputText(key = 'input-sort')],
            [[sg.Button('Prev'),sg.Button('Next'),sg.Button('Load')]],
            [sg.Button('Account'), sg.Button('Log'),sg.Button('Traits'),sg.Button('Plot')]]
            self.window = sg.Window(self.menu, layout,margins = (10,10),finalize = True)
            plot.plot(self)





    def loop(self):

        with Pool(6) as self.pool:
            if os.path.exists("C:/Screener/tmp/pnl/charts"):
                shutil.rmtree("C:/Screener/tmp/pnl/charts")
            os.mkdir("C:/Screener/tmp/pnl/charts")
            self.preloadamount = 7
            self.i = 0
            self.menu = None
            self.event = [None]
            self.index = None
            self.update(self)
            while True:
                self.event, self.values = self.window.read()
                if self.event == "Traits" or self.event == "Plot" or self.event == "Account" or self.event == "Log":
                    self.menu = self.event
                    self.update(self)
                elif self.event != "":
                    
                    #print(self.menu)
                    if self.menu == "Traits":

                        traits.traits(self)
                    elif self.menu == "Plot":
                        plot.plot(self)
                    elif self.menu == "Account":
                        account.account(self)
                    elif self.menu == "Log":
                        log.log(self)
if __name__ == "__main__":
    PNL.loop(PNL)




