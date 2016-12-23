
#import config.SimNearAvgConfig as SIM_System
import SimNearAvgConfig as SIM_System
import pybrowseweb as stock_web
import datetime
import random
import time
import pandas as pd

def getPrice(highest_price, lowest_price):
    h = float(highest_price,)
    l = float(lowest_price)
    random.seed(SIM_System.SIM_RAND_SEED)
    return random.uniform(l, h)
    #print (str(h) + "--" + str(l))
    #return (h+l)/2
    
def writeSIMCsv(sim_info_summary):
    sim_stock_pandas = pd.DataFrame(sim_info_summary)
    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S_SimulateResult') + '.csv'
    sim_stock_pandas.to_csv(file_name)

if __name__ == "__main__":
    print("====Start SIM Near Avg ============") 
    begin_time = time.time()
    
    stock_web.initBroseWeb()
    
    sim_c = 0
    sim_info_manage = []
    for stock_id in stock_web.stockdata_manager:
        sim_c+=1
        print("--> " +str(sim_c) + "/" + str(len(stock_web.stockdata_manager.keys())))
        sim_info = {}
        sim_info['stock_id'] = stock_id
        #sim_info['choices'] = 0 
        sim_info['record_choices'] = 0 
        sim_info['record_info'] = []
        
        date_start = datetime.date.today()
        date_end = date_start - datetime.timedelta(days=SIM_System.SIM_DAYS)
        d_count = d_index = record_index = 0
        print (str(date_start) + "~" + str(date_end))
        while (date_start >= date_end ):
            flag_times = 1
            if sim_info['record_choices'] >= SIM_System.SIM_MAX_TRANS_TIMES:
                if SIM_System.SIM_PROGRESS_TIMES_ENABLE == 1:
                    break
                else:
                    flag_times = 0
            d_index = stock_web.getDateIndex(stock_id, date_end.strftime('%Y/%m/%d'))
            if d_index != record_index and flag_times == 1:
                ret = stock_web.caculateStockChoice(stock_id,  date_end.strftime('%Y/%m/%d'))
                if (ret == 1):
                    sim_date = date_end
                    sim_count = sim_index = sim_record_index = 0
                    
                    sim_info['record_choices']+=1
                    sim_info['sim_buy_date']=sim_date
                    sim_info['sim_buy_index'] = d_index
                    s_data = stock_web.stockdata_manager[stock_id].getItem(d_index)
                    sim_info['sim_cost_price'] = getPrice(s_data['highest_price'], s_data['lowest_price'])

                    sim_date+=datetime.timedelta(days=1)
                    while (date_start >= sim_date ):
                        sim_index = stock_web.getDateIndex(stock_id, sim_date.strftime('%Y/%m/%d'))
                        if (sim_record_index != sim_index):
                            sim_record_index = sim_index
                            
                            sim_data = stock_web.stockdata_manager[stock_id].getItem(sim_index)
                            sell_price = getPrice(sim_data['highest_price'], sim_data['lowest_price'])
                            price_diff = sell_price - sim_info['sim_cost_price']
                            price_percent = float(abs(price_diff))/sim_info['sim_cost_price']
                            if (price_percent>=SIM_System.SIM_TRANS_PERCENT) or (sim_count > SIM_System.SIM_TRANS_DAYS_LIMIT):
                                sim_info['sim_sell_price'] = sell_price
                                sim_info['sim_sell_date'] = sim_date
                                sim_info['sim_price_diff'] = price_diff
                                sim_info['sim_price_percent'] = price_percent
                                sim_info['sim_sell_index'] = sim_index
                                sim_info_manage.append(sim_info)
                                break

                        sim_count+=1
                        sim_date+=datetime.timedelta(days=1)

                record_index = d_index
                
            d_count+=1
            date_end+=datetime.timedelta(days=1)
    
    sim_info_summary = {}
    sim_info_summary['total_trans'] = 0
    sim_info_summary['total_success_trans'] = 0
    sim_info_summary['total_fail_trans'] = 0
    sim_info_summary['total_success_money'] = 0.0
    sim_info_summary['total_fail_money'] = 0.0
    sim_info_summary['total_trans_buy_money'] = 0.0
    sim_info_summary['total_trans_sell_money'] = 0.0
    
    writeSIMCsv(sim_info_manage)
    
    for i in range(len(sim_info_manage)):
    	sim_info_summary['total_trans']+=1
    	if sim_info_manage[i]['sim_price_diff']>=0:
    		sim_info_summary['total_success_trans']+=1
    		sim_info_summary['total_success_money']+=float(sim_info_manage[i]['sim_price_diff'])
    	else:
    		sim_info_summary['total_fail_trans']+=1
    		sim_info_summary['total_fail_money']+=float(sim_info_manage[i]['sim_price_diff'])
    	sim_info_summary['total_trans_buy_money']+=float(sim_info_manage[i]['sim_cost_price'])
    	sim_info_summary['total_trans_sell_money']+=float(sim_info_manage[i]['sim_sell_price'])
    
    finished_time = time.time()
    print("----> total spend:" + str(finished_time-begin_time))
    print(sim_info_manage)
    print("=======================================================")
    print("=======================================================")
    print("===================    Summary       ==================")
    print("=======================================================")
    print("=======================================================")
    print(sim_info_summary)
