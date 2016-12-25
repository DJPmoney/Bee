import StockCompanyConfig as SysConfig
import urllib
from datetime import datetime
from datetime import date
from datetime import timedelta
import pandas as pd
import os
from pathlib import Path
import csv


class CompanyRevenue:
    def __init__(self):
        self.revenue = []
        self.revenue_pandas= None
        
    def addItem_Revenue(self,  date,  item):
        if date in self.revenue or len(item) == 0:
            return
        data = {}
        data['date'] = date
        data['revenue'] = int(item[0].replace(",", ""))
        data['last_month_revenue_percent'] = float(item[1].replace(",", ""))
        data['last_year_revenue'] = int(item[2].replace(",", ""))
        data['last_year_revenue_percent'] = float(item[3].replace(",", ""))
        data['accumulat_revenue'] = int(item[4].replace(",", ""))
        data['last_year_accumulat_revenue'] = int(item[5].replace(",", ""))
        data['revenue_percent'] = float(item[6].replace(",", ""))
        self.revenue.append(data)
    
    def getItem_Revenue(self):
        return self.revenue
        
    def listRevenuePandas(self):   
        self.revenue_pandas = pd.DataFrame(self.revenue)

class CompanyInfo(CompanyRevenue):
    def __init__(self,  stock_id):
        CompanyRevenue.__init__(self)
        self.stock_id = stock_id
    
    def writeCsvUpdate(self):
        if len(self.revenue) == 0:
            return 
        file_name = SysConfig.STOCK_COMPANY_FOLDER + "update_info.txt"
        with open(file_name,  "a") as f:
            f.write(self.stock_id+":"+self.revenue[0]['date'] + "\n")
            
    def checkCsvUpdate(self):
        file_name = SysConfig.STOCK_COMPANY_FOLDER + "update_info.txt"
        try:
            with open(file_name,  "r") as f :
                for line in f:
                    line = line.rstrip('\n')
                    if line.find(self.stock_id ) >= 0:
                        s_date = datetime.strptime(line.split(":")[1], '%Y/%m')
                        c_date = datetime.strptime(date.today().strftime('%Y/%m/01'),  "%Y/%m/%d")
                        c_date = c_date - timedelta(days=20)
                        c_date = datetime.strptime(c_date.strftime('%Y/%m'),  "%Y/%m")
                        if (s_date > c_date):
                            return 1
                        return 0
        except:
            return 1
        return 2
        
    def writeRevenueCSV(self):
        if len(self.revenue) == 0:
            return 
        file_name = SysConfig.STOCK_COMPANY_FOLDER + self.stock_id + SysConfig.STOCK_COMPANY_REVENUE_FILE
        self.revenue_pandas.to_csv(file_name)
        self.writeCsvUpdate()
    
    def readRevenueCSV(self):
        file_name = SysConfig.STOCK_COMPANY_FOLDER + self.stock_id + SysConfig.STOCK_COMPANY_REVENUE_FILE
        if os.path.isfile(file_name) == False:
            return 0
        self.revenue_pandas = pd.DataFrame.from_csv(file_name)
        with open(file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
               self.revenue.append(row)
        return 1


def accessCompanyRevenue(stock_id,  info):
    web_path = SysConfig.HISTORY_STOCK_WEB%stock_id
    try: 
        response= urllib.request.urlopen(web_path)
        data = response.read().decode('utf-8')
    except:
        return 0
           
    c_date = datetime.strptime(date.today().strftime('%Y/%m/01'),  "%Y/%m/%d")
    flag_end = 0
    t_data = data
    while (flag_end<2):
        s_date = c_date.strftime('%Y/%m')
        s_prefix = '<td class="cr">'+s_date+'</td>'
        res_info = t_data.split(s_prefix)
        if len(res_info) == 2:
            s_i = res_info[1].find("</tr>")
            if s_i < 0:
                break
            s = res_info[1][:s_i]
            t_data = res_info[1][s_i:]
            res = s.split("</td>")
            item = []
            for i in range(len(res)):
                if res[i].find(">") <0:
                    continue
                item.append(res[i].split(">")[1])
            info.addItem_Revenue(s_date,  item)
        else:
            t_data = res_info[0]
            flag_end+=1
        c_date = c_date - timedelta(days=20)
        c_date= datetime.strptime(c_date.strftime('%Y/%m/01'),  "%Y/%m/%d")
        
    info.listRevenuePandas()
    return 1

def checkHistoryStock():
    if os.path.isdir(SysConfig.STOCK_COMPANY_FOLDER) == False:
       path = Path(SysConfig.STOCK_COMPANY_FOLDER) 
       path.mkdir(parents=True)

def accesssCompanyInfo(stock_id):
    info = CompanyInfo(stock_id)
    ret = info.checkCsvUpdate()
    if ret == 1:
         if accessCompanyRevenue(stock_id,  info) ==0:
             return None
         info.writeRevenueCSV()
    elif ret == 0:
        if info.readRevenueCSV()  == 0:
            return None
    else:
        return None
    return info
    


