
from discordwebhook import Discord
import pathlib
import mplfinance as mpf
import statistics
import pandas as pd
import datetime
from Data5 import Data

discordtopGainers = Discord(url="https://discord.com/api/webhooks/1071666210514669648/dSLYGAB5CWQuulV46ePmExwgljauPexCG10R2ZqZctTl7lyya-Zs7lJ7ecLjQEruAfYw")
discordintraday = Discord(url="https://discord.com/api/webhooks/1071667193709858847/qwHcqShmotkEPkml8BSMTTnSp38xL1-bw9ESFRhBe5jPB9o5wcE9oikfAbt-EKEt7d3c")
discord = Discord(url="https://discord.com/api/webhooks/1071506429229416519/41ps0qlsiiFRDLxnZVCF5KuDtb_SWBHCwB5scK-YUf96mrBpzZRydsT2C4GiGPDAEmKW")

class Log:
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



    def intraday(df,currentday, tf, ticker, z, path, st):
        mc = mpf.make_marketcolors(up='g',down='r')
        s  = mpf.make_mpf_style(marketcolors=mc)
        ourpath = pathlib.Path("C:/Screener/tmp")/ 'test.png'
        z = round(z, 3)
        df = df[-100:]
        df.set_index('datetime', inplace = True)
        mpf.plot(df, type='candle', mav=(10, 20), volume=True, title=f'{ticker}, {st}, {z}, {tf}', style=s, savefig=ourpath)
        Log.sendDiscordIntradayPost('tmp/test.png')

    def log(df,currentday, tf, ticker, z, path, st):
 
        if path == 2:
            
            
            Log.intraday(df,currentday, tf, ticker, z, path, st)
            
        if path == 1:
            
            if df.iloc[currentday][0] == datetime.date.today(): 
                dateString = '0'
            else:
                dateString = df.iloc[currentday][0]
            pmPrice = df.iloc[currentday][1]
            data ={'Date': [dateString],
                    'Ticker':[ ticker],
                    'Setup': [str(st)],
                    'Z': [z],
                    'tf':[tf]}
        
            dfadd = pd.DataFrame(data)
            dfadd.to_csv((r"C:/Screener/tmp/todays_setups.csv"), mode='a', index=False, header=False)

        if path == 0 and False:
           

    
        
            cooldown = 20

            dateString = str(data_daily.iloc[currentday][0])
            
           
            
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
            
            

            prevdate = data_daily.index[currentday - 1]


            try:
                scan = pd.read_csv(r"C:\Screener\tmp\setups.csv", header = None)

            
                scanholder = pd.DataFrame()
                for k in range(len(scan)):
                    if scan.iloc[k][1] == tick:
                        scanholder = pd.concat([scanholder,scan.iloc[[k]]])
                scan = scanholder

                scanholder = pd.DataFrame()
                for k in range(len(scan)):
                    if scan.iloc[k][2] == setup_type:
                        scanholder = pd.concat([scanholder,scan.iloc[[k]]])
                scan = scanholder
                
                
                try:
                    str_recent_date = scan.iloc[-1][0]
                    recent_date = datetime.datetime.strptime(str_recent_date, '%Y-%m-%d').date()
                    #today_date = datetime.datetime.strptime(dateToSearch, '%Y-%m-%d').date()
                    today_date = dateToSearch.date()
                    delta = (today_date - recent_date).days
                    #print(f"{delta} , {tick}")
                    if delta <= cooldown:
                        exclude = True
                        # print(f"excluded {tick} ///////////////////////")
                    
                    else:
                        exclude = False
                except IndexError:
                    exclude = False
            except pd.errors.EmptyDataError:
                exclude = False
            #except IndexError:
                # exclude = False

            

            if not exclude:
            
                


           
                gap = round( (data_daily.iloc[currentday][1]/data_daily.iloc[currentday-1][4] - 1)*100,2)

                volma = []
                for i in range(10):
                    volma.append(data_daily.iloc[currentday-1-i][5])
                vol = round((data_daily.iloc[currentday][5]/statistics.mean(volma) ),2)

                q_data = Data.get('QQQ')#pd.read_csv("C:/Screener/data_csvs/QQQ_data.csv")
                qcurrentday = Data.findex(q_data, dateToSearch)
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
                four = round((data_daily.iloc[currentday+3][4] / data_daily.iloc[currentday][1] - 1) * 100,2)
                five = round((data_daily.iloc[currentday+4][4] / data_daily.iloc[currentday][1] - 1) * 100,2)

                change10 = round((data_daily.iloc[currentday-1][4] / data_daily.iloc[currentday-11][4] - 1) * 100,2)
                change20 = round((data_daily.iloc[currentday-1][4] / data_daily.iloc[currentday-21][4] - 1) * 100,2)
                change60 = round((data_daily.iloc[currentday-1][4] / data_daily.iloc[currentday-61][4] - 1) * 100,2)
                change250 = round((data_daily.iloc[currentday-1][4] / data_daily.iloc[currentday-251][4] - 1) * 100,2)
                            
              


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
                    close = data_daily.iloc[currentday+i][4]

                    if i == 0:
                        if close > ma10:
                            short = False
                        else:
                            short = True

                    if short:
                        if close > ma10:
                            break
                    else:
                        if ma10 > close:
                            break
                   
                    
                    if i > 150:
                        break

                    i += 1

                ten = round( (data_daily.iloc[currentday+i][4] / data_daily.iloc[currentday][1] - 1)*100,2)
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
                        #'rating': [""],
                        'time': [time],
                        'timeframe': [tf]
  
                        }
        
                dfadd = pd.DataFrame(data)


            
            
                dfadd.to_csv((r"C:/Screener/tmp/setups.csv"), mode='a', index=False, header=False)
            
            

            


