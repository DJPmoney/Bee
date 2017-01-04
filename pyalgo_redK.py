import pandas as pd
from datetime import datetime
from datetime import timedelta
import StockConfig as System
import  pyscore
import traceback

def getDateIndex(stock_data,  date):
    s = datetime.strptime(date, "%Y/%m/%d")
    if len(stock_data) == 0:
        return -1
    for i in range(len(stock_data)):
        d = datetime.strptime(stock_data[i]['date'], "%Y/%m/%d")
        if s>=d:
            return i
    return 0

def caculate_reqK_quantity_price(stock_id,  stock_data,  stock_pandas,  d_date,  score):
    s_idx = getDateIndex(stock_data, d_date.strftime('%Y/%m/%d'))
    e_idx = getDateIndex(stock_data, (d_date-timedelta(days=System.RED_K_DURING)) .strftime('%Y/%m/%d'))
    
    #mean_quan = stock_pandas['quantity'][s_idx:e_idx].mean()
    #mean_price = stock_pandas['finial_price'][s_idx:e_idx].mean()
    if s_idx == -1 or e_idx == -1:
        return 0
    success_times = 0
    count_times = 0
    for i in range(e_idx,  s_idx,  -1):
        d_idx = getDateIndex(stock_data, ( datetime.strptime(stock_data[i]['date'], "%Y/%m/%d")-timedelta(days=System.RED_K_DURING)) .strftime('%Y/%m/%d'))
        if d_idx == -1:
            continue
        
        count_times+=1
        flag_quan = 1
        flag_price = 1
        mean_quan = stock_pandas['quantity'][i:d_idx].mean()
        
        if mean_quan < System.RED_K_MIN_AVG_QUANTITY:
            flag_quan = 0
        quan = float(stock_data[i]['quantity'])
        if quan == 0:
             flag_quan = 0
        diff_quan = mean_quan/quan
        if diff_quan>=System.RED_K_QUANTITY_PERCENT:
            flag_quan = 0
            
        score.append(['caculate_reqK_quantity_price#mean_quan', 
                            d_idx,  s_idx,  e_idx,  mean_quan, diff_quan, 
                            System.RED_K_MIN_AVG_QUANTITY,  System.RED_K_QUANTITY_PERCENT
                            ])
            
        mean_price = stock_pandas['finial_price'][i:d_idx].mean()
        price = float(stock_data[i]['finial_price'])
        diff_price = float(mean_price)/price
        if diff_price>=System.RED_K_PRICE_PERCENT:
            flag_price = 0
        score.append(['caculate_reqK_quantity_price#mean_price', 
                             diff_price,  System.RED_K_PRICE_PERCENT
                            ])
        if flag_price == 1 and flag_quan == 1:
            success_times+=1
    score.append(['caculate_reqK_quantity_price#success_times', 
                             success_times,  count_times
                            ])
    if success_times>=System.RED_K_MIN_TIMES:
        return 1
    return 0

def caculate_reqK_cross(stock_id,  stock_data,  stock_pandas,  d_date,  score):
    idx = getDateIndex(stock_data, d_date.strftime('%Y/%m/%d'))
    if idx == -1:
        return 0
    finial_price = float(stock_data[idx]['finial_price'])
    avg_twenty = float(stock_data[idx]['avg_twenty'])
    diff = abs(finial_price - avg_twenty) / avg_twenty
    score.append(['caculate_reqK_cross', 
                          diff, None, System.RED_K_CROSS_PERCENT])
    return (diff<=System.RED_K_CROSS_PERCENT)
    
def caculate_redK_mointor(stock_id,  stock_data,  stock_pandas,  date):
    d_date = datetime.strptime(date , "%Y/%m/%d")
    score = []
    flag_q_p = 1
    flag_cross = 1
    if caculate_reqK_quantity_price(stock_id,  stock_data,  stock_pandas,  d_date,  score) == 0:
        flag_q_p = 0
    if caculate_reqK_cross(stock_id,  stock_data,  stock_pandas,  d_date,  score) == 0:
        flag_cross = 0
    pyscore.appendFunctionScroe(traceback.extract_stack(None, 2)[0][2], stock_id,  score)
    if flag_q_p == 0 or flag_cross == 0:
        return 0
    
    return 1
