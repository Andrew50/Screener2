
import statistics
from Log3 import Log as log

from Data7 import Data as data
from sklearn.linear_model import LinearRegression
import numpy as np

class Detection:

   

	def check(bar):
		
		ticker = bar[0]
		tf = bar[1]
		path = bar[2]
		date_list = bar[3]
		date = date_list[0]
		
		try:
			dff = data.get(ticker,tf,date)
			
		except FileNotFoundError:
			return
		

		except TypeError:
			return
		
		if len(dff) > 50:
			for date in date_list:
				try:
				
					currentday = data.findex(dff,date)
					
					if currentday != None:
						
						length = 500
						start = currentday - length
						if start < 0:
							start = 0
						df = dff[start:currentday + 50]
						currentday = data.findex(df,date)
					
						dolVol, adr = Detection.requirements(df,currentday)
						
						if tf == 'd':

							
							if dolVol > 1000000 and adr > 3:
								sEP = False
								sMR = False
								sPivot = False
								sFlag = True
								dolVolFilter = 10000000
			
								if(dolVol > .2* dolVolFilter  and adr > 3.5 and sEP):
									Detection.EP(df,currentday, tf, ticker, path)
								if(dolVol > .7 * dolVolFilter    and adr > 5 and sMR):
									Detection.MR(df,currentday, tf, ticker, path)
								if(dolVol > .8* dolVolFilter   and adr > 3.5 and sPivot):
									
									Detection.Pivot(df,currentday, tf, ticker, path)
								if(dolVol > .7 * dolVolFilter   and adr > 4 and sFlag):
									Detection.Flag(df,currentday, tf, ticker, path)

						if tf == '1min':
							
							if dolVol > 20000 and adr > .08:
							
								Detection.Pop(df,currentday, tf, ticker, path)
							
					
						if tf == '5min':
							if dolVol > 100000 and adr > .1:
								Detection.Pop(df,currentday, tf, ticker, path)
					
						if tf == 'h':
						
							pass
			
				except :
					pass

		#except Exception as e: print(e)
  
	def requirements(df,currentday):

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
			return dolVol, adr
		except:
			return 0 ,0
		   
	def Pop(df,currentday, tf, ticker, path):
		i = 0
		zfilter = 25
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
		
			log.log(df,current, tf, ticker, z, path, 'Pivot')   






	def Flag(df,currentday, tf, ticker, path):

		
		lmax = 100
		lmin = 7
		mal = 5

		upper_stdev_filter = 1.5
		lower_stdev_filter = .75
		upper_stdev_filter2 = 1.5

		lower_stdev_filter2 = 1
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
		ma = MA(df,currentday - 1,mal)
		i = 2
		while True:
			prevma = MA(df,currentday - i,mal)
			if slope == 1 and ma < prevma:
				slope = -1
				add = df.iat[currentday-i,3]
				swings = np.append(swings,[[add,i,0]],axis = 0)
				if end:
					break
			elif slope == -1 and ma > prevma:
				slope = 1
				add = df.iat[currentday-i,3]
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
		ma = MA(df,currentday - 1,mal)
		i = 2
		end = False
		while True:
	
			prevma = MA(df,currentday - i,mal2)
			if slope == 1 and ma < prevma:
				slope = -1
				add = df.iat[currentday-i,3]
				swings = np.append(swings,[[add,i,0]],axis = 0)
				add = df.iat[currentday-i,2]
				swings = np.append(swings,[[add,i,0]],axis = 0)
				if end:
					break
			elif slope == -1 and ma > prevma:
				slope = 1
				add = df.iat[currentday-i,3]
				swings = np.append(swings,[[add,i,1]],axis = 0)
				add = df.iat[currentday-i,1]
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
			while True:
				if swings[i,1] > l:
					swings = swings[0:i]
					break
				i += 1
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
			stdev = np.std(yl)
			mean = np.mean(yl)
			x = np.empty(0)
			y = np.empty(0)
			for i in range(len(yl) -1,-1,-1):
				z = (yl[i] - mean)/stdev
				if z < -upper_stdev_filter2 or z > lower_stdev_filter2:
					yl = np.delete(yl,i)
					xl = np.delete(xl,i,axis = 0)
			stdev = np.std(yh)
			mean = np.mean(yh)
			x = np.empty(0)
			y = np.empty(0)
			for i in range(len(yh) -1,-1,-1):
				z = (yh[i] - mean)/stdev
				if z > upper_stdev_filter or z < -lower_stdev_filter:
					yh = np.delete(yh,i)
					xh = np.delete(xh,i,axis = 0)
			modelh = LinearRegression().fit(xh, yh)
			bh = modelh.intercept_
			mh = modelh.coef_
			modell = LinearRegression().fit(xl, yl)
			bl = modell.intercept_
			ml = modell.coef_

			#calc traits
			tightening = mh - ml
			tightness = bh - bl
			higher_lows = -ml
			z = move_size / tightness
			atr= []
			adr_l = int(l)
			for j in range(adr_l): 
				high = df.iat[currentday-j-1,1]
				low = df.iat[currentday-j-1,2]
				val = (high - low ) 
				atr.append(val)
			atr = statistics.mean(atr)  
			oc = (df.iat[currentday - 1,0] + df.iat[currentday - 1,3])/2
			avg_slope = ((abs(ml) + abs(mh))/2)
			high = df.iat[currentday,1]
			low = df.iat[currentday,2]
			prev_close =df.iat[currentday-1,3]
			if (bh > bl and 
			z >3  and
			bh + mh*l > bl + ml*l 
			and oc < bh): 
				if prev_close < bh and prev_close > bl:
					val = avg_slope / atr
					if val < .1:
						val2 = tightening/atr
						if val2 > 0:
							log.log(df,currentday, tf, ticker, z, path, 'Flag')  

	  

