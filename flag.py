

from Data7 import Data as data
from Scan import Scan as scan
from Log3 import Log as log

import pandas as pd
import statistics
import mplfinance as mpf
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import random

gosh = 1

upper_stdev_filter = 1.5

lower_stdev_filter = .75


upper_stdev_filter2 = 1.5

lower_stdev_filter2 = 1






			


	


class Flag:
	def flag(df,current, tf, ticker, path):

		

		lmax = 100
		lmin = 7
		mal = 5
		mal2 = 2
		coef = 0.01

		swings = np.empty([0,3])
		slope = 0
		prevma = []
		end = False
		def MA(df,i,l):
			ma = []
			for j in range(l):
				ma.append(df.iat[i-j,3])
			return statistics.mean(ma)
		ma = MA(df,current - 1,mal)
		i = 2
		while True:
			prevma = MA(df,current - i,mal)
			if slope == 1 and ma < prevma:
				slope = -1
				add = df.iat[current-i,3]
				swings = np.append(swings,[[add,i,0]],axis = 0)
				if end:
					break
			elif slope == -1 and ma > prevma:
				slope = 1
				add = df.iat[current-i,3]
				swings = np.append(swings,[[add,i,1]],axis = 0)
				if end:
					break
			elif slope == 0:
				if ma > prevma:
					slope = 1
				else:
					slope = -1
			if i >= lmax:
				end = True
			ma = prevma
			i += 1
		lval = 0
		l = 0
		for i in range(len(swings)-1):
			val = abs(swings[i,0]/swings[i+1,0] - 1) * (1 - coef * swings[i,1])
			if val > lval:
				lval = val
				move_size = abs(swings[i,0] - swings[i+1,0])
				l = swings[i,1] + int(mal/2)
		slope = 0
		swings = np.empty([0,3])
		ma = MA(df,current - 1,mal)
		i = 2
		end = False
		while True:
	
			prevma = MA(df,current - i,mal2)
			if slope == 1 and ma < prevma:
				slope = -1
	
				#add = df.iat[current-i+1,3]
				#add = prevma
				add = df.iat[current-i,3]
				swings = np.append(swings,[[add,i,0]],axis = 0)
				add = df.iat[current-i,2]

				swings = np.append(swings,[[add,i,0]],axis = 0)
				if end:
					break
			elif slope == -1 and ma > prevma:
		
				slope = 1
				#add = df.iat[current-i+1,3]
				#add = prevma
				add = df.iat[current-i,3]
				swings = np.append(swings,[[add,i,1]],axis = 0)
				add = df.iat[current-i,1]
				swings = np.append(swings,[[add,i,1]],axis = 0)
				if end:
					break
			elif slope == 0:
				if ma > prevma:
					slope = 1
				else:
					slope = -1

			if i >= lmax:
				end = True
			ma = prevma
			i += 1

		
		if l >= lmin and l < lmax:
			
			i = 0


			#get swing points within l

			while True:
				if swings[i,1] > l:
					swings = swings[0:i]
					break
				i += 1




			#sort swings into highs and lows

			n = len(swings)

			xh = np.empty([0,1])
			yh = np.empty(0)
			xl = np.empty([0,1])
			yl = np.empty(0)

			all_swings = []

			for i in range(n):
				high = swings[i,2]
		
				if high == 1:
			
					xh = np.append(xh,[[swings[i,1]]],axis = 0)
					yh = np.append(yh,swings[i,0])
				else:
			
					xl = np.append(xl,[[swings[i,1]]],axis = 0)
					yl = np.append(yl,swings[i,0])

				all_swings.append(swings[i,0])


			#add most recent andle

			


			#fitler out high stdev points

	

			stdev = np.std(yl)
			mean = np.mean(yl)#df.iat[current,3]# statistics.mean(all_swings)#df.iat[current,3]#np.mean(yh)






			x = np.empty(0)
			y = np.empty(0)

			for i in range(len(xl)):
				val = yl[i] 
				date = -xl[i,0]
				x = np.append(x,date)
				y = np.append(y,(val-mean)/stdev)

			#plt.scatter(x,y)
			#plt.show()

			for i in range(len(yl) -1,-1,-1):
				z = (yl[i] - mean)/stdev
				if z < -upper_stdev_filter2 or z > lower_stdev_filter2:
					yl = np.delete(yl,i)
					xl = np.delete(xl,i,axis = 0)


			stdev = np.std(yh)
			mean = np.mean(yh)
			x = np.empty(0)
			y = np.empty(0)

			for i in range(len(xh)):
				val = yh[i] 
				date = -xh[i,0]
				x = np.append(x,date)
				y = np.append(y,(val-mean)/stdev)

			#plt.scatter(x,y)
			#plt.show()

	
			for i in range(len(yh) -1,-1,-1):
				z = (yh[i] - mean)/stdev
				if z > upper_stdev_filter or z < -lower_stdev_filter:
					yh = np.delete(yh,i)
					xh = np.delete(xh,i,axis = 0)

	
				#plot after
			x = np.empty(0)
			y = np.empty(0)

			for i in range(len(xh)):
				val = yh[i] 
				date = -xh[i,0]
				x = np.append(x,date)
				y = np.append(y,val)




	

			modelh = LinearRegression().fit(xh, yh)

			bh = modelh.intercept_

			mh = modelh.coef_

			modell = LinearRegression().fit(xl, yl)

			bl = modell.intercept_

			ml = modell.coef_


			x1 = str(df.index[-l])

			x2 = str(df.index[-1])

			y1 = float(l*mh + bh)

			y2 = float(0*mh + bh)

			xl1 = str(df.index[-l])

			xl2 = str(df.index[-1])

			yl1 = float(l*ml + bl)

			yl2 = float(0*ml + bl)

			points = [(x1,y1),(x2,y2) , (xl2,yl2),(xl1,yl1)]
			#[(xl2,yl2),(xl1,yl1)]
			

	



			tightening = mh - ml

			tightness = bh - bl#abs(((mh*(l/2) + bh ) - ( ml * (l/2) + bl)) )

			higher_lows = -ml

			z = move_size / tightness

			atr= []
			adr_l = int(l)
			for j in range(adr_l): 
				high = df.iat[current-j-1,1]
				low = df.iat[current-j-1,2]
				val = (high - low ) 
				atr.append(val)
			atr = statistics.mean(atr)  

			flag = False


			oc = (df.iat[current - 1,0] + df.iat[current - 1,3])/2

			oc_now = (df.iat[current ,0] + df.iat[current ,3])/2

			avg_slope = ((abs(ml) + abs(mh))/2)

			
			high = df.iat[current,1]

			low = df.iat[current,2]

			prev_close =df.iat[current-1,3]

			prev_high = df.iat[current-1,1]

			prev_low = df.iat[current-1,2]

			setup = 'None'

			

			if (bh > bl and 
			z >3  and
			bh + mh*l > bl + ml*l 
			and oc < bh): 
				
				if oc < bh and oc > bl:
				
					if prev_close < bh and prev_close > bl:
						val = avg_slope / atr
						

						if val < .1:
							
							val2 = tightening/atr
							val5 = (avg_slope*pow(l,.7))/atr
							if val2 > 0 and val5 < .65:
							
								flag = True
								
						
			if  flag: #or test :


				try:
					val = val[0]
				except:
					pass
				try:
					val2 = val2[0]
				except:
					pass
				
				


				line = df.index[-l]
				mc = mpf.make_marketcolors(up='g',down='r')
				s  = mpf.make_mpf_style(marketcolors=mc)
				
				if path == None:
					#if val5 > .35 and val5 < .4:
					mpf.plot(df, type='candle', style=s, alines = points, title = f'{ticker} , {date} , {val5}')#, alpha = .25))#vlines=dict(vlines=[line],

						#mpf.plot(df, type='candle', style=s,vlines=dict(vlines=[line]))

				else:

					
					log.log(df,current, tf, ticker, l, path, 'Flag')   


	
if __name__ == '__main__':
	

	date_list = ['2022-07-28','2023-03-31','2023-03-10','2023-03-30','2020-08-13','2020-11-10','2023-01-05',
				 '2023-01-04','2023-02-16','2023-03-22','2023-01-04','2023-01-04',
				 '2022-01-05','2022-10-18','2023-01-03','2022-12-09','2022-09-06',
				 '2023-03-31','2022-04-11','2022-04-11','2022-08-04','2022-09-22',
				 '2023-08-03']

	ticker_list = ['enph','dpst','riot','meli','tsla','tsla','elf',
				   'mlco','mlco','aehr','cweb','tme',
				   'nue','kold','orcl','amat','enph',
				   'mdb','pump','oxy','mrna','celh',
				   'rytm']


	tickers = scan.get().index.to_list()
	test = True
	c = -1
	index = -1
	while True:
		c += 1
		try:
			index += 1
			if not test:
				dh = random.randint(0,len(tickers) - 1)
				ticker = tickers[dh]

				dfg = data.get(ticker)
				ind = random.randint(0,len(dfg)-1)

				date = dfg.index[ind]
			else:
				ticker = 'amzn'#ticker_list[c]
				#date = date_list[c]



			df = data.get(ticker)
			#index = data.findex(df,date)
			df = df[index - 200:index]
			current = len(df) - 1



			dol_vol_l = 5
			dolVol = []
			for i in range(dol_vol_l):
				dolVol.append(df.iat[current-1-i,3]*df.iat[current-1-i,4])
			dolVol = statistics.mean(dolVol)  

			tf = 'd'
			path = None
			dol_vol_filter = 10*1000000

			if dolVol > dol_vol_filter:
				Flag.flag(df,current, tf, ticker, path)

		except:
			pass

