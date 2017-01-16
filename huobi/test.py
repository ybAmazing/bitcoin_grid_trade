from huobi.Util import *
from huobi import HuobiService

if __name__ == "__main__":
    ret = HuobiService.sell(1, 8000, 0.0038, "", 11, SELL)

    print ret
    #ret = HuobiService.getOrderIdByTradeId(1, 2, ORDER_ID_BY_TRADE_ID)
    #ret = HuobiService.getOrderInfo(1, ret['id'], ORDER_INFO)
    #print(ret)
