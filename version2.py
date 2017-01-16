# coding:utf-8
from gevent import monkey, spawn, joinall, sleep
monkey.patch_all()  # Magic!

from huobi.Util import *
from huobi import HuobiService
from huobi.Conf import *
from random import random
import logging

from huobi import db_helper

logger = logging.getLogger('trades')
logger.setLevel(logging.INFO)
f_handler = logging.FileHandler('./trades.log')
formatter = logging.Formatter('%(asctime)s %(message)s')
f_handler.setFormatter(formatter)
logger.addHandler(f_handler)


def get_current_price():
    return HuobiService.getCurrentMarket()['ticker']['last']


global CURR_PRICE
global GRID_BIT_AMOUNT
global GRID_MONEY_SPAN
CURR_PRICE = get_current_price()
GRID_BIT_AMOUNT = 0.003
GRID_MONEY_SPAN = 1.0


def sure_buy(price, amount):
    trade_id = 0
    resp = {}
    while True:
        trade_id = int(1000000 * random())
        amount = format_amount(amount)
        resp = HuobiService.buy(1, str(price), str(amount), None, trade_id, BUY)
        # print resp
        if resp is not None and 'msg' not in resp and 'id' in resp:
            break
        sleep(1)
    return trade_id, resp['id']


def sure_sell(price, amount):
    trade_id = 0
    resp = {}
    while True:
        trade_id = int(1000000 * random())
        amount = format_amount2(amount)
        # print "before sell"
        resp = HuobiService.sell(1, str(price), str(amount), None, trade_id, SELL)
        # print resp
        # a bug resp can be none
        if resp is not None and 'msg' not in resp and 'id' in resp:
            break
        sleep(1)
    return trade_id, resp['id']


def sure_order_success(coin_type, order_id, order_price):
    global CURR_PRICE
    while True:
        resp = HuobiService.getOrderInfo(coin_type, order_id, ORDER_INFO)
        # print resp
        if resp is not None and 'msg' not in resp and 'status' in resp:         # all success
            if resp['status'] == 2:
                break
        sleep_time = get_sleep_time(abs(CURR_PRICE - order_price))
        sleep(sleep_time)


def draw_line_up(price):
    global GRID_BIT_AMOUNT
    while True:
        amount = GRID_BIT_AMOUNT
        print "up" + str(price)
        high_price = price
        # high_amount = GRID_MONEY_HALF / high_price
        # s_trade_id, s_order_id = sure_sell(high_price, high_amount)
        # print "sell_order price is :" + str(high_price)

        #  BIT_COIN amount as trade Unit
        s_trade_id, s_order_id = sure_sell(high_price, amount)
        # print "befor mysql"
        db_helper.insert_order(s_order_id, s_trade_id, 1, high_price, amount, 0)

        # half trade had finished, delete from orders table, add to half_trades table
        sure_order_success(1, s_order_id, price)
        db_helper.delete_order(s_order_id)
        db_helper.insert_half_trade(s_order_id, s_trade_id, 1, high_price, amount)

        print 'UP Sell %10.2f' % high_price
        logger.info('UP Sell %10.2f' % high_price)

        low_price = price - GRID_MONEY_SPAN
        # low_amount = GRID_MONEY_HALF / low_price
        # b_trade_id, b_order_id = sure_buy(low_price, low_amount)
        # print "buy_order price is :" + str(low_price)

        b_trade_id, b_order_id = sure_buy(low_price, amount)
        db_helper.insert_order(b_order_id, b_trade_id, 1, low_price, amount, 1)

        # two-way trade had finished, delete from orders table and half_trades table, add to trades table
        sure_order_success(1, b_order_id, price)
        db_helper.delete_order(b_order_id)
        db_helper.delete_half_trade(s_order_id)
        db_helper.insert_trades(s_order_id, s_trade_id, b_order_id, b_trade_id, 1,
                                high_price, low_price, amount)
        print 'UP Buy %10.2f' % low_price
        logger.info('UP Buy %10.2f' % low_price)

        logger.info("UP gain profit! %10.2f -- %10.2f" % (high_price, low_price))
        print "======================"
        print "UP gain profit! %10.2f -- %10.2f" % (high_price, low_price)
        print "======================"


def draw_line_down(price):
    global GRID_BIT_AMOUNT
    while True:
        amount = GRID_BIT_AMOUNT
        print "down" + str(price)
        low_price = price
        # low_amount = GRID_MONEY_HALF / low_price
        # b_trade_id, b_order_id = sure_buy(low_price, low_amount)
        # print "buy_order price is :" + str(low_price)

        b_trade_id, b_order_id = sure_buy(low_price, amount)
        db_helper.insert_order(b_order_id, b_trade_id, -1, low_price, amount, 0)

        # half trade had finished, delete from orders table, add to half_trades table
        sure_order_success(1, b_order_id, price)
        db_helper.delete_order(b_order_id)
        db_helper.insert_half_trade(b_order_id, b_trade_id, -1, low_price, amount)

        print 'DOWN Buy %10.2f' % low_price
        logger.info('DOWN Buy %10.2f' % low_price)

        high_price = price + GRID_MONEY_SPAN
        # high_amount = GRID_MONEY_HALF / high_price
        # s_trade_id, s_order_id = sure_sell(high_price, high_amount)
        # print "sell_order price is :" + str(high_price)

        s_trade_id, s_order_id = sure_sell(high_price, amount)
        db_helper.insert_order(s_order_id, s_trade_id, -1, high_price, amount, 1)

        # two-way trade had finished, delete from orders table and half_trades table, add to trades table
        sure_order_success(1, s_order_id, price)
        db_helper.delete_order(s_order_id)
        db_helper.delete_half_trade(b_order_id)
        db_helper.insert_trades(b_order_id, b_trade_id, s_order_id, s_trade_id, -1,
                                low_price, high_price, amount)

        print 'DOWN Sell %10.2f' % high_price
        logger.info('DOWN Sell %10.2f' % high_price)

        logger.info("DOWN gain profit! %10.2f -- %10.2f" % (low_price, high_price))
        print "======================"
        print "DOWN gain profit! %10.2f -- %10.2f" % (low_price, high_price)
        print "======================"


def get_sleep_time(diff):
    if diff < 5:
        return 1
    elif diff < 10:
        return 20
    elif diff < 20:
        return 150
    elif diff < 50:
        return 600
    elif diff < 100:
        return 1800
    else:
        return 7200


def format_amount(amount):
    return int(amount*10000)/10000.0


def format_amount2(amount):
    return int(amount * 1000) / 1000.0


def update_CURR_PRICE():
    global CURR_PRICE
    CURR_PRICE = get_current_price()
    sleep(10)


def get_manual_conf():
    global GRID_BIT_AMOUNT
    global GRID_MONEY_SPAN
    while True:
        with open("./amount.in", "r") as f:
            GRID_BIT_AMOUNT = float(f.read())
        with open("./grid_money_span.in", "r") as f:
            GRID_MONEY_SPAN = float(f.read())
        sleep(10)


def sure_cancel(trade_id):
    while True:
        resp = HuobiService.cancelOrder(1, trade_id, CANCEL_ORDER)
        if resp is not None and 'result' in resp:
            break
        sleep(3)


def get_order_status(order_id, order_price):
    while True:
        resp = HuobiService.getOrderInfo(1, order_id, ORDER_INFO)
        if resp is not None and 'msg' not in resp and 'status' in resp:
            return resp
            break
        sleep_time = get_sleep_time(abs(CURR_PRICE - order_price))
        sleep(sleep_time)


def reverse_draw_up(reverse_price, price, amount, forward_order_id=0, forward_trade_id=0):
    b_trade_id, b_order_id = sure_buy(reverse_price, amount)
    db_helper.insert_order(b_order_id, b_trade_id, 1, reverse_price, amount, 1)

    # two-way trade had finished, delete from orders table and half_trades table, add to trades table
    sure_order_success(1, b_order_id, reverse_price)
    db_helper.delete_order(b_order_id)
    db_helper.delete_half_trade(forward_order_id)
    db_helper.insert_trades(forward_order_id, forward_trade_id, b_order_id, b_trade_id, 1,
                            price, reverse_price, amount)
    print 'UP Buy %10.2f' % reverse_price
    logger.info('UP Buy %10.2f' % reverse_price)

    logger.info("UP gain profit! %10.2f -- %10.2f" % (price, reverse_price))
    print "======================"
    print "UP gain profit! %10.2f -- %10.2f" % (price, reverse_price)
    print "======================"
    spawn(draw_line_up, price)


def reverse_draw_down(reverse_price, price, amount, forward_order_id=0, forward_trade_id=0):
    s_trade_id, s_order_id = sure_sell(reverse_price, amount)
    db_helper.insert_order(s_order_id, s_trade_id, -1, reverse_price, amount, 1)

    # two-way trade had finished, delete from orders table and half_trades table, add to trades table
    sure_order_success(1, s_order_id, reverse_price)
    db_helper.delete_order(s_order_id)
    db_helper.delete_half_trade(forward_order_id)
    db_helper.insert_trades(forward_order_id, forward_trade_id, s_order_id, s_trade_id, -1,
                            price, reverse_price, amount)

    print 'DOWN Sell %10.2f' % reverse_price
    logger.info('DOWN Sell %10.2f' % reverse_price)

    logger.info("DOWN gain profit! %10.2f -- %10.2f" % (price, reverse_price))
    print "======================"
    print "DOWN gain profit! %10.2f -- %10.2f" % (price, reverse_price)
    print "======================"
    spawn(draw_line_down, price)


def deal_old_order(order):
    order_id = order[0]
    trade_id = order[1]
    up_down = order[2]
    price = order[3]
    amount = order[4]
    status = order[5]

    # get the order status on server, then check
    order_info = get_order_status(order_id, price)
    if order_info['status'] > 2:
        return

    if order_info['status'] == 0:
        sure_cancel(order_id)
        db_helper.delete_order(order_id)
        if status == 0:
            if up_down == 1:
                spawn(draw_line_up, price)
            else:
                spawn(draw_line_down, price)
        else:
            if up_down == 1:
                reverse_draw_up(price, price + up_down * GRID_MONEY_SPAN, amount)
            else:
                reverse_draw_down(price, price + up_down * GRID_MONEY_SPAN, amount)

    if order_info['status'] == 1:
        amount = order_info['amount'] - order_info['processed_amount']

    # order_info['status'] == 2, this order finished!
    if order_info['status'] == 2 or order_info['status'] == 1:
        db_helper.delete_order(order_id)
        # this order is a forward order
        if status == 0:
            db_helper.insert_half_trade(order_id, trade_id, up_down, price, amount)
            if up_down == 1:
                reverse_draw_up(price - up_down * GRID_MONEY_SPAN, price, amount)
            else:
                reverse_draw_down(price - up_down * GRID_MONEY_SPAN, price, amount)
        # this order is a reverse order
        else:
            db_helper.delete_half_trade(order_id)
            db_helper.insert_trades(0, 0, order_id, trade_id, up_down, 0, price, amount)
            if up_down == 1:
                spawn(draw_line_up, price)
            else:
                spawn(draw_line_down, price)


def continue_prev_orders():
    orders = db_helper.select_table("orders")
    for order in orders:
        spawn(deal_old_order, order)        



if __name__ == '__main__':
    CURR_PRICE = get_current_price()
    HIGHEST = CURR_PRICE
    LOWEST = CURR_PRICE

    #load previos data from database and manual data from file
    db_helper.load_from_db()
    spawn(get_manual_conf)
    continue_prev_orders()

    while True:
        print "HIGHEST :" + str(HIGHEST)
        print "LOWEST :" + str(LOWEST)
        print "curr :" + str(CURR_PRICE)

        if CURR_PRICE >= HIGHEST - CRITICAL_DIFF:
            for i in range(1, LINE_NUM+1):
                spawn(draw_line_up, HIGHEST + i * GRID_SPAN)
            HIGHEST = HIGHEST + LINE_NUM * GRID_SPAN

        if CURR_PRICE <= LOWEST + CRITICAL_DIFF:
            for i in range(1, LINE_NUM+1):
                spawn(draw_line_down, LOWEST - i * GRID_SPAN)
            LOWEST = LOWEST - LINE_NUM * GRID_SPAN

        db_helper.update_high_low(HIGHEST, LOWEST)

        sleep(60)
        CURR_PRICE = get_current_price()




