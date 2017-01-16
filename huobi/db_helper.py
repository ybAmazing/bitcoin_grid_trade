import MySQLdb
import time
import sys
from Conf import HIGHEST, LOWEST, TOTAL_PROFIT


def init_db():
    db = MySQLdb.connect("localhost", "root", "honeynet@ics2016", "huobi")
    cursor = db.cursor()

    try:
        cursor.execute("delete from orders")
        cursor.execute("delete from half_trades")
        # cursor.execute("delete from trades")
        db.commit()
    except:
        print sys.exc_info()[0]
        db.rollback()
    db.close()


def insert_order(order_id, trade_id, up_down, price, amount, status):
    db = MySQLdb.connect("localhost", "root", "honeynet@ics2016", "huobi")
    cursor = db.cursor()
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    sql = """insert into orders(order_id, trade_id, up_down, price, amount, status, order_time)
                values(%s,%s,%s,%s,%s,%s,'%s')
            """ % (order_id, trade_id, up_down, price, amount, status, now)

    # print sql
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print sys.exc_info()[0]
        db.rollback()
    db.close()


def delete_order(order_id):
    db = MySQLdb.connect("localhost", "root", "honeynet@ics2016", "huobi")
    cursor = db.cursor()
    sql = """delete from orders where order_id=%s""" % order_id

    # print sql
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print sys.exc_info()[0]
        db.rollback()
    db.close()


def insert_half_trade(order_id, trade_id, up_down, price, amount):
    db = MySQLdb.connect("localhost", "root", "honeynet@ics2016", "huobi")
    cursor = db.cursor()
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    sql = """insert into half_trades(order_id, trade_id, up_down, price, amount, deal_time)
                values(%s,%s,%s,%s,%s,'%s')
            """ % (order_id, trade_id, up_down, price, amount, now)

    # print sql
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print sys.exc_info()[0]
        db.rollback()
    db.close()


def delete_half_trade(order_id):
    db = MySQLdb.connect("localhost", "root", "honeynet@ics2016", "huobi")
    cursor = db.cursor()
    sql = """delete from half_trades where order_id=%s""" % order_id

    # print sql
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print sys.exc_info()[0]
        db.rollback()
    db.close()


def insert_trades(order_id_1, trade_id_1, order_id_2, trade_id_2, up_down, price1, price2, amount):
    db = MySQLdb.connect("localhost", "root", "honeynet@ics2016", "huobi")
    cursor = db.cursor()
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    sql = """insert into trades(order_id_1, trade_id_1, order_id_2, trade_id_2, up_down, price1, price2, amount, deal_time)
                values(%s,%s,%s,%s,%s,%s,%s,%s,'%s')
            """ % (order_id_1, trade_id_1, order_id_2, trade_id_2, up_down, price1, price2, amount, now)

    # profit_sql = ""
    # if price1 != 0 and price2 != 0:
    #     profit_sql = "update profit set sum=sum+%s" % (abs(price2-price1) * amount)

    try:
        cursor.execute(sql)
        # cursor.execute(profit_sql)
        db.commit()
    except:
        print sys.exc_info()[0]
        db.rollback()
    db.close()


def select_table(table):
    db = MySQLdb.connect("localhost", "root", "honeynet@ics2016", "huobi")
    cursor = db.cursor()
    sql = """select * from %s""" % table

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except:
        print sys.exc_info()[0]
        db.rollback()
    db.close()


# def update_profit(add_profit):
#     db = MySQLdb.connect("localhost", "root", "honeynet@ics2016", "huobi")
#     cursor = db.cursor()
#     sql = "update profit set sum=sum+%s" % add_profit
#     try:
#         cursor.execute(sql)
#         ret = cursor.fetchone()
#         return ret
#     except:
#         print sys.exc_info()[0]
#         db.rollback()
#     db.close()

# def update_high_low(highest, lowest):
#     db = MySQLdb.connect("localhost", "root", "honeynet@ics2016", "huobi")
#     cursor = db.cursor()
#     sql = "insert into high_low(highest, lowest) values(%s,%s)" % (highest, lowest)

#     try:
#         cursor.execute("delete from high_low")
#         cursor.execute(sql)
#         db.commit()
#     except:
#         print sys.exc_info()[0]
#         db.rollback()
#     db.close()


# def get_high_low():
#     db = MySQLdb.connect("localhost", "root", "honeynet@ics2016", "huobi")
#     cursor = db.cursor()
#     sql = "select * from high_low"

#     try:
#         cursor.execute(sql)
#         ret = cursor.fetchone()
#         return ret
#     except:
#         print sys.exc_info()[0]
#         db.rollback()
#     db.close()


# def get_prev_profit():
#     db = MySQLdb.connect("localhost", "root", "honeynet@ics2016", "huobi")
#     cursor = db.cursor()
#     sql = "select * from profit"
#     try:
#         cursor.execute(sql)
#         ret = cursor.fetchone()
#         return ret
#     except:
#         print sys.exc_info()[0]
#         db.rollback()
#     db.close()


if __name__ == '__main__':
    # insert_half_trade(1, 2, 0, 5210.2, 0.003)
    insert_trades(5, 6, 7, 8, 0, 1.2, 1.3, 0.002)
    # delete_order(1)
    # ret = select_table("trades")
    # for item in ret:
    #     print type(item[5])
    #update_high_low(123, 53)
    #print get_high_low()
    # a, b = get_high_low()
    # print a
    # print b





