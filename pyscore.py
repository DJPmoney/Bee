import pandas as pd
import ScoreConfig as System
import traceback

g_scoretab = System.ScoreTab


def appendFunctionScroe(func_name,  stock_id,  score):
    if func_name not in g_scoretab:
        return 0
    if score == None or len(score) == 0:
        return 0
    if stock_id not in g_scoretab[func_name]['data']:
        g_scoretab[func_name]['data'][stock_id] = {}
        
    g_scoretab[func_name]['data'][stock_id]['original_scrore'] = score
    return 1

def scoreStockNearAvg(key):
    print(traceback.extract_stack(None, 2)[0][2])
def scoreStockQuantity(key):
    print(traceback.extract_stack(None, 2)[0][2])
def score_redK_mointor(key):
    print(traceback.extract_stack(None, 2)[0][2])
def scoreCompanyRevenue(key):
    print(traceback.extract_stack(None, 2)[0][2])
def scoreMarkPriceTrend(key):
    print(traceback.extract_stack(None, 2)[0][2])

    
def caculateScore():
    for key in g_scoretab:
        g_scoretab[key]['callbackFunc'](key)
    
def initScore():
    global g_scoretab
    
    for key in g_scoretab:
        if 'data' not in g_scoretab[key]:
            g_scoretab[key]['data'] = {}
    g_scoretab['caculateStockNearAvg']['callbackFunc'] = scoreStockNearAvg
    g_scoretab['calculateStockQuantity']['callbackFunc'] = scoreStockQuantity
    g_scoretab['caculate_redK_mointor']['callbackFunc'] = score_redK_mointor
    g_scoretab['caculateCompanyRevenue']['callbackFunc'] = scoreCompanyRevenue
    g_scoretab['calculateMarkPriceTrend']['callbackFunc'] = scoreMarkPriceTrend
            
            
def test1():
    print("test1")
def test2():
    print("test2")
def test3():
    print("test3")
            
if __name__ == "__main__":
    a = {
    't1':test1,  
    't2':test2, 
    't3':test3, 
    }
    
    a['t1']()
