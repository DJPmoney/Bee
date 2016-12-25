import time
import requests
import csv
from datetime import datetime
from datetime import timedelta
from datetime import date
import pandas as pd
import os.path
from pathlib import Path
import StockConfig as System

def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y%m%d").strftime('%Y%m%d'):
            raise ValueError
        return True
    except ValueError:
        return False

def findDateIndex(m_data,  cdate):
    sdate = datetime.strptime(cdate, "%Y/m/d")
    for i in range(len(m_data)):
        pdate = datetime.strptime(m_data[i]['date'],  "%Y/m/d")
        if (pdate == sdate):
            return i
        elif i == 0 and sdate>pdate:
            return 0
    return -1

def caculateMarketTrend(m_data,  cdate):
    if System.ENABLE_MARKET_TREND == 0:
        return 1
    if m_data == None:
        return 1
        
    d_index = findDateIndex(m_data,  cdate)
    if (d_index < 0):
        return 1
    t = float(m_data[d_index+1]['finial_price']) - float(m_data[d_index]['finial_price'])
    return t <= System.MARKET_MIN_TREND_LIMIT
    

def accessMarketWithWeb():
    try:
        str_res = requests.get(System.HISTORY_MARKET_WEB,  timeout=60)
        if str_res.text == "":
             return None
        res = str_res.text.replace(" ",  ",").split(",")
        count_size=0
        for j in range(len(res)):
            if validate(res[j]) == False:
                break
            count_size+=1
        item = []
        for j in range(count_size-1,  0,  -1):
            data = {}
            cdate = res[j]
            cdate = datetime.strptime(cdate, "%Y%m%d").strftime('%Y/%m/%d')
            data['date'] = cdate
            data['opening_price'] = res[j+count_size]
            data['highest_price']= res[j+count_size*2]
            data['lowest_price']= res[j+count_size*3]
            data['finial_price']= res[j+count_size*4]
            data['quantity']= res[j+count_size*5]
            item.append(data)
            #print([cdate,  opening_price,  highest_price,  lowest_price,  finial_price,  quantity])
        return item
    except:
        return None

if __name__ == "__main__":
    accessMarketWithWeb()
