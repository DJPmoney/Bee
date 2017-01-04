import pandas as pd
import ScoreConfig as System
import traceback

g_scoretab = System.ScoreTab
g_caculate_score_tab = {}

def appendFunctionScroe(func_name,  stock_id,  score):
    if func_name not in g_scoretab:
        return 0
    if score == None or len(score) == 0:
        return 0
    if stock_id not in g_scoretab[func_name]['data']:
        g_scoretab[func_name]['data'][stock_id] = {}
        
    g_scoretab[func_name]['data'][stock_id]['original_scrore'] = score
    return 1
    
def addStockScore(params,  param_name, item,  s_score,   k):
    if item not in s_score:
        s_score[item] = [param_name,  0,  0,  0]
    p = params[param_name][item]
    s_score[item][1]+= float(k)*p
    s_score[item][2]+= p
    s_score[item][3] = float(s_score[item][1]) / float(s_score[item][2])
    return s_score
    
def calcuStockScoeWeighted(s_score,  params,  key):
    items= []
    for item in s_score:
        items.append(item)
    for item in items:
        p = s_score[item][0]
        if p not in s_score:
            s_score[p] = [0,  0,  0]
        s_score[p][0]+=s_score[item][1]
        s_score[p][1]+=s_score[item][2]
        s_score[p][2] = float(s_score[p][0])/float(s_score[p][1])
    percent = 0.0
    count = 0
    for p in params:
        if p in s_score:
            percent += s_score[p][2]
            count+=1
    s_score["weighted"] = (float(percent)/float(count))* float(g_scoretab[key]['weighted'])
    return s_score

def scoreStockNearAvg(key):
    print(traceback.extract_stack(None, 2)[0][2])
    score_near_manage = {}
    data = g_scoretab[key]['data']
    params = g_scoretab[key]['parameter']
    for stock_id in data:
        s_score = {}
        s = data[stock_id]['original_scrore']
        for i in range(len(s)):
            f = s[i][0]
            if f == "calculateNearAvg":
                addStockScore(params,  "calculateNearAvg",  "satisfy_min_near",  s_score,  
                                      s[i][1])
        if len(s_score)>0:
            calcuStockScoeWeighted(s_score,  params,  key)
            score_near_manage[stock_id] = s_score
    g_caculate_score_tab[key] = score_near_manage
    
def scoreStockQuantity(key):
    print(traceback.extract_stack(None, 2)[0][2])
    score_near_manage = {}
    data = g_scoretab[key]['data']
    params = g_scoretab[key]['parameter']
    for stock_id in data:
        s_score = {}
        s = data[stock_id]['original_scrore']
        for i in range(len(s)):
            f = s[i][0]
            if f == "checkQuantity":
                d = 0.0
                if s[i][1] != 0:
                    d = float(s[i][1] - s[i][4])/float(s[i][1])
                addStockScore(params,  "checkQuantity",  "satisfy_min_quantity",  s_score,  d)
                d = 0.0
                if s[i][6] != 0:
                    d = float(s[i][5])/float(s[i][6]) 
                addStockScore(params,  "checkQuantity",  "exceed_avg_times",  s_score,  d)
        if len(s_score)>0:
            calcuStockScoeWeighted(s_score,  params,  key)
            score_near_manage[stock_id] = s_score
    g_caculate_score_tab[key] = score_near_manage
    
def score_redK_mointor(key):
    print(traceback.extract_stack(None, 2)[0][2])
    score_near_manage = {}
    data = g_scoretab[key]['data']
    params = g_scoretab[key]['parameter']
    for stock_id in data:
        s_score = {}
        s = data[stock_id]['original_scrore']
        for i in range(len(s)):
            f = s[i][0]
            if f == "caculate_reqK_quantity_price#mean_quan":
                d = 0.0
                if s[i][5] != 0:
                    d = 1 - float(s[i][5])
                    if d <=0:
                        d  = 0.0
                addStockScore(params,  "caculate_redK_quantity_price",  "satisfy_redK_quantity",  s_score,  d)
            if f == "caculate_reqK_quantity_price#mean_price":
                d = 0.0
                if s[i][1] != 0:
                    d = 1 - float(s[i][1])
                    if d <=0:
                        d  = 0.0
                addStockScore(params,  "caculate_redK_quantity_price",  "satisfy_redK_price",  s_score,  d)
            if f == "caculate_reqK_quantity_price#success_times":
                d = 0.0
                if s[i][2] != 0:
                    d = float(s[i][1]) / float(s[i][2])
                addStockScore(params,  "caculate_redK_quantity_price",  "satisfy_redK_quantity_price",  s_score,  d)
            if f == "caculate_reqK_cross":
                d = 0.0
                if s[i][1] != 0:
                    d = 1 - float(s[i][1])
                    if d <=0:
                        d  = 0.0
                addStockScore(params,  "caculate_redK_cross",  "satisfy_min_quantity",  s_score,  d)
        if len(s_score)>0:
            calcuStockScoeWeighted(s_score,  params,  key)
            score_near_manage[stock_id] = s_score
    g_caculate_score_tab[key] = score_near_manage

def scoreMarkPriceTrend(key):
    print(traceback.extract_stack(None, 2)[0][2])
    score_near_manage = {}
    data = g_scoretab[key]['data']
    params = g_scoretab[key]['parameter']
    for stock_id in data:
        s_score = {}
        s = data[stock_id]['original_scrore']
        for i in range(len(s)):
            f = s[i][0]
            if f == "calculateMarkPriceTrend":
                d = 0.0
                k = 0.0
                if s[i][3] > s[i][4] and  s[i][3]>0 and  s[i][4]>0:
                    d = 1 - (float(s[i][4])/float(s[i][3]))
                    if s[i][1] == 1:
                        k = d
                addStockScore(params,  "calculateMarkPriceTrend",  "satisfy_price_increase",  s_score,  d)
                addStockScore(params,  "calculateMarkPriceTrend",  "satisfy_market_trend",  s_score,  k)
        if len(s_score)>0:
            calcuStockScoeWeighted(s_score,  params,  key)
            score_near_manage[stock_id] = s_score
    g_caculate_score_tab[key] = score_near_manage
    
def scoreCompanyRevenue(key):
    print(traceback.extract_stack(None, 2)[0][2])

    
def caculateScore():
    for key in g_scoretab:
        g_scoretab[key]['callbackFunc'](key)
    
    score_summary = {}
    result_summary = []
    for key in g_caculate_score_tab:
        stock_score = g_caculate_score_tab[key]
        for stock_id in stock_score:
            if stock_id not in score_summary:
                score_summary[stock_id] = {}
                score_summary[stock_id]['summary_score']  = 0.0
            data = stock_score[stock_id]
            score_summary[stock_id][key]  = 0
            if 'weighted' in data:
                 score_summary[stock_id][key] =  data['weighted']
            score_summary[stock_id]['summary_score'] +=score_summary[stock_id][key]
    for stock_id in score_summary:
        result_summary.append([stock_id,  score_summary[stock_id]['summary_score'] ])
    for i in range(len(result_summary)):
        for j in range(i+1,  len(result_summary)):
            if result_summary[i][1] < result_summary[j][1]:
                result_summary[i], result_summary[j] = result_summary[j], result_summary[i]
    print("===========Score Sort: "+ str(System.ScoreTop))
    for i in range(System.ScoreTop):
        s = "Top_"+str(i+1) + ":"
        s+= str(result_summary[i][0])
        s+= "  -- " + str(result_summary[i][1])
        print(s)
    
def initScore():
    global g_scoretab
    global g_caculate_score_tab
    
    for key in g_scoretab:
        if 'data' not in g_scoretab[key]:
            g_scoretab[key]['data'] = {}
    g_scoretab['caculateStockNearAvg']['callbackFunc'] = scoreStockNearAvg
    g_scoretab['calculateStockQuantity']['callbackFunc'] = scoreStockQuantity
    g_scoretab['caculate_redK_mointor']['callbackFunc'] = score_redK_mointor
    g_scoretab['caculateCompanyRevenue']['callbackFunc'] = scoreCompanyRevenue
    g_scoretab['calculateMarkPriceTrend']['callbackFunc'] = scoreMarkPriceTrend
            
if __name__ == "__main__":
    pass
