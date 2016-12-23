import time
import requests
import csv
#import config.StockConfig as System
import StockConfig as System
from datetime import datetime
from datetime import timedelta
from datetime import date
import pandas as pd
#import numpy as nm
import os.path
from pathlib import Path
import pyalgo_redK
import progressbar

stockdata_manager = {}

class StockData:
    def __init__(self,  stock_id):
        self.stock_id = stock_id
        self.stock_data=[]
        self.stock_pandas = None
        self.count = 0
        
    def addItem(self, date, opening_price , highest_price, lowest_price, finial_price, quantity,  
                         short_buy,  short_sell,  foreign_investment,  legal_person,  self_employed):
        item = {}
        item['date'] = date
        item['opening_price'] = float(opening_price)
        item['highest_price'] = float(highest_price)
        item['lowest_price'] = float(lowest_price)
        item['finial_price'] = float(finial_price)
        item['quantity'] = int(quantity)
        item['short_buy'] = int(short_buy)
        item['short_sell'] = int(short_sell)
        item['foreign_investment'] = int(foreign_investment)
        item['legal_person'] = int(legal_person)
        item['self_employed'] = int(self_employed)
        self.stock_data.append(item)
        self.count+=1

    def getItem(self,  index):
        if index >= self.count:
            return None
        return self.stock_data[index]
        
    def getStockData(self):
        return self.stock_data
        
    def getStockPandas(self):
        return self.stock_pandas
        
    def getItemCount(self):
        return self.count
	
    def calculateAvg(self):
        if self.count == 0:
            return
        amount_five = []
        amount_ten = []
        amount_twenty = []
        amount_sixty = []
        amount_hundred_twenty = []
        index_five = 5
        index_ten = 10
        index_twenty = 20
        index_sixty = 60
        index_hundred_twenty = 120
        for i  in range(index_five):
        	amount_five.append(float(self.stock_data[i]['finial_price']))
        for i  in range(index_ten):
        	amount_ten.append(float(self.stock_data[i]['finial_price']))
        for i  in range(index_twenty):
        	amount_twenty.append(float(self.stock_data[i]['finial_price']))
        for i  in range(index_sixty):
        	amount_sixty.append(float(self.stock_data[i]['finial_price']))
        for i  in range(index_hundred_twenty):
        	amount_hundred_twenty.append(float(self.stock_data[i]['finial_price']))
        self.stock_data[0]['avg_five'] = sum(amount_five)/len(amount_five)
        self.stock_data[0]['avg_ten'] = sum(amount_ten)/len(amount_ten)
        self.stock_data[0]['avg_twenty'] = sum(amount_twenty)/len(amount_twenty)
        self.stock_data[0]['avg_sixty'] = sum(amount_sixty)/len(amount_sixty)
        self.stock_data[0]['avg_hundred_twenty'] = sum(amount_hundred_twenty)/len(amount_hundred_twenty)
        
        for i in range(1,  self.count):
            if (index_five+i) <= self.count:
                amount_five[(index_five+i-1)%5] = float(self.stock_data[index_five+i-1]['finial_price'])
            if (index_ten+i) <= self.count:
                amount_ten[(index_ten+i-1)%10] = float(self.stock_data[index_ten+i-1]['finial_price'])
            if (index_twenty+i) <= self.count:
                amount_twenty[(index_twenty+i-1)%20] = float(self.stock_data[index_twenty+i-1]['finial_price'])
            if (index_sixty+i) <=  self.count:
                amount_sixty[(index_sixty+i-1)%60] = float(self.stock_data[index_sixty+i-1]['finial_price'])
            if (index_hundred_twenty+i) <= self.count:
                amount_hundred_twenty[(index_hundred_twenty+i-1)%120] = float(self.stock_data[index_hundred_twenty+i-1]['finial_price'])
            self.stock_data[i]['avg_five'] = sum(amount_five)/len(amount_five)
            self.stock_data[i]['avg_ten'] = sum(amount_ten)/len(amount_ten)
            self.stock_data[i]['avg_twenty'] = sum(amount_twenty)/len(amount_twenty)
            self.stock_data[i]['avg_sixty'] = sum(amount_sixty)/len(amount_sixty)
            self.stock_data[i]['avg_hundred_twenty'] = sum(amount_hundred_twenty)/len(amount_hundred_twenty)
        
    def writeCSV(self):
        if self.count == 0:
            return 
        file_name = System.STOCK_DATA_FOLDER + self.stock_id + '.csv'
        self.stock_pandas.to_csv(file_name)
        
    def readCSV(self):
        file_name = System.STOCK_DATA_FOLDER + self.stock_id + '.csv'
        if os.path.isfile(file_name) == False:
            return 0
        self.stock_pandas = pd.DataFrame.from_csv(file_name)
        with open(file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
               self.stock_data.append(row)
        self.count = len(self.stock_data)
        return 1
        
    def listPandas(self):   
        self.stock_pandas = pd.DataFrame(self.stock_data)

    def calculateNearAvg(self,  start,  end):
        during= end - start
        #print ("======calculateNearAvg: "+ self.stock_id)
        #print (str(start) + ":" + str(end))
        diff = ((self.stock_pandas['avg_five'][start:end]-self.stock_pandas['avg_sixty'][start:end])/self.stock_pandas['avg_five'][start:end]).abs()
        #print (diff)
        count_diff=(diff<=System.NEAR_AVG_DIFF_PERCENT).sum()
        #print (count_diff)
        if (float(count_diff)/(during)) >= System.NEAR_AVG_GRAVITY_PERCENT:
            #print ("======calculateNearAvg: True :" + str(float(count_diff)/(during)))
            return 1
        #print ("======calculateNearAvg: False :" + str(float(count_diff)/(during)))
        return 0
        
    def calculateQuantity(self,  start,  end):
        quan = []
        for i in range(start,  end):
            data = {}
            data['quan_date'] = self.stock_data[i]['date']
            data['quan_value'] = int(self.stock_data[i]['quantity'])
            data['quan_previous'] = int(self.stock_data[i+1]['quantity'])
            data['quan_diff'] = data['quan_value'] - data['quan_previous'] 
            data['quan_diff_percent']  = 0
            if (data['quan_value'] > 0):
                data['quan_diff_percent'] = float(data['quan_previous']) / data['quan_value']
            quan.append(data)
        return quan
        
    def printMsg(self):
        print("===Stock ID:" + self.stock_id)
        for i in range(self.count):
            print(self.stock_data[i])

def getCompanyList(): 
    #print(System.COMPANY_LIST_FILE)
    csvfile = open(System.COMPANY_LIST_FILE, 'r')
    reader = csv.DictReader( csvfile)
    return [ row for row in reader ]

def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y/%m/%d").strftime('%Y/%m/%d'):
            raise ValueError
        return True
    except ValueError:
        return False
 
def writeCsvUpdate():
    file_name = System.STOCK_DATA_FOLDER + "update_info.txt"
    with open(file_name,  "w") as f :
        f.write(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
 
def checkCsvUpdate():
    file_name = System.STOCK_DATA_FOLDER + "update_info.txt"
    update = ""
    try:
        with open(file_name,  "r") as f :
            update = f.readline()
    except:
        return 1
    
    u_date = datetime.strptime(update, "%Y/%m/%d %H:%M:%S")
    u_date+=timedelta(hours=System.HOURS_CSV_UPDATE)
    n_date = datetime.strptime(datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  '%Y/%m/%d %H:%M:%S')
    return (n_date>=u_date)
         
def getDateIndex(stock_id,  date):
    s = datetime.strptime(date, "%Y/%m/%d")
    stock = stockdata_manager[stock_id]
    for i in range(stock.getItemCount()):
        d = datetime.strptime(stock.getItem(i)['date'], "%Y/%m/%d")
        if s>=d:
            return i
    return 0
 
def accessHistoryStockWithWeb(stock_id):
    try:
         history_data_web = System.HISTORY_STOCK_WEB%stock_id
         #print(history_data_web)
         stock_data = StockData(stock_id)
         str_res = requests.get(history_data_web,  timeout=60)
         if str_res.text == "":
             return None
         res = str_res.text.replace(" ",  ",").split(",")
         #print (res.text)
         count_size=0
         for j in range(len(res)):
            if validate(res[j]) == False:
                break
            count_size+=1
         for j in range(count_size-1,  0,  -1):
            date = res[j]
            opening_price = res[j+count_size]
            highest_price= res[j+count_size*2]
            lowest_price= res[j+count_size*3]
            finial_price= res[j+count_size*4]
            quantity= res[j+count_size*5]
            short_buy= res[j+count_size*6]
            short_sell= res[j+count_size*7]
            foreign_investment= res[j+count_size*8]
            legal_person= res[j+count_size*9]
            self_employed= res[j+count_size*10]
            stock_data.addItem(date,opening_price, highest_price,lowest_price, finial_price, quantity, 
                                         short_buy,  short_sell,  foreign_investment,  legal_person,  self_employed)
         stock_data.calculateAvg()
         stock_data.listPandas()
         stock_data.writeCSV()
    except:
        return None
    return stock_data

def accessHistoryStockWithCsv(stock_id):
    stock_data = StockData(stock_id)
    if stock_data.readCSV() == 0:
        return None
    return stock_data

def accessAllHistoryStock():
    company = getCompanyList()
    flag_update = checkCsvUpdate()
    bar = progressbar.ProgressBar()
    for i in bar(range(len(company))):
        #print (str(i) + "/" + str(len(company)))
        stock_id = company[i]['Number']
        if (flag_update == 1):
            stock = accessHistoryStockWithWeb(stock_id)
        else:
            stock = accessHistoryStockWithCsv(stock_id)
        if stock != None:
            stockdata_manager[stock_id] = stock
        #if (stockdata_manager[stock_id] != None):
        #   stockdata_manager[stock_id].printMsg()
        #if i > 5:
        #break
    if (flag_update == 1):
        writeCsvUpdate()
    return stockdata_manager

def caculateStockNearAvg(stock_id,  date,  during):
    if validate(date) == False or during== 0:
        return 0
    if stock_id  not in stockdata_manager:
        return 0
    if stockdata_manager[stock_id].getItemCount() <= 0:
        return 0
    #print(stock_id)
    #print(stockdata_manager[stock_id].getItem(0))
    start = getDateIndex(stock_id,  date)
    end = start + during
    return stockdata_manager[stock_id].calculateNearAvg(start,  end)

def checkQuantity(quan):
    if (quan == None):
        return 0
    sum_quan = 0
    avg_quan = 0
    for i in range(len(quan)):
        sum_quan+=quan[i]['quan_value']
    if len(quan) > 0:
        avg_quan = float(sum_quan)/len(quan)
    if (avg_quan <= System.QUANTITY_TRANS_AVERAGE):
        return 0
        
    return 1

def calculateStockQuantity(stock_id,  date,  during):
    if validate(date) == False or during== 0:
        return 0
    if stock_id  not in stockdata_manager:
        return 0
    if stockdata_manager[stock_id].getItemCount() <= 0:
        return 0
    start = getDateIndex(stock_id,  date)
    end = start + during
    return checkQuantity(stockdata_manager[stock_id].calculateQuantity(start,  end))
    
def caculateStockChoice(stock_id,  date):
    if validate(date) == False:
        return 0
    if stock_id  not in stockdata_manager:
        return 0
    #if (caculateStockNearAvg(stock_id, date,  System.DURING_NEAR_AVG) == 0):
    #    return 0
    #if (calculateStockQuantity(stock_id, date,  System.DURING_QUANTITY) == 0):
     #   return 0
    if pyalgo_redK.caculate_redK_mointor(stock_id,  stockdata_manager[stock_id].getStockData(),  
                   stockdata_manager[stock_id].getStockPandas(),  date) ==0:
        return 0
    return 1

def checkHistoryStock():
    if os.path.isdir(System.STOCK_DATA_FOLDER) == False:
       path = Path(System.System.STOCK_DATA_FOLDER) 
       path.mkdir(parents=True)

def initBroseWeb():
    checkHistoryStock()
    stockdata_manager = accessAllHistoryStock()
    return stockdata_manager
    
if __name__ == "__main__":
    begin_time = time.time()
    
    initBroseWeb()
    choice_stock = {}
    cur_date = date.today().strftime('%Y/%m/%d')
    i = 0
    bar = progressbar.ProgressBar()
    for  stock_id in bar(stockdata_manager):
        #print (str(i) + "##" + str(len(stockdata_manager)))
        i+=1
        ret = caculateStockChoice(stock_id, cur_date)
        if ret == 1:
            choice_stock[stock_id] = stockdata_manager[stock_id]
    
    finished_time = time.time() 
    print("----> total spend:" + str(finished_time-begin_time))
    print ("Choice Size:" + str(len(choice_stock)))
    print (choice_stock.keys())

#if __name__ == "__main__":
 #   initBroseWeb()
