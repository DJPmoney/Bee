#
#   'function name' :{
#         'weighted':  weighted score
#         'min_satisfy_percent':  this stock score must satisfy minium score precent. If not satisfy , this stock would be removal
#         'enable': this function enable or not
#   }
ScoreTab = {
    'caculateStockNearAvg':{ 
        'weighted' :  10 , 
        'min_satisfy_percent': 0.6, 
        'enable' : True,
       'data':{} , 
    }, 
    'calculateStockQuantity':{ 
        'weighted' :  10 , 
        'min_satisfy_percent': 0.6, 
        'enable' : True, 
        'data':{}, 
    }, 
   'caculate_redK_mointor':{ 
        'weighted' :  50 , 
        'min_satisfy_percent': 0.6, 
        'enable' : True, 
        'data':{}, 
    },  
    'caculateCompanyRevenue':{ 
        'weighted' :  10 , 
        'min_satisfy_percent': 0.6, 
        'enable' : True, 
        'data':{}, 
    },  
    'calculateMarkPriceTrend':{ 
        'weighted' :  20 , 
        'min_satisfy_percent': 0.6, 
        'enable' : True,
       'data':{},  
    },  
}
