from Data7 import Data as data
from Scan import Scan as scan

import pandas as pd
import statistics
import mplfinance as mpf
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import random

from multiprocessing  import Pool







date_list = ['2023-03-29','2022-11-10','2022-09-13','2022-08-10','2022-07-27',
			 '2022-11-10','2023-01-06','2023-01-20']

ticker_list = ['qqq','qqq','qqq','qqq','qqq',
			   'mgni','aehr','nflx','coin']


tickers = scan.get().index.to_list()
test = False
c = -1
while True:
	c += 1
	try:
		if not test:
			dh = random.randint(0,len(tickers) - 1)
			ticker = tickers[dh]
			dfg = data.get(ticker)
			ind = random.randint(0,len(dfg)-1)
			date = dfg.index[ind]
		else:
			ticker = ticker_list[c]
			date = date_list[c]
		l = 20
		z_filter = 2
		df = data.get(ticker)
		index = data.findex(df,date)+1
		df = df[index - 200:index]
		current = len(df) - 1


		########################################################################
		dat = []
		for i in range(l):
			k = i - l
			val = df.iat[current + k,0] / df.iat[current + k -1,3] - 1
			dat.append(val)

		val = df.iat[current,0] / df.iat[current - 1,3] - 1
		z = (val - statistics.mean(dat))/statistics.stdev(dat)


		close1 = df.iat[current-1,3]
		close2 = df.iat[current-2,3]
		close3 = df.iat[current-3,3]
		open0 = df.iat[current,0]
		open2 = df.iat[current-2,0]
		open1 = df.iat[current - 1,0]
		high1 = df.iat[current - 1,1]

		ma10 = []
		for i in range(10):
			ma10.append(df.iat[current-i-1,3])
		ma10 = statistics.mean(ma10) 


		dol_vol_l = 5
       

        
		dolVol = []
		for i in range(dol_vol_l):
			dolVol.append(df.iat[current-1-i,3]*df.iat[current-1-i,4])
		dolVol = statistics.mean(dolVol)              
            
		atr= []
		adr_l = 14
		for j in range(adr_l): 
			high = df.iat[current-j-1,1]
			low = df.iat[current-j-1,2]
			val = (high - low ) 
			atr.append(val)
		atr = statistics.mean(atr)  

		vol_filter = 5 * 1000000

		setup = False
		if z > z_filter:

			if close1 < close2 and close1 < open1 and open0 > close1 and open0 > high1 and open0 > ma10  and dolVol > vol_filter and close2/open2 - 1 < .01 :

				setup = True


###########################################################################################
		mc = mpf.make_marketcolors(up='g',down='r')
		s  = mpf.make_mpf_style(marketcolors=mc)
		if setup or test:

			high = 0
			low = df.iat[current-1,2]
			for i in range(3):
				val = df.iat[current-i,0]
				if val > high:
					high = val
				


			val = (high - low)/atr
			if test:
				mpf.plot(df, type='candle', style=s,title = str(f' {setup} , {round(z,3)} , {val} '))#, alpha = .25))#vlines=dict(vlines=[line],
			else:
				mpf.plot(df, type='candle', style = s, title = str(val))#, alpha = .25))#vlines=dict(vlines=[line],


	except:
		pass
