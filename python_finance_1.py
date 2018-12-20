import datetime as dt
##matplotlib to graph things
import matplotlib.pyplot as plt
from matplotlib import style
## manipulate data
import pandas as pd
##
import pandas_datareader.data as web

style. use("ggplot")

##date 
start = dt.datetime(2017,1,1)
end = dt.datetime(2018,12,15)
##API
df = web.DataReader("TSLA", 'yahoo', start, end)
##rows of data
print(df.head(12))

##creating into a csv file
df.to_csv("TSLA.csv")
