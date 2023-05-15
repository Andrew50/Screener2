

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
        

        self.df_log = self.df_log.sort_values(by='datetime', ascending = False)
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
                try:
                    dt = self.values['input-datetime']
                    dt  = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
                    shares = float(self.values['input-shares'])
                    price = float(self.values['input-price'])
                    setup = str(self.values['input-setup'])

                    add = pd.DataFrame({
            
                        'ticker': [ticker],
                        'datetime':[dt],
                        'shares': [shares],
                        'price': [price],
                        'setup': [setup]
                        })
                    df_log = self.df_log
                    if self.index == None:
                        df_log = pd.concat([df_log,add])
                        df_log.reset_index(inplace = True, drop = True)
                    else:
                    
                        df_log.iat[self.index,0] = ticker
                        old_date = df_log.iat[self.index,1]
                        df_log.iat[self.index,1] = dt
                        df_log.iat[self.index,2] = shares
                        df_log.iat[self.index,3] = price
                        df_log.iat[self.index,4] = setup
                        if old_date < dt:
                            dt = old_date
                    df_log = df_log.sort_values(by='datetime', ascending = True).reset_index(drop = True)
                    self.df_pnl = account.calcaccount(self.df_pnl,df_log,dt)
                    self.df_pnl.reset_index().to_feather(r"C:\Screener\sync\pnl.feather")
                    self.df_traits = traits.update(add.values.tolist()[0], self.df_log,self.df_traits,self.df_pnl)

                    self.df_log = df_log
                    if os.path.exists("C:/Screener/tmp/pnl/charts"):
                        shutil.rmtree("C:/Screener/tmp/pnl/charts")
                    os.mkdir("C:/Screener/tmp/pnl/charts")
                    #self.df_log.
                    #self.df_log.to_feather(r"C:\Screener\sync\log.feather")
                except Exception as e:
                    sg.Popup(str(e))
                
        if self.event == "Delete":
            if self.index != None:
                bar = self.df_log.iloc[self.index].to_list()
                df_log = self.df_log.drop(self.index).reset_index(drop = True)
                df_log = df_log.sort_values(by='datetime', ascending = True)
                self.df_pnl = account.calcaccount(self.df_pnl,df_log,bar[1])
                self.df_pnl.reset_index().to_feather(r"C:\Screener\sync\pnl.feather")
                self.df_traits = traits.update(bar, self.df_log,self.df_traits,self.df_pnl)
                self.df_log = df_log
                self.index = None
                if os.path.exists("C:/Screener/tmp/pnl/charts"):
                    shutil.rmtree("C:/Screener/tmp/pnl/charts")
                os.mkdir("C:/Screener/tmp/pnl/charts")
                

           
        elif self.event == "Clear":
            if self.index == None:
            
                self.window["input-ticker"].update("")
                self.window["input-shares"].update("")
                self.window["input-price"].update("")
                self.window["input-setup"].update("")
                self.window["input-datetime"].update("")
            else:
                self.index = None

        try:
            self.window['-index-'].update(f'Index {self.index}')
        except:
            pass
        
        self.df_log = self.df_log.reset_index(drop = True)  
        self.df_log.to_feather(r"C:\Screener\sync\log.feather")
        table = self.df_log.sort_values(by='datetime', ascending = False).values.tolist()

       
        self.window["-table-"].update(table)