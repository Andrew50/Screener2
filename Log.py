

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

from Traits import Traits as traits
from Account import Account as account



class Log:

    def log(self):
       
        if self.event == '-table-':
            try:
                index = self.values['-table-'][0]
                
                if type(index) == int:
                    self.index = index
                    bar = self.df_log.iloc[index]
                    self.window["input-ticker"].update(bar[0])
                    self.window["input-datetime"].update(bar[1])
                    self.window["input-shares"].update(bar[2])
                    self.window["input-price"].update(bar[3])
                    self.window["input-setup"].update(bar[4])
                    
            except:
                pass

            
        
        if self.event == "Enter":
            
            ticker = str(self.values['input-ticker'])

            if ticker != "":
                dt = self.values['input-datetime']
                dt  = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
                shares = float(self.values['input-shares'])
                price = float(self.values['input-price'])
                setup = str(self.values['input-setup'])

                add = pd.DataFrame({
            
                    'Ticker': [ticker],
                    'Datetime':[dt],
                    'Shares': [shares],
                    'Price': [price],
                    'Setup': [setup]
                    })
                if self.index == None:
                    self.df_log = pd.concat([self.df_log,add])
                    self.df_log.reset_index(inplace = True, drop = True)
                else:
                    self.df_log.iat[self.index,0] = ticker
                    self.df_log.iat[self.index,1] = dt
                    self.df_log.iat[self.index,2] = shares
                    self.df_log.iat[self.index,3] = price
                    self.df_log.iat[self.index,4] = setup
                self.df_log = self.df_log.sort_values(by='Datetime', ascending = True)
                account.update(self,dt)
                traits.update(self,add.values.tolist()[0])
                
                self.df_log.to_feather(r"C:\Screener\tmp\log.feather")
                
        if self.event == "Delete":
            if self.index != None:
                bar = self.df_log.iloc[self.index].to_list()
                self.df_log = self.df_log.drop(self.index).reset_index(drop = True)
                self.df_log = self.df_log.sort_values(by='Datetime', ascending = True)
                account.update(self,bar[1])
                traits.update(self,bar)
                

           
        elif self.event == "Clear":
            self.index = None
            self.window["input-ticker"].update("")
            self.window["input-shares"].update("")
            self.window["input-price"].update("")
            self.window["input-setup"].update("")
            self.window["input-datetime"].update("")

        self.df_log = self.df_log.sort_values(by='Datetime', ascending = True)
        self.df_log = self.df_log.reset_index(drop = True)
        self.df_log.to_feather(r"C:\Screener\tmp\pnl\log.feather")
        table = self.df_log.values.tolist()

       
        self.window["-table-"].update(table)