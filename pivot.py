from Data7 import Data as data
from Scan import Scan as scan

import datetime

import pandas as pd
import statistics
import mplfinance as mpf
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import random
from Log3 import Log as log
from multiprocessing  import Pool





class Pivot:
	def pivot(df,current, tf, ticker, path):


		########################################################################
		
		z_filter = 1.5
		coef_filter = .5
		
		
		atr= []
		adr_l = 14
		for j in range(adr_l): 
			high = df.iat[current-j-1,1]
			low = df.iat[current-j-1,2]
			val = (high - low ) 
			atr.append(val)
		atr = statistics.mean(atr) 

		i = 2

		def MA(df,i,l):
			ma = []
			for j in range(l):
				ma.append(df.iat[i-j,3])
			return statistics.mean(ma)

		ma = MA(df,current-1,2)
		while True:
			prevma = MA(df,current-i,2)
			if ma > prevma or i > 10:
				break

			ma = prevma
			i += 1

		i -= 1
	
		d = []
		for k in range(20):
			c = df.iat[current - 2 - k,3]
			o = df.iat[current - 1 - k,0]
			d.append(o/c - 1)

		val = df.iat[current,0]/df.iat[current-1,3] - 1
		z = (val - statistics.mean(d))/statistics.stdev(d)

		coef = (df.iat[current,0] - df.iat[current-1,3])/(df.iat[current-i,0] - df.iat[current-1,3])
		setup  = None
		#if coef > coef_filter and z > z_filter and df.iat[current-2,3] > df.iat[current-1,3] and df.iat[current-2,3] - df.iat[current-2,0] < atr/3 and df.iat[current,0] > df.iat[current-1,0]:
		#	setup = 'P'

		if coef > coef_filter and z < -z_filter and df.iat[current-2,3] < df.iat[current-1,3] and df.iat[current-2,0] - df.iat[current-2,3] < atr/3  and df.iat[current,0] < df.iat[current-1,0]:
			setup = 'NP'

		mc = mpf.make_marketcolors(up='g',down='r')
		s  = mpf.make_mpf_style(marketcolors=mc)
		if setup != None:

			high = 0
			low = df.iat[current-1,2]
			for i in range(3):
				val = df.iat[current-i,0]
				if val > high:
					high = val
				
			val = (high - low)/atr
			if path == None:
				mpf.plot(df, type='candle', style=s,title = str(f' {setup} , {round(z,3)} , {coef} '))
			else:
				log.log(df,current, tf, ticker, z, path, setup)  




if __name__ == '__main__':

	date_list = ['2021-05-20','2023-03-29','2022-11-10','2022-09-13','2022-08-10','2022-07-27',
				 '2022-11-10','2023-01-06','2023-01-20','2023-01-09']

	ticker_list = ['coin','qqq','qqq','qqq','qqq','qqq',
				   'mgni','aehr','nflx','coin']


	tf = 'd'

	tickers = scan.get().index.to_list()
	test = False
	ccccc = -1


	startdate = datetime.date(2020, 1, 1)
	enddate = datetime.datetime.now()# - datetime.timedelta(date_buffer)
                



	sample = data.get('AAPL',tf)
	start_index = data.findex(sample,startdate)  
	end_index = data.findex(sample, enddate)
            
	#print(f'{start_index} , {end_index}')
	trim = sample[start_index:end_index]
	date_list = trim.index.tolist()




	while True:
		ccccc += 1
		try:
			if not test:
				dh = random.randint(0,len(tickers) - 1)
				ticker = tickers[dh]
				dfg = data.get(ticker)
				ind = random.randint(0,len(dfg)-1)
				date = dfg.index[ind]
			else:
				ticker = 'spy'#ticker_list[ccccc]
				date = date_list[ccccc]
			l = 20
			z_filter = 2
			df = data.get(ticker)
			index = data.findex(df,date)+1
			df = df[index - 200:index]
			current = len(df) - 1

			dol_vol_l = 5
			dolVol = []
			for i in range(dol_vol_l):
				dolVol.append(df.iat[current-1-i,3]*df.iat[current-1-i,4])
			dolVol = statistics.mean(dolVol)              
		
			vol_filter = 5 * 1000000
			path = None
			if dolVol > vol_filter:
				Pivot.pivot(df,current, tf, ticker, path)



		except:
			pass




