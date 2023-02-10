﻿from discordwebhook import Discord
import pathlib
import mplfinance as mpf
import datetime
import matplotlib as mpl
from tvDatafeed import TvDatafeed
discordtopGainers = Discord(url="https://discord.com/api/webhooks/1071666210514669648/dSLYGAB5CWQuulV46ePmExwgljauPexCG10R2ZqZctTl7lyya-Zs7lJ7ecLjQEruAfYw")
discordintraday = Discord(url="https://discord.com/api/webhooks/1071667193709858847/qwHcqShmotkEPkml8BSMTTnSp38xL1-bw9ESFRhBe5jPB9o5wcE9oikfAbt-EKEt7d3c")
discord = Discord(url="https://discord.com/api/webhooks/1071506429229416519/41ps0qlsiiFRDLxnZVCF5KuDtb_SWBHCwB5scK-YUf96mrBpzZRydsT2C4GiGPDAEmKW")


class discordManager:
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




    def post(df, screenbar, z, type, currentDay):
        dateString = currentDay
        z = round(z, 3)
        setup_df = df
        tick = str(screenbar['Ticker'])
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
        if(currentDay == "0"):
            gapValuePercent = dayChange
            lengthDf = len(setup_df)
            prevClose = currPrice
            setup_df = setup_df[lengthDf - 80:]
        else:
            if(currentDay == len(setup_df)):
                dateString = str(datetime.datetime.now().date())
            else:
                dateString = str(setup_df.index[currentDay]).split(" ")[0]

            if(dateString == str(datetime.datetime.now().date())):
                prevClose = currPrice
                pmPrice = round((prevClose + pmChange), 2)
                gapValuePercent = round(((pmPrice/prevClose) - 1)*100, 2)
            else:
                prevClose = round(setup_df.iloc[currentDay - 1][4], 2)
                setupDayOpen = round(setup_df.iloc[currentDay][1], 2)
                gapValuePercent = round(((setupDayOpen/prevClose) - 1)*100, 2)
                pmChange = setupDayOpen - prevClose

        #else()
        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        ourpath = pathlib.Path("C:/Screener/tmp") / "test.png"
        if(type == "Pop"):
            openCandlePrice = float(setup_df.iloc[len(setup_df)-1][1])
            changePrice = round(float(currPrice - openCandlePrice), 2)
            mpf.plot(setup_df, type='candle', mav=(10, 20), volume=True, title=tick, style=s, savefig=ourpath)
            discordManager.sendDiscordEmbedIntraday(tick + f" Open of 1m:{openCandlePrice} >> Current: {currPrice} ▲ {changePrice} ({change}%)", f"Intraday % Gaining Setup, Volume: {volume}, RelVol: {relativeVolAtTime}x, MCap: ${marketCapText}B")
            discordManager.sendDiscordIntradayPost('tmp/test.png')

        if(type == "Gainer"):
            openCandlePrice = float(setup_df.iloc[len(setup_df)-1][1])
            changePrice = round(float(currPrice - openCandlePrice), 2)
            mpf.plot(setup_df, type='candle', mav=(10, 20), volume=True, title=tick, style=s, savefig=ourpath)
            discordManager.sendDiscordEmbedGainers(tick + f" PC:{prevClose} >> {currPrice} ▲ {currPrice} ({dayChange}%)", f"Top Gainer, Volume: {volume}, RelVol: {relativeVolAtTime}x, MCap: ${marketCapText}B")
            discordManager.sendDiscordGainersPost('tmp/test.png')

        if(dateString == str(datetime.datetime.now().date())):
            if(type == "MR"):
                mpf.plot(df, type='candle', volume=True, title=tick, hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
                discordManager.sendDiscordEmbed(tick + f" PC:{prevClose} >> PM$:{pmPrice} ▼ {pmChange} ({gapValuePercent}%)", f"MR {z}")
                discordManager.sendDiscordPost('tmp/test.png')
            if(type == "EP"):
                mpf.plot(df, type='candle', volume=True, title=tick, hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
                discordManager.sendDiscordEmbed(tick + f" {prevClose} >> PM$:{pmPrice} ▲ {pmChange} ({gapValuePercent}%)", f"EP {z}")
                discordManager.sendDiscordPost('tmp/test.png')
            if(type == "NEP"):
                mpf.plot(df, type='candle', volume=True, title=tick, hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
                discordManager.sendDiscordEmbed(tick + f" {prevClose} >> PM$:{pmPrice} ▼ {pmChange} ({gapValuePercent}%)", f"NEP {z}")
                discordManager.sendDiscordPost('tmp/test.png')
            if(type == "Pivot"):
                mpf.plot(df, type='candle', volume=True, title=tick, hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
                discordManager.sendDiscordEmbed(tick + f" {prevClose} >> PM$:{pmPrice} ▼ {pmChange} ({gapValuePercent}%)", f"Pivot {z}")
                discordManager.sendDiscordPost('tmp/test.png')
        else:
            if(type == "MR"):
                mpf.plot(df, type='candle', volume=True, title=tick, vlines=dict(vlines=[dateString],linewidths=(1), alpha=0.25), style=s, savefig=ourpath)
                discordManager.sendDiscordEmbed(tick + f" {prevClose} >> {setupDayOpen} ▼ {pmChange} ({gapValuePercent}%)", f"MR {z}")
                discordManager.sendDiscordPost('tmp/test.png')
            if(type == "EP"):
                mpf.plot(df, type='candle', volume=True, title=tick, vlines=dict(vlines=[dateString],linewidths=(1), alpha=0.25), style=s, savefig=ourpath)
                discordManager.sendDiscordEmbed(tick + f" {prevClose} >> {setupDayOpen} ▲ {pmChange} ({gapValuePercent}%)", f"EP {z}")
                discordManager.sendDiscordPost('tmp/test.png')
            if(type == "NEP"):
                mpf.plot(df, type='candle', volume=True, title=tick, vlines=dict(vlines=[dateString],linewidths=(1), alpha=0.25), style=s, savefig=ourpath)
                discordManager.sendDiscordEmbed(tick + f" {prevClose} >> {setupDayOpen} ▼ {pmChange} ({gapValuePercent}%)", f"NEP {z}")
                discordManager.sendDiscordPost('tmp/test.png')
            if(type == "Pivot"):
                mpf.plot(df, type='candle', volume=True, title=tick, vlines=dict(vlines=[dateString],linewidths=(1), alpha=0.25), style=s, savefig=ourpath)
                discordManager.sendDiscordEmbed(tick + f" {prevClose} >> {setupDayOpen} ▼ {pmChange} ({gapValuePercent}%)", f"Pivot {z}")
                discordManager.sendDiscordPost('tmp/test.png')

if __name__ == "__main__":
    tv = TvDatafeed()
    mc = mpf.make_marketcolors(up='g',down='r')
    s  = mpf.make_mpf_style(marketcolors=mc)
    ourpath = pathlib.Path("C:/Screener/tmp") / "test.png"
    data_apple = tv.get_hist('AAPL', 'NASDAQ', n_bars=50)
    print(datetime.datetime.now())
    mpf.plot(data_apple, type='candle', volume=True, title='AAPL', style=s, savefig=ourpath)
    print(datetime.datetime.now())


