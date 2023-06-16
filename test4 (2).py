from datetime import datetime, timedelta
import pandas as pd
import warnings
from time import sleep
from lightweight_charts import Chart
from tvDatafeed import TvDatafeed, Interval
from Data7 import Data as data

class Simulate:

    def run(setuptype):
        df = pd.read_feather(r"C:/Screener/sync/allsetups.feather")

        new_df = df.drop(axis=1, labels=["Z", "timeframe", "annotation"])
        for i in range(len(df)):
            new_df.at[i, 'ticker'] = df.iloc[i]['Ticker']
            new_df.at[i, 'date'] = df.iloc[i]['Date']
            if(df.iloc[i]['Setup'] == setuptype):
                new_df.at[i, 'setup'] = 1
            else:
                new_df.at[i, 'setup'] = 0
        new_df = new_df.drop(axis=1, labels=['Ticker', 'Date', 'Setup'])

        new_df.to_feather(f'C:/Screener/setups/database/{setuptype}.feather')

        print(new_df)

    def read(name, t):

        if(t == "csv"):
            df = pd.read_csv(r"D:/Users/csben/Desktop/read/" + name + ".csv")
        else:
            df = pd.read_feather(f"D:/Users/csben/Desktop/read/{name}.feather")
        print(df.to_string())

    def formatTicks(name):
        df = df = pd.read_csv(r"D:/Users/csben/Desktop/read/" + name + ".csv")
        df = df.drop(axis=1, labels=['Last Exchange', 'Bid Exchange', 'Ask Exchange', 'Trade Condition']).reset_index(drop = True)
        df['price'] = df['Last Price']
        df['time'] = pd.to_datetime(df['Time'])
        df['volume'] = df['Last Size']
        df.to_csv(r"D:/Users/csben/Desktop/read/" + name + "_ticks.csv", index=False)
    
    def get_previous_data(ticker, referencetime, stagger=150):
        df = data.get(ticker, tf='minute')
        timeIndex = data.findex(df, referencetime)
        df = df[timeIndex-stagger:timeIndex]
        df = df.reset_index(drop = False)
        df['time'] = df['datetime']
        df = df.drop(axis=1, labels='datetime').reset_index(drop = True)
        return df 

    def lightweight(name, speed=1):
        warnings.simplefilter(action='ignore', category=FutureWarning)
        ticker = name.split("_")[0]
        '''
        tv = TvDatafeed()
        test = tv.get_hist("NVCR", "NASDAQ", Interval.in_1_minute, 600)
        new = test[:210].drop(axis=1, labels=['symbol', 'volume']).reset_index(drop = True)
        new['time'] = new['datetime']
        new = new.drop(axis=1, labels='datetime')'''
        df2 = pd.read_csv(r"D:/Users/csben/Desktop/read/" + name + "_ticks.csv")
        print(df2)
        before_data = Simulate.get_previous_data(ticker, df2.iloc[0]['time'])
        ticks = df2[['time', 'price', 'volume']]
        chart = Chart(volume_enabled=False)
        chart.set(before_data)
        chart.show()
        for i, tick in ticks.iterrows():
            chart.update_from_tick(tick)
            print(f"NVCR  {df2.iloc[i]['Bid Price']}->{df2.iloc[i]['Bid Size']} -- {df2.iloc[i]['Ask Price']}->{df2.iloc[i]['Ask Size']} | Last: {df2.iloc[i]['Last Price']} x {int(df2.iloc[i]['Last Size']/100)} {df2.iloc[i]['time']}|||||", end='\r')
            if((i != len(ticks)-1) and (df2.iloc[i]['time'] == df2.iloc[i+1]['time'])):
                pass
            elif (i != len(ticks)-1): 
                delay = p


            sleep(delay/speed)


if __name__ == '__main__':

    aiTest.test()
    #Simulate.run('P')
    #Simulate.read('test', "csv")
    #Simulate.formatTicks('NVCR_test')
    #Simulate.lightweight('NVCR_test')
