
import statistics
from Log3 import Log as log

from flag import Flag as flag
from pivot import Pivot as pivot

import datetime

from Data7 import Data as data
from sklearn.linear_model import LinearRegression
import numpy as np
from Scan import Scan

class Detection:

   

	def check(bar):
		
		ticker = bar[0]
	
		tf = bar[1]
		path = bar[2]
		date_list = bar[3]
		
		date = date_list[0]
		
		
		try:
			dff = data.get(ticker,tf,date)
			
		except KeyError:
			pass
		
		except FileNotFoundError:
			
			return
		

		except TypeError:
			
			return
		
		if len(dff) > 20:
		
			for date in date_list:
				try:
				
				
					currentday = data.findex(dff,date)
					
					if currentday != None and currentday > 15:
						
						length = 500
						start = currentday - length
						if start < 0:
							start = 0
						df = dff[start:currentday + 50]
						currentday = data.findex(df,date)
					
						dolVol, adr, pmDolVol = Detection.requirements(df,currentday,path,ticker)
	
						if tf == 'd':
							
							
							if dolVol > 1000000 and adr > 3:
								if   ((datetime.datetime.now().hour) < 5 or (datetime.datetime.now().hour == 5 and datetime.datetime.now().minute < 40)) or True:
									sEP = True
									sMR = True
									sPivot = True
									sFlag = True
								else:
									sEP = False
									sMR = False
									sPivot = True
									sFlag = False
								dolVolFilter = 10000000
								
								if((dolVol > .2* dolVolFilter or pmDolVol  > 1 * 1000000)  and adr > 3.5 and sEP):
									Detection.EP(df,currentday, tf, ticker, path)
								if((dolVol > .7 * dolVolFilter or pmDolVol  > 1 * 1000000 )   and adr > 5 and sMR):
									Detection.MR(df,currentday, tf, ticker, path)
								if((dolVol > .8* dolVolFilter or pmDolVol  > 1 * 1000000)   and adr > 3.5 and sPivot):
									
									pivot.pivot(df,currentday, tf, ticker, path)
								if((dolVol > .7 * dolVolFilter or pmDolVol  > 1 * 1000000 ) and adr > 4 and sFlag):
									
									flag.flag(df,currentday, tf, ticker, path)
									
						if tf == '1min':
						
							if dolVol > 20000 and adr > .08:
							
								Detection.Pop(df,currentday, tf, ticker, path)



					
						if tf == '5min':
							if dolVol > 100000 and adr > .1:
								Detection.Pop(df,currentday, tf, ticker, path)
					
						if tf == 'h':
						
							pass
				except TimeoutError:
					pass
				except IndexError:
					pass
				except TypeError:
					pass
				except ValueError:
					pass
				
		#except Exception as e: print(e)
  
	def requirements(df,currentday,path,ticker):

		dol_vol_l = 5
		adr_l = 15

		try:
			if(currentday == None): 
				return 0, 0
			dolVol = []
			for i in range(dol_vol_l):
				dolVol.append(df.iat[currentday-1-i,3]*df.iat[currentday-1-i,4])
			dolVol = statistics.mean(dolVol)              
			adr= []
			for j in range(adr_l): 
				high = df.iat[currentday-j-1,1]
				low = df.iat[currentday-j-1,2]
				val = (high/low - 1) * 100
				adr.append(val)
			adr = statistics.mean(adr)  
			try:
				if path == 1:
					screenbar = Scan.Scan.get('0','d').loc[ticker]
					pmvol =  screenbar['Pre-market Volume']

					pmprice = df.iat[currentday,0]
					pmDolVol = pmvol * pmprice
				else:
					pmDolVol = 0
			except:
				print('pm vol failed')
				pmDolVol = 0

			return dolVol, adr, pmDolVol
		except:
			return 0 ,0 , 0
		   
	def Pop(df,currentday, tf, ticker, path):
		i = 0
		zfilter = 10
		data = []
		length = 500
		x = df.iat[currentday - i,4] + df.iat[currentday - i-1,4]
		y = ((df.iat[currentday - i,3]/df.iat[currentday - i,0]) + (df.iat[currentday - i,3]/df.iat[currentday - i,0]) - 2)
		current_value = x*pow(y,2)
		df = df[currentday-length:currentday + 1]
		currentday = length - 1
		for i in range(length): 
			x = df.iat[currentday - i-1, 4] + df.iat[currentday - i-2,4]
			y = ((df.iat[currentday - i-1,3]/df.iat[currentday - i-1,0]) + (df.iat[currentday - i-1,3]/df.iat[currentday - i-1,0]) - 2)
			value = x*pow(y,2)
			data.append(value)
	
		z = (current_value - statistics.mean(data))/statistics.stdev(data)
	
		if ((z < -zfilter) or (z > zfilter)):
			log.log(df,currentday, tf, ticker, z, path , 'Pop')  
   
	def EP(df,currentday, tf, ticker, path):
		pmPrice = df.iat[currentday,0]
		
		zfilter = 5.5

		prevClose = df.iat[currentday-1,3]
		gaps = []
		lows = []
		highs = []
		todayGapValue = ((pmPrice/prevClose)-1)
		for j in range(20): 
			gaps.append((df.iat[currentday-1-j,0]/df.iat[currentday-2-j,3])-1)
			lows.append(df.iat[currentday-j-1,2])
			highs.append(df.iat[currentday-j-1,1])

		z = (todayGapValue-statistics.mean(gaps))/statistics.stdev(gaps)
		   
		
		if(z > zfilter) and pmPrice > max(highs):
			log.log(df,currentday, tf, ticker, z, path, 'EP')  
			
		elif (z < -zfilter) and pmPrice < min(lows):
			log.log(df,currentday, tf, ticker, z, path , 'NEP')  

 
	def MR(df,currentday, tf, ticker, path):
		
		
		pmPrice = df.iat[currentday,0]
		
		zfilter = 3.5
		gapzfilter0 = 5.5
		gapzfilter1 = 4
		changezfilter = 2.5
	  
		prevClose = df.iat[currentday-1,3]
		zdata = []
		zgaps = []
		zchange = []
			
		
		if df.iat[currentday-1,3] < df.iat[currentday-1,0] and df.iat[currentday-2,3] < df.iat[currentday-2,0] and df.iat[currentday-3,3] < df.iat[currentday-3,0]:

			  
			for i in range(30):
				n = 29-i
				gapvalue = abs((df.iat[currentday-n-1,0]/df.iat[currentday-n-2,3]) - 1)
				changevalue = abs((df.iat[currentday-n-1,3]/df.iat[currentday-n-1,0]) - 1)
				lastCloses = 0
					
				for c in range(4): 
					
					lastCloses += df.iat[currentday-2-c-n,3]
				fourSMA = (lastCloses/4)
				datavalue = abs(fourSMA/df.iat[currentday-n-1,0] - 1)
				if i == 29:
					gapz1 = (gapvalue-statistics.mean(zgaps))/statistics.stdev(zgaps)
				zgaps.append(gapvalue)
				zchange.append(changevalue)
				if i > 14:
					zdata.append(datavalue)

			 
			todayGapValue = abs((pmPrice/prevClose)-1)
			todayChangeValue = abs(df.iat[currentday-1,3]/df.iat[currentday-1,0] - 1)
			lastCloses = 0
			for c in range(4): 
				lastCloses = lastCloses + df.iat[currentday-c-1,3]
				
			fourSMA = (lastCloses/4)
			value = (fourSMA)/pmPrice - 1


			
			gapz = (todayGapValue-statistics.mean(zgaps))/statistics.stdev(zgaps)
			changez = (todayChangeValue - statistics.mean(zchange))/statistics.stdev(zchange) 
			z = (abs(value) - statistics.mean(zdata))/statistics.stdev(zdata) 
				
			  
			if (gapz1 < gapzfilter1 and gapz < gapzfilter0 and changez < changezfilter and z > zfilter and value > 0):
			  
			   
				log.log(df,currentday, tf, ticker, z, path, 'MR')  
			   
	  
	def Pivot(df,current, tf, ticker, path):
	   

		atr= []
		adr_l = 14
		for j in range(adr_l): 
			high = df.iat[current-j-1,1]
			low = df.iat[current-j-1,2]
			val = (high - low ) 
			atr.append(val)
		atr = statistics.mean(atr) 



		z_filter = 1.5
		coef_filter = .5

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
	
		if coef > coef_filter and z > z_filter and df.iat[current-2,3] > df.iat[current-1,3] and df.iat[current-2,3] - df.iat[current-2,0] < atr/3  and df.iat[current,0] > df.iat[current-1,0]:
		
			log.log(df,current, tf, ticker, z, path, 'P')   

		if coef > coef_filter and z < -z_filter and df.iat[current-2,3] < df.iat[current-1,3] and df.iat[current-2,0] - df.iat[current-2,3] < atr/3  and df.iat[current,0] < df.iat[current-1,0]:


			log.log(df,current, tf, ticker, z, path, 'NP') 




	

	  

