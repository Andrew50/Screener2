from discordwebhook import Discord
import pathlib
import mplfinance as mpf
import pandas as pd
import datetime
import matplotlib as mpl
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

       


    def daily(screenbar, z, setup_type, dateToSearch,pmPrice):
    
        tick = str(screenbar['Ticker'])
        dateString = dateToSearch
        data ={'Date': [dateString],
                'Ticker':[ tick],
                'Setup': [str(setup_type)],
                'Z': [z],
                'pm':[pmPrice]}
        
        dfadd = pd.DataFrame(data)
        if dateToSearch == "0":
            dfadd.to_csv((r"C:/Screener/tmp/todays_setups.csv"), mode='a', index=False, header=False)
        else:
            dfadd.to_csv((r"C:/Screener/tmp/setups.csv"), mode='a', index=False, header=False)
   







