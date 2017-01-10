import StockCompanyConfig as SysConfig
import urllib
from datetime import datetime
from datetime import date
from datetime import timedelta
import pandas as pd
import os
from pathlib import Path
import csv
import  pyscore
import traceback


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
        s = ""
        flag_s = 0
        with open(file_name,  "r") as f :
            for line in f:
                t =  line.rstrip('\n')
                if t.find(self.stock_id ) >= 0:
                    if flag_s  == 0:
                        flag_s = 1
                        s+=(self.stock_id+":"+self.revenue[0]['date'] + "\n")
                else:
                    s+=line
        if flag_s == 0:
            s+=(self.stock_id+":"+self.revenue[0]['date'] + "\n")
        with open(file_name,  "w") as f:
            f.write(s)
            
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
                        if (s_date >= c_date):
                            return 0
                        return 1
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


def findDateIndex(revenue,  cdate):
    if revenue == None or len(revenue) == 0:
        return -1
    pdate = datetime.strptime(cdate,  "%Y/%m/%d")
    s = str(pdate.year) + "/" + str(pdate.month)
    kdate = datetime.strptime(s,  "%Y/%m")
    for i in range(len(revenue)):
        sdate = datetime.strptime(revenue[i]['date'],  "%Y/%m")
        if kdate == sdate:
            return i
        elif i == 0 and kdate>sdate:
            return 0
    return -1

def caculateLastMonthGrowth(stock_id,  company_info,  date_idx,  score):
    d = float(company_info.getItem_Revenue()[date_idx]['last_month_revenue_percent'])
    score.append(['caculateLastMonthGrowth',  
                          d,  SysConfig.REVENUE_LAST_MONTH__GROTH_PERCENT,  None])
    ret = (d >= SysConfig.REVENUE_LAST_MONTH__GROTH_PERCENT)
    if SysConfig.REVENUE_LAST_MONTH_GROWTH_ENABLE ==0:
        ret = 1
    return ret
    
def caculateContinousMonthGrowth(stock_id,  company_info,  date_idx,  score):
    
    revenue = company_info.getItem_Revenue()
    s_idx = date_idx
    e_idx = s_idx + SysConfig.REVENUE_CONTINOUS_MONTH_GROWTH
    error_count  = 0
    for i in range(s_idx,  e_idx):
        if float(revenue[i]['last_year_revenue_percent']) < SysConfig.REVENUE_CONTINOUS_MONTH_GROWTH_PERCENT:
            error_count+=1
            score.append(['caculateContinousMonthGrowth#last_year_revenue_percent',
                                  float(revenue[i]['last_year_revenue_percent']),  
                                  SysConfig.REVENUE_CONTINOUS_MONTH_GROWTH_PERCENT,  None])
    
    score.append(['caculateContinousMonthGrowth#error_count',
                          error_count, None,  None])
    if SysConfig.REVENUE_CONTINOUS_MONTH_GROWTH <=0:
        return 1
    return (error_count == 0)
    
def caculateContinousGrowth(stock_id,  company_info,  date_idx,  score):
    revenue = company_info.getItem_Revenue()
    s_idx = date_idx
    e_idx = s_idx + SysConfig.REVENUE_CONTINOUS_RECENT_GROTH
    error_count = 0
    for i in range(s_idx,  e_idx):
        if float(revenue[i]['last_month_revenue_percent']) < SysConfig.REVENUE_CONTINOUS_RECENT_GROTH_PERCENT:
            error_count+=1
            score.append(['caculateContinousGrowth#last_month_revenue_percent',
                                  float(revenue[i]['last_month_revenue_percent']),  
                                  SysConfig.REVENUE_CONTINOUS_RECENT_GROTH_PERCENT,  None])
                                  
    score.append(['caculateContinousGrowth#error_count',
                          error_count, None,  None])
    if SysConfig.REVENUE_CONTINOUS_RECENT_GROTH <=0:
        return 1
    return (error_count == 0)

def caculateCompanyRevenue(companyinfo_manager,  stock_id,  cdate):
    if stock_id not in companyinfo_manager:
        return 1
    
    company_info = companyinfo_manager[stock_id]
    if len(company_info.getItem_Revenue()) == 0:
        return 1
    date_idx = findDateIndex(company_info.getItem_Revenue(),  cdate)
    if  date_idx< 0:
        return 1
        
    score = []
    flag_m = 1
    flag_c_m = 1
    flag_c = 1
    if caculateLastMonthGrowth(stock_id,  company_info,  date_idx,  score) == 0:
        flag_m = 0
    if caculateContinousMonthGrowth(stock_id,  company_info,  date_idx,  score) == 0:
        flag_c_m = 0
    if caculateContinousGrowth(stock_id,  company_info,  date_idx,  score) == 0:
        flag_c = 0
        
    pyscore.appendFunctionScroe(traceback.extract_stack(None, 2)[0][2], stock_id,  score)
    if flag_m == 0 or flag_c_m == 0  or flag_c == 0:
        return 0
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
    
if __name__ == "__main__":
    stock_id = "6283"
    company_info = accesssCompanyInfo("6283")
    cdate = date.today().strftime('%Y/%m/%d')
    
    date_idx = findDateIndex(company_info.getItem_Revenue(),  cdate)
    score = []
    caculateLastMonthGrowth(stock_id,  company_info,  date_idx,  score)
    caculateContinousMonthGrowth(stock_id,  company_info,  date_idx,  score) 
    caculateContinousGrowth(stock_id,  company_info,  date_idx,  score) 


