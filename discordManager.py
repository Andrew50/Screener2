from discordwebhook import Discord
import pathlib
import mplfinance as mpf
import matplotlib as mpl

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
        setup_df = df
        tick = str(screenbar['Ticker'])
        exchange = str(screenbar['Exchange'])
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
        relativeVolAtTime = round(screenbar['Relative Volume at Time'], 1)
        prevClose = setup_df.iloc[len(setup_df)-1][4]
        pmPrice = round((prevClose + pmChange), 2)
        if(currentDay == "0"):
            todayGapValuePercent = dayChange;
        if(currentDay == 80):
            todayGapValuePercent = round((pmPrice/currPrice), 2)
        z = round(z, 3)
        
        marketCapText = round((marketCap / 1000000000), 2)
        if(currentDay == "0"):
            lengthDf = len(setup_df)
            setup_df = setup_df[lengthDf - 80:]


        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        ourpath = pathlib.Path("C:/Screener/tmp") / "test.png"
        if(type == "Pop"):
            openCandlePrice = float(setup_df.iloc[len(setup_df)-1][1])
            changePrice = round(float(currPrice - openCandlePrice), 2)
            mpf.plot(setup_df, type='candle', mav=(10, 20), volume=True, title=tick, style=s, savefig=ourpath)
            discordManager.sendDiscordEmbedIntraday(tick + f" {openCandlePrice} >> Current: {currPrice} ▲ {changePrice} ({change}%)", f"Intraday % Gaining Setup, Volume: {volume}, RelVol: {relativeVolAtTime}x, MCap: ${marketCapText}B")
            discordManager.sendDiscordIntradayPost('tmp/test.png')

        if(type == "Gainer"):
            openCandlePrice = float(setup_df.iloc[len(setup_df)-1][1])
            changePrice = round(float(currPrice - openCandlePrice), 2)
            mpf.plot(setup_df, type='candle', mav=(10, 20), volume=True, title=tick, style=s, savefig=ourpath)
            discordManager.sendDiscordEmbedGainers(tick + f" {prevClose} >> {currPrice} ▲ {currPrice} ({dayChange}%)", f"Top Gainer, Volume: {volume}, RelVol: {relativeVolAtTime}x, MCap: ${marketCapText}B")
            discordManager.sendDiscordGainersPost('tmp/test.png')

        if(currentDay == (len(df)-1)):
            if(type == "MR"):
                datetime = str(df.index[currentDay])
                date = datetime.split()[0]
                mpf.plot(df, type='candle', volume=True, title=tick, vlines=dict(vlines=[date],linewidths=(1), alpha=0.25), hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
                discordManager.sendDiscordEmbed(tick + f" PC:{prevClose} >> PM$:{pmPrice} ▲ PMC:{pmChange} ({todayGapValuePercent}%)", f"MR Setup, Z-Score: {z}")
                discordManager.sendDiscordPost('tmp/test.png')
            if(type == "EP"):
                datetime = str(df.index[currentDay])
                date = datetime.split()[0]
                mpf.plot(df, type='candle', volume=True, title=tick, vlines=dict(vlines=[date],linewidths=(1), alpha=0.25), hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
                discordManager.sendDiscordEmbed(tick + f" {prevClose} >> {pmPrice} ▲ {pmChange} ({todayGapValuePercent}%)", f"MR Setup, Z-Score: {z}")
                discordManager.sendDiscordPost('tmp/test.png')
        else:
            if(type == "MR"):
                datetime = str(df.index[currentDay])
                date = datetime.split()[0]
                mpf.plot(df, type='candle', volume=True, title=tick, vlines=dict(vlines=[date],linewidths=(1), alpha=0.25), hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
                discordManager.sendDiscordEmbed(tick + f" {prevClose} >> {pmPrice} ▲ {pmChange} ({todayGapValuePercent}%)", f"MR Setup, Z-Score: {z}")
                discordManager.sendDiscordPost('tmp/test.png')
            if(type == "EP"):
                datetime = str(df.index[currentDay])
                date = datetime.split()[0]
                mpf.plot(df, type='candle', volume=True, title=tick, vlines=dict(vlines=[date],linewidths=(1), alpha=0.25), hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
                discordManager.sendDiscordEmbed(tick + f" {prevClose} >> {pmPrice} ▲ {pmChange} ({todayGapValuePercent}%)", f"MR Setup, Z-Score: {z}")
                discordManager.sendDiscordPost('tmp/test.png')




