from discordwebhook import Discord
import pathlib
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




    def post(self,screenbar,z,channel):
        tick = str(screenbar['Ticker'])
        exchange = str(screenbar['Exchange'])
        pmChange = screenbar['Pre-market Change']
        prevcloseprice = screenbar['Price']
        volume = screenbar['Volume']
        dolVol = screenbar['Volume*Price']

        todayGapValuePercent = todayGapValue*100;



        z = round(z, 3)


        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)



        ourpath = pathlib.Path("C:/Screener/tmp") / "test.png"
        
        mpf.plot(data_daily, type='candle', mav=(10, 20), volume=True, title=tick, hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
        dM.sendDiscordEmbed(tick + f" {prevClose} >> {pmPrice} ▲ {pmChange} ({todayGapValuePercent}%)", f"EP Setup, Z-Score: {z}")
        dM.sendDiscordPost('tmp/test.png')

        z = round(z, 3)
        ourpath = pathlib.Path("C:/Screener/tmp") / "test.png"
        todayGapValuePercent = todayGapValue*100;
        mpf.plot(data_daily, type='candle', mav=(10, 20), volume=True, title=tick, hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
        dM.sendDiscordEmbed(tick + f" {prevClose} >> {pmPrice} ▼ {pmChange} ({todayGapValuePercent}%)", f"NEP Setup, Z-Score: {z}")
        dM.sendDiscordPost('tmp/test.png')


        z = round(z, 3)
        ourpath = pathlib.Path("C:/Screener/tmp") / "test.png"
        todayGapValuePercent = todayGapValue*100;
        mpf.plot(data_daily, type='candle', mav=(10, 20), volume=True, title=tick, hlines=dict(hlines=[pmPrice], linestyle="-."), style=s, savefig=ourpath)
        dM.sendDiscordEmbed(tick + f" {prevClose} >> {pmPrice} ▲ {pmChange} ({todayGapValuePercent}%)", f"MR Setup, Z-Score: {z}")
        dM.sendDiscordPost('tmp/test.png')



        ourpath = pathlib.Path("C:/Screener/tmp") / "test3.png"
                openCandlePrice = float(data_100.iloc[len(data_100)-1][1])
                changePrice = round(float(currPrice - openCandlePrice), 2)
            
                marketCapText = round((marketCap / 1000000000), 2)
            
                mpf.plot(data_100, type='candle', volume=True, title=tick, style=s, savefig=ourpath)
                dM.sendDiscordEmbedIntraday(tick + f" {openCandlePrice} >> Current: {currPrice} ▲ {changePrice} ({change}%)", f"Intraday % Gaining Setup, Volume: {volume}, RelVol: {relativeVolAtTime}x, MCap: ${marketCapText}B")
                dM.sendDiscordIntradayPost('tmp/test3.png')


                changeFromOpen = screener_data.iloc[i]['Change from Open']
            openValue = screener_data.iloc[i]['Open']
            
            pmChange = screener_data.iloc[i]['Pre-market Change']
            
            marketCap = float(screener_data.iloc[i]['Market Capitalization'])
            relativeVolAtTime = round(screener_data.iloc[i]['Relative Volume at Time'], 1)


