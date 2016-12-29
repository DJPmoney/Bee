#http://matplotlib.org/examples/pylab_examples/finance_demo.html
#http://stackoverflow.com/questions/13128647/matplotlib-finance-volume-overlay
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
from matplotlib.finance import volume_overlay3
from matplotlib.dates import num2date
from matplotlib.dates import date2num
import matplotlib.mlab as mlab
import datetime
import os
from os.path import isfile, join

SHOW_K_LEN = 40
def plot_kBar(stock_id):
    file_path = join('data', 'history_stock', stock_id+'.csv')
    pic_path = join('data','K_bar')

    if not os.path.exists(pic_path):
        os.mkdir(pic_path)

        #datafile = 'data/history_stock/2454.csv'
    r = mlab.csv2rec(file_path, delimiter=',')

    # the dates in my example file-set are very sparse (and annoying) change the dates to be sequential
    # for i in range(len(r)-1):
    #   r['date'][i+1] = r['date'][i] + datetime.timedelta(days=1)
    quotes = []
    candlesticks = zip(date2num(r['date']),r['opening_price'],r['highest_price'],r['lowest_price'],r['finial_price'],r['quantity'])
    for i in candlesticks :
        quotes.append(i)
    #print(len(candlesticks))
    quotes.reverse()
    #date1 = (2016, 11, 1)
    #date2 = (2016, 12, 31)
    #quotes2 = quotes_historical_yahoo_ohlc('2454.tw', date1, date2)
    #print(quotes[-SHOW_K_LEN:])
    #print(quotes2)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1,1,1)
    plt.title(stock_id)
    ax.set_ylabel('Quote ($)', size=12)
    candlestick_ohlc(ax, quotes[-SHOW_K_LEN:],width=0.6,colorup='r', colordown='g')

    #ax.xaxis_date()
    #plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')


    # shift y-limits of the candlestick plot so that there is space at the bottom for the volume bar chart
    pad = 0.25
    yl = ax.get_ylim()
    ax.set_ylim(yl[0]-(yl[1]-yl[0])*pad,yl[1])

    #  create the second axis for the volume bar-plot
    ax2 = ax.twinx()


    # set the position of ax2 so that it is short (y2=0.32) but otherwise the same size as ax
    ax2.set_position(matplotlib.transforms.Bbox([[0.125,0.1],[0.9,0.32]]))

    # get data from candlesticks for a bar plot
    dates = [x[0] for x in quotes[-SHOW_K_LEN:]]
    #print("a.dates = ",dates)
    dates = np.asarray(dates)
    #print("b.dates = ",dates)
    volume = [x[5] for x in quotes[-SHOW_K_LEN:]]
    #print("a.volume = ",volume)
    volume = np.asarray(volume)
    #print("b.volume = ",volume)

    open_price = [x[1] for x in quotes[-SHOW_K_LEN:]]
    open_price = np.asarray(open_price)
    close_price = [x[4] for x in quotes[-SHOW_K_LEN:]]
    close_price = np.asarray(close_price)
    # make bar plots and color differently depending on up/down for the day
    pos = open_price-close_price<0
    neg = open_price-close_price>0
    #print("pos = ",pos)
    #print("neg = ",neg)
    ax2.bar(dates[pos],volume[pos],color='red',width=1,align='center')
    ax2.bar(dates[neg],volume[neg],color='green',width=1,align='center')
    #ax2.bar(dates[-SHOW_K_LEN:],volume[-SHOW_K_LEN:],color='green',width=1,align='center')

    #scale the x-axis tight
    ax2.set_xlim(min(dates),max(dates))
    # the y-ticks for the bar were too dense, keep only every third one
    yticks = ax2.get_yticks()
    ax2.set_yticks(yticks[::3])

    ax2.yaxis.set_label_position("right")
    ax2.set_ylabel('Volume', size=12)

    # format the x-ticks with a human-readable date. 
    xt = ax.get_xticks()
    new_xticks = [datetime.date.isoformat(num2date(d)) for d in xt]
    ax.set_xticklabels(new_xticks,rotation=45, horizontalalignment='right')

    #plt.ion()

    #plt.show()
    plt.savefig(join(pic_path,stock_id+'.png'),dpi=150)
    plt.close(fig)


if __name__ == '__main__':
    stock_id = '2454'
    plot_kBar(stock_id)