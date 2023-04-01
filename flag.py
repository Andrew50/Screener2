

from Data7 import Data as data

import pandas as pd
import statistics
import mplfinance as mpf
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

date = '2023-03-26'#'2020-08-12'#'2020-11-18'
ticker = 'meli'#'tsla'

lmax = 100
lmin = 5
mal = 3


coef = 0



df = data.get(ticker)
index = data.findex(df,date)

df = df[index - 300:index]



#find swings

current = len(df) - 1

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
		swings = np.append(swings,[[prevma,i,0]],axis = 0)
		if end:
			break
	elif slope == -1 and ma > prevma:
		
		slope = 1
		swings = np.append(swings,[[prevma,i,1]],axis = 0)
		if end:
			break
	elif slope == 0:
		if ma > mal:
			slope = 1
		else:
			slope = -1

	if i >= lmax:
		end = True
	ma = prevma
	i += 1



#find l
lval = 0
l = 0


for i in range(len(swings)-1):


	val = abs(swings[i,0]/swings[i+1,0] - 1)/pow(swings[i,1],coef)
	if val > lval:
		lval = val
		l = swings[i,1]


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

	for i in range(n):
		high = swings[i,2]
		
		if high == 1:
			
			xh = np.append(xh,[[swings[i,1]]],axis = 0)
			yh = np.append(yh,swings[i,0])
		else:
			
			xl = np.append(xl,[[swings[i,1]]],axis = 0)
			yl = np.append(yl,swings[i,0])



	god = []
	for i in range(len(yh)):
		god.append(yh[i])

	stdev = statistics.stdev(god)
	mean = statistics.mean(god)

	for i in range(len(yh)):

		

	

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

	points =[(x1,y1),(x2,y2)]

	x = np.empty(0)
	y = np.empty(0)







	for i in range(len(xh)):
		val = yh[i] 
		date = -xh[i,0]
		x = np.append(x,date)
		y = np.append(y,val)

	print(points)

	rx = np.empty(0)
	ry = np.empty(0)

	for i in range(len(xh)):
		 
		date = xh[i,0]
		val = yh[i] - (mh*date + bh)
		rx = np.append(rx,date)
		ry = np.append(ry,val)


	line = df.index[-l]
	mc = mpf.make_marketcolors(up='g',down='r')
	s  = mpf.make_mpf_style(marketcolors=mc)
	mpf.plot(df, type='candle', style=s, alines = points)#, alpha = .25))#vlines=dict(vlines=[line],


	plt.scatter(x,y)
	plt.show()

	plt.scatter(rx,ry)
	plt.show()


	


	
	



