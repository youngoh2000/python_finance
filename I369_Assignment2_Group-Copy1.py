
# coding: utf-8

# # Bitcoin Price Analysis - Group 9
# Group Memebers: Nick Forche, Young Oh, Congci Hao
# 
# ### Objectives:
# - Extract BTC prices from Yahoo Finance and key words frequency from Google Trends
# - Manipulate, transform, and merge datasets to prepare variables
# - Run simple regression against the key words 'Bitcoin'
# - Analyze regression statistics and conlcude the significance

# In[84]:

import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
from datetime import datetime

from scipy import stats
import statsmodels.api as sm 

import matplotlib.pyplot as plt


# In[85]:

#Setting the end date to today
end = datetime.today()

#Start date set to one year back
start = datetime(end.year-5,end.month,end.day)

#using yahoo finance to grab cryptocurrency data
BTC = pdr.get_data_yahoo('BTC-USD',start = "2014-1-1",end = datetime.today(),interval='m')
ETH = pdr.get_data_yahoo('ETH-USD',start = "2014-1-1",end = datetime.today(),interval='m')
# ETH = pdr.DataReader('ETH-USD','yahoo',start,end)
# LTC = pdr.DataReader('LTC-USD','yahoo',start,end)


# In[86]:

#Look at top 5 rows of Bitcoin data
BTC.tail(5)
ETH.tail(5)


# In[87]:

#Set the figure sizes
plt.rcParams['figure.figsize'] = (10,8)


# In[88]:

#Plot the Bitcoin price movements over the past 5 years
BTC['Adj Close'].plot(legend = True);
#ploting Eth
ETH['Adj Close'].plot(legend = True);


# In[93]:

#Plot 10,20,and 50 days moving average with daily Bitcoin prices

ma_days = [10,20,50]

for ma in ma_days:
     column_name = "MA %s days"%(str(ma))        
     BTC[column_name] = BTC['Adj Close'].rolling(window=ma,center=False).mean()

for co in ma_days:
    column_name = "MA %s days"%(str(co))
    ETH[column_name] = ETH['Adj Close'].rolling(window=ma,center=False).mean()
    
BTC[['Adj Close','MA 10 days','MA 20 days','MA 50 days']].plot(legend=True);
ETH[['Adj Close','MA 10 days','MA 20 days','MA 50 days']].plot(legend=True);


# ### Don't Run This Section - Use Pytrend package to extract daily google searches data (Didn't work for montly frequencies)

# In[94]:

from pytrends.request import TrendReq
pytrends = TrendReq(hl='en-US', tz=360)

kw_list = ["Bitcoin"]
kw_list2 = ["Ethereum"]


# In[95]:

search_df = pytrends.get_historical_interest(kw_list, year_start=2019, month_start=1, day_start=1, year_end=2019, month_end=3, day_end=1,cat=0, geo='', gprop='', sleep=0.5)
#search_df = pytrends.interest_over_time()
search_df.head(5)

search_df2 = pytrends.get_historical_interest(kw_list2, year_start=2019, month_start=1, day_start=1, year_end=2019, month_end=3, day_end=1,cat=0, geo='', gprop='', sleep=0.5)
search_df2.head(5)


# ### Download Bitcoin Google Seraches from Google Trends 

# In[98]:

BTC_searches= pd.read_csv('multiTimeline.csv',skiprows=1)
#ETH_searches= pd.read_csv('C:/Users/47523/Desktop/2019 Spring/INFO_I369 Performance Analytics/Assignment2_Group/multiTimeline eth.csv',skiprows=1)


# In[100]:

BTC_searches.columns = ['Date','Bitcoin']
#ETH_searches.columns = ['Date','Bitcoin']


# ### Combine Two Pandas Dataframes

# In[101]:

BTC_prices = BTC['Adj Close'].iloc[:-1]
BTC_prices

ETH_prices = ETH['Adj Close'].iloc[:-1]
ETH_prices


# In[103]:

df = pd.concat([BTC_prices.reset_index(drop=True),BTC_searches.reset_index(drop=True)], axis=1)
#df2 = pd.concat([ETH_prices.reset_index(drop=True),ETH_searches.reset_index(drop=True)], axis=1)


# In[104]:

#df = df.set_index('Date')
df.head(3)

#df2.head(3)


# ### Simple Linear Regression Statistics

# In[111]:

#Draw the scatter plot with Bitcoin searches as an independent variable, 
#and Bitcoin average monthly prices as a dependent variable
X = df['Bitcoin']
Y = df['Adj Close']
plt.scatter(X,Y)
plt.axis([0,120,0,15000])

#Draw the trend line
z = np.polyfit(X,Y,1)
p = np.poly1d(z)
plt.plot(X,p(X),"r")
plt.show()


# In[ ]:

#Draw the scatter plot with Ethereum searches as an independent variable, 
#and Ethereum average monthly prices as a dependent variable
X = df['Ethereum']
Y = df['Adj Close']
plt.scatter(X,Y)
plt.axis([0,120,0,15000])

#Draw the trend line
z = np.polyfit(X,Y,1)
p = np.poly1d(z)
plt.plot(X,p(X),"r")
plt.show()


# In[107]:

#Apply statsmodel to run regression and conclude detailed stats
X1 = sm.add_constant(X)
reg = sm.OLS(Y, X1).fit()


# In[ ]:

reg.summary()


# In[ ]:

#Or use scipy to run linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)
stats.linregress(X,Y)


# ### Insights:
# 1. This univariate regression explains that 64.8% of the Bitcoin prices is explained by 'Bitcoin' frequencies in Google searches
# 2. p-values for the slope and intercept are both smaller than 0.01. The model has decent prediction power for future Bitcoin prices.
