import pandas as pd
from datetime import datetime
from datetime import timedelta
import StockConfig as System

def getDateIndex(stock_data,  date):
    s = datetime.strptime(date, "%Y/%m/%d")
    for i in range(len(stock_data)):
        d = datetime.strptime(stock_data[i]['date'], "%Y/%m/%d")
        if s>=d:
            return i
    return 0

def caculate_reqK_quantity_price(stock_id,  stock_data,  stock_pandas,  d_date):
    s_idx = getDateIndex(stock_data, d_date.strftime('%Y/%m/%d'))
    e_idx = getDateIndex(stock_data, (d_date-timedelta(days=System.RED_K_DURING)) .strftime('%Y/%m/%d'))
    
    #mean_quan = stock_pandas['quantity'][s_idx:e_idx].mean()
    #mean_price = stock_pandas['finial_price'][s_idx:e_idx].mean()
    success_times = 0
    for i in range(e_idx,  s_idx,  -1):
        d_idx = getDateIndex(stock_data, ( datetime.strptime(stock_data[i]['date'], "%Y/%m/%d")-timedelta(days=System.RED_K_DURING)) .strftime('%Y/%m/%d'))
        mean_quan = stock_pandas['quantity'][i:d_idx].mean()
        mean_price = stock_pandas['finial_price'][i:d_idx].mean()
        quan = float(stock_data[i]['quantity'])
        if quan == 0:
            continue
        diff_quan = mean_quan/quan
        if diff_quan>=System.RED_K_QUANTITY_PERCENT:
            continue
        price = float(stock_data[i]['finial_price'])
        diff_price = float(mean_price)/price
        #print(str(diff_price) + "," + str(mean_price)+"," + str(price))
        if diff_price>=System.RED_K_PRICE_PERCENT:
            continue
        #print("-->caculate_reqK_quantity_price --> 2")
        success_times+=1
        if success_times>=System.RED_K_MIN_TIMES:
            return 1
    return 0

def caculate_reqK_cross(stock_id,  stock_data,  stock_pandas,  d_date):
    idx = getDateIndex(stock_data, d_date.strftime('%Y/%m/%d'))
    finial_price = float(stock_data[idx]['finial_price'])
    avg_twenty = float(stock_data[idx]['avg_twenty'])
    diff = abs(finial_price - avg_twenty) / avg_twenty
    return (diff<=System.RED_K_CROSS_PERCENT)
    
def caculate_redK_mointor(stock_id,  stock_data,  stock_pandas,  date):
    d_date = datetime.strptime(date , "%Y/%m/%d")
    if caculate_reqK_quantity_price(stock_id,  stock_data,  stock_pandas,  d_date) == 0:
        return 0
    if caculate_reqK_cross(stock_id,  stock_data,  stock_pandas,  d_date) == 0:
        return 0
        
    return 1
