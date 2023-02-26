
from argparse import ONE_OR_MORE
from multiprocessing.pool import CLOSE
import typing_extensions
from discordwebhook import Discord
import pathlib
import mplfinance as mpf
import statistics
import pandas as pd
import datetime
import matplotlib as mpl
from Datav4 import Data
from tvDatafeed import TvDatafeed
from datetime import datetime
discordtopGainers = Discord(url="https://discord.com/api/webhooks/1071666210514669648/dSLYGAB5CWQuulV46ePmExwgljauPexCG10R2ZqZctTl7lyya-Zs7lJ7ecLjQEruAfYw")
discordintraday = Discord(url="https://discord.com/api/webhooks/1071667193709858847/qwHcqShmotkEPkml8BSMTTnSp38xL1-bw9ESFRhBe5jPB9o5wcE9oikfAbt-EKEt7d3c")
discord = Discord(url="https://discord.com/api/webhooks/1071506429229416519/41ps0qlsiiFRDLxnZVCF5KuDtb_SWBHCwB5scK-YUf96mrBpzZRydsT2C4GiGPDAEmKW")

class log:
    def sendDiscordEmbedGainers(ticker, description):
        discordtopGainers.post(
            embeds=[
            {

                "title": ticker,
                "description": description,
            }
            ],
        )
    def sendDiscordEmbedIntraday(ticker, description):
        discordintraday.post(
            embeds=[
            {

                "title": ticker,
                "description": description,
            }
            ],
        )
        

    def sendDiscordEmbed(ticker, description):
        discord.post(
            embeds=[
            {

                "title": ticker,
                "description": description,
            }
            ],
        )
    def sendDiscordPost(f):
        discord.post(file={"test": open(f, "rb")})
    def sendDiscordIntradayPost(f):
        discordintraday.post(file={"test": open(f, "rb")})
    def sendDiscordGainersPost(f):
        discordtopGainers.post(file={"test": open(f, "rb")})



    def intraday(df, screenbar, z, type):
        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        ourpath = pathlib.Path("C:/Screener/tmp") / "test.png"

       

        z = round(z, 3)
        setup_df = df
            
        change = round(screenbar["Change 1m, %"], 2)
        dayChange = round(screenbar['Change %'], 2)
        #changeFromOpen = round(screenbar['Change from Open'], 2)
        #openValue = screenbar['Open']
        currPrice = screenbar['Price']
        volume = screenbar['Volume']
        tick = screenbar['Ticker']
        pmChange = screenbar['Pre-market Change']
        currPrice = screenbar['Price']
        volume = screenbar['Volume']
        dolVol = screenbar['Volume*Price']
        marketCap = round(screenbar['Market Capitalization'], 1)
        marketCapText = round((marketCap / 1000000000), 2)
        relativeVolAtTime = round(screenbar['Relative Volume at Time'], 1)
        gapValuePercent = 0
        prevClose = 0
        pmPrice = 0
        prevClose = currPrice
        pmPrice = round((prevClose + pmChange), 2)
        gapValuePercent = round(((pmPrice/prevClose) - 1)*100, 2)
        lengthDf = len(setup_df)
        setup_df = setup_df[lengthDf - 80:]
        if(type == "Pop"):
            openCandlePrice = float(setup_df.iloc[len(setup_df)-1][1])
            changePrice = round(float(currPrice - openCandlePrice), 2)
            mpf.plot(setup_df, type='candle', mav=(10, 20), volume=True, title=tick, style=s, savefig=ourpath)
            log.sendDiscordEmbedIntraday(tick + f" Open of 1m:{openCandlePrice} >> Current: {currPrice} ▲ {changePrice} ({change}%)", f"Intraday % Gaining Setup, Volume: {volume}, RelVol: {relativeVolAtTime}x, MCap: ${marketCapText}B")
            log.sendDiscordIntradayPost('tmp/test.png')

        if(type == "Gainer"):
            openCandlePrice = float(setup_df.iloc[len(setup_df)-1][1])
            changePrice = round(float(currPrice - openCandlePrice), 2)
            mpf.plot(setup_df, type='candle', mav=(10, 20), volume=True, title=tick, style=s, savefig=ourpath)
            log.sendDiscordEmbedGainers(tick + f" PC:{prevClose} >> {currPrice} ▲ {currPrice} ({dayChange}%)", f"Top Gainer, Volume: {volume}, RelVol: {relativeVolAtTime}x, MCap: ${marketCapText}B")
            log.sendDiscordGainersPost('tmp/test.png')

       


    def daily(screenbar, z, setup_type, dateToSearch,pmPrice, data_daily,currentday):
    
        
        if dateToSearch == "0":

            tick = str(screenbar['Ticker'])
            dateString = dateToSearch
            data ={'Date': [dateString],
                    'Ticker':[ tick],
                    'Setup': [str(setup_type)],
                    'Z': [z],
                    'pm':[pmPrice]}
        
            dfadd = pd.DataFrame(data)
            dfadd.to_csv((r"C:/Screener/tmp/todays_setups.csv"), mode='a', index=False, header=False)
        else:
            
            #gap percent
            #adr
            #vol %
            #q risin 10 > rising 20
            # 1 dperf
            # 2 d perf
            #3 d perf
            #10 ma perf
            #10 am perf time
           
            
           


            tick = str(screenbar['Ticker'])
            dateString = dateToSearch


           
            gap = round( (data_daily.iloc[currentday-1][4]/data_daily.iloc[currentday-1][1] - 1)*100,2)

            volma = []
            for i in range(10):
                volma.append(data_daily.iloc[currentday-1-i][5])
            vol = round((data_daily.iloc[currentday][5]/statistics.mean(volma) ),2)

            q_data = pd.read_csv("C:/Screener/data_csvs/QQQ_data.csv")
            qcurrentday = Data.findIndex(q_data, dateToSearch,False)
            q10 = []
            q20 = []

            for i in range(21):
                close = q_data.iloc[qcurrentday - 1-i][4]

                q20.append(close)
                if i >= 9:
                    q10.append(close)

                if i == 19:
                    prev10 = statistics.mean(q10)
                    prev20 = statistics.mean(q20)

            current10 = statistics.mean(q10)
            current20 = statistics.mean(q20)
            
            if current10 > prev10 and current20 > prev20 and current10 > current20:
                q = True
            else:
                q = False
            
            one = round((data_daily.iloc[currentday][4] / data_daily.iloc[currentday][1] - 1) * 100,2)
            two =   round((data_daily.iloc[currentday+1][4] / data_daily.iloc[currentday][1] - 1) * 100,2)
            three =  round((data_daily.iloc[currentday+2][4] / data_daily.iloc[currentday][1] - 1) * 100,2)

            
          
                            
            adr = []
            for j in range(20): 
                high = data_daily.iloc[currentday-j-1][2]
                low = data_daily.iloc[currentday-j-1][3]
                val = (high/low - 1) * 100
                adr.append(val)
                        
            adr = round(statistics.mean(adr) ,2)
           
            i = 0
            while True:

                ma10 = []
                for j in range(10):
                    ma10.append((data_daily.iloc[currentday-j+i][4]))
                ma10 = statistics.mean(ma10)
                if (data_daily.iloc[currentday+i][4]) < ma10:
                    break

                if i > 150:
                    break

                i += 1
            ten = round( (data_daily.iloc[currentday+i][4] / data_daily.iloc[currentday][4] - 1)*100,2)
            time = i 

          
        

            data ={'Date': [dateString],
                    'Ticker':[tick],
                    'Setup': [str(setup_type)],
                    'Z': [z],
                    'gap': [gap],
                    'adr': [adr],
                    'vol': [vol],
                    'q': [q],
                    '1': [one],
                    '2': [two],
                    '3': [three],
                    '10': [ten],
                    'annotation': [""],
                    'rating': [""],
                    'time': [time]
  
                    }
        
            dfadd = pd.DataFrame(data)


            
            
            dfadd.to_csv((r"C:/Screener/tmp/setups.csv"), mode='a', index=False, header=False)
            
            







