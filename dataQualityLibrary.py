import pandas as pd
import glob

import plotly.plotly as py
import plotly.offline as offline
import plotly.graph_objs as go
import numpy as np
import matplotlib.pyplot as plt
import logging

true=1
false=0

def sayHello():
	logging.info ('DataQuality Library Loaded')
	
def printSeperator():
	for a in range(0, 60):
			print ('-',end='')

def setLoggingLevel (loggingLevel):
	logger = logging.getLogger()
	logger.setLevel (loggingLevel)

# Shortcut to simple pie chart function. 
# We simply need to pass two arrays and a bool (Offline_mode currently not used)
def drawPie (labelArr, valueArr, title, offline_mode):
	# offline_mode is currently not used
	fig = {
	'data': [{'labels': labelArr,
			  'values': valueArr,
			  'type': 'pie',
			  #'pull': .2,
			  #'hole':.2,
			  #'colorscale':'blues',
			  'textposition':'outside'}],
	'layout': {'title': title},
	 
	 }
	
	if offline_mode:
		offline.iplot (fig)
	else:	
		py.plot (fig)
	

def pieChartUniqueValues (df, col_name, offline_mode):
	valueCounts = df[col_name].value_counts('dropna=false')
	drawPie (df[col_name].unique(), valueCounts.get_values(), col_name, offline_mode)
	
def findNumericAnomolies (df, col_name, showCompleteRow):
	
	showCompleteOutlierRow = 0

	logging.info ('*** Empty columns are ignored by this version of the function *** ')
	logging.info ('fn std ' + str(df[col_name].std()))
	outliers = df[col_name][np.abs(df[col_name]-df[col_name].mean()) > df[col_name].std() * 1]

	percentageOutliers = outliers.shape[0] / df.shape[0] * 100

	logging.info ('')
	logging.info ("standard deviation is calculated as " + str(df[col_name].std()))
	logging.info ('')
	logging.info ("Percentage outliers for " + col_name + " is " + str(percentageOutliers) + "%")
	logging.info ('')
	logging.info ('The following ' + str (outliers.shape[0]) + ' values have been deemed to be outliers based on 3 differences to std for column ' + col_name)
	logging.info ('')

	if showCompleteRow:
		print (df.ix[outliers.index.get_values()])
	else:
		print (outliers)

def findTextLengthOutliers (df, col_name, showCompleteRow):
	colValLength = []
	# Not the most efficient way of doing this, let me know if you have a better way
	#totalChars=0
	for fieldVal in df[col_name]:		 
		colValLength.append (len(str(fieldVal)))

	std = np.std (colValLength)
	mean = np.mean (colValLength)

	logging.info (" Mean is " + str(mean))
	logging.info (" Std is " + str (std))
	logging.info ('')

	# now we have the standard deviation lets find out what matches it
	#
	logging.info ('Looking for length based text outliers in row ' + col_name)
	
	for index, row in df.iterrows():
		if np.abs((len(str(row[col_name])) - mean)) > (std * 1):
			if showCompleteRow:
				print (row.get_values())
			else:
				print (str(row[col_name]))


#http://stackoverflow.com/questions/23199796/detect-and-exclude-outliers-in-pandas-dataframe
#df=pd.DataFrame({'Data':np.random.normal(size=200)})  #example dataset of normally distributed data. 
#df[np.abs(df.Data-df.Data.mean())<=(3*df.Data.std())] #keep only the ones that are within +3 to -3 standard deviations in the column 'Data'.
#df[~(np.abs(df.Data-df.Data.mean())>(3*df.Data.std()))] #or if you prefer the other way around