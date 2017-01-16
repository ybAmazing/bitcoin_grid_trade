#coding=utf-8
from gevent import monkey, spawn, joinall
monkey.patch_all()  # Magic!
from huobi.Util import *
from huobi import HuobiService
from huobi.Conf import *
import time
import json


def test():
    ret = HuobiService.getCurrentMarket()
    print ret

# def up_transaction(price):
#     high_price = price
#     high_amount = GRID_MONEY_HALF / high_price
#
#     trade_id = 1
#     while True:
#         ret = HuobiService.sell(1, str(high_price), str(high_amount), None, trade_id, SELL)
#         if ret:
#             insert_trade()
#             break
#
#     while True:
#         ret = HuobiService.getOrderIdByTradeId(trade_id)
#         if ret:
#             order_info = HuobiService.getOrderInfo(1, ret, SELL)
#             if order_info:
#                 break
#
#     low_price = price - GRID_MONEY_SPAN
#     low_amount = GRID_MONEY_HALF / low_price
#
#     trade_id = 2
#     while True:
#         ret = HuobiService.buy(1, str(low_price), str(low_amount), None, trade_id, BUY)
#         if ret:
#             break
#
#     while True:
#         ret = HuobiService.getOrderIdByTradeId(trade_id)
#         if ret:
#             order_info = HuobiService.getOrderInfo(1, ret, BUY)
#             if order_info:
#                 break
#     write_to_db()
#
#
# def down_transaction(price):
#     low_price = price
#     low_amount = GRID_MONEY_HALF / low_price
#     HuobiService.buy(1, str(low_price), str(low_amount), None, None, BUY)
#
#     high_price = price + GRID_SPAN
#     high_amount = GRID_MONEY_HALF / high_price
#     HuobiService.sell(1, str(high_price), str(high_amount), None, None, SELL)
#
#
#
#
# def draw_10_lines(draw_type):
#     if draw_type == 1:
#         for i in range(1, 11):
#             up_transaction(HIGHEST + GRID_MONEY_SPAN * i)
#
#     if draw_type == -1:
#         for i in range(1, 11):
#             down_transaction(LOWEST - GRID_MONEY_SPAN * i)

def getCurrentPrice():
    print HuobiService.getCurrentMarket()['ticker']['last']



if __name__ == "__main__":
    # ret = HuobiService.getCurrentMarket()
    # current_price = ret['last']
    # if current_price >= HIGHEST - CRITICAL_DIFF:
    #     draw_10_lines(current_price, 1)
    #
    # if current_price <= LOWEST + CRITICAL_DIFF:
    #     draw_10_lines(current_price, -1)


    # print "提交限价单接口"
    # print HuobiService.buy(1,"2355","0.01",None,None,BUY)
    # print "提交市价单接口"
    # print HuobiService.buyMarket(2,"30",None,None,BUY_MARKET)
    # print "取消订单接口"
    # print HuobiService.cancelOrder(1,68278313,CANCEL_ORDER)

    start = time.time()

    joinall([spawn(getCurrentPrice) for _ in range(300)])

    print "total spent time %d seconds " % (time.time() - start)


    #print ret

    # print "查询个人最新10条成交订单"
    # print HuobiService.getNewDealOrders(1,NEW_DEAL_ORDERS)
    # print "根据trade_id查询order_id"
    # print HuobiService.getOrderIdByTradeId(1,274424,ORDER_ID_BY_TRADE_ID)
    # print "获取所有正在进行的委托"
    # print HuobiService.getOrders(1,GET_ORDERS)
    # print "获取订单详情"
    # print HuobiService.getOrderInfo(1,68278313,ORDER_INFO)
    # print "现价卖出"
    # print HuobiService.sell(2,"22.1","0.2",None,None,SELL)
    # print "市价卖出"
    # print HuobiService.sellMarket(2,"1.3452",None,None,SELL_MARKET)



