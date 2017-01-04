ScoreTop = 20

#
#   'function name' :{
#         'weighted':  weighted score
#         'min_satisfy_percent':  this stock score must satisfy minium score precent. If not satisfy , this stock would be removal
#         'enable': this function enable or not
#   }
ScoreTab = {
    'caculateStockNearAvg':{ 
        'weighted' :  20 , 
        'min_satisfy_percent': 0.6, 
        'enable' : True,
        'parameter': {
             'calculateNearAvg' : {
                 'satisfy_min_near' :100, 
             }, 
        }, 
       'data':{} , 
    }, 
    'calculateStockQuantity':{ 
        'weighted' :  10 , 
        'min_satisfy_percent': 0.6, 
        'enable' : True,
        'parameter': {
             'checkQuantity' : {
                 'satisfy_min_quantity' : 20, 
                 'exceed_avg_times': 80, 
             }, 
        }, 
        'data':{}, 
    }, 
   'caculate_redK_mointor':{ 
        'weighted' :  50 , 
        'min_satisfy_percent': 0.6, 
        'enable' : True, 
        'parameter': {
             'caculate_redK_quantity_price' : {
                 'satisfy_redK_quantity' : 20, 
                 'satisfy_redK_price': 20, 
                 'satisfy_redK_quantity_price': 60, 
             }, 
             'caculate_redK_cross':{
                'satisfy_min_quantity' : 60,
             }, 
        }, 
        'data':{}, 
    },  
    'caculateCompanyRevenue':{ 
        'weighted' :  0 , 
        'min_satisfy_percent': 0.6, 
        'enable' : True, 
        'data':{}, 
    },  
    'calculateMarkPriceTrend':{ 
        'weighted' :  20 , 
        'min_satisfy_percent': 0.6, 
        'enable' : True,
        'parameter': {
             'calculateMarkPriceTrend' : {
                 'satisfy_price_increase' : 30, 
                 'satisfy_market_trend': 70, 
             }, 
        }, 
       'data':{},  
    },  
}
