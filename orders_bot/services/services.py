import sqlite3
from datetime import datetime, timedelta

days_of_week = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']

def delete_orders_by_date(date):

    conn = sqlite3.connect('cafe_bot\orders.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE date < ?", (date,))
    conn.commit()
    conn.close()

def day_list():

    now = datetime.now()
    if now.hour >= 14:
        start_date = now + timedelta(days=2)
    else:
        start_date = now + timedelta(days=1)
    next_seven_days = []
    for i in range(7):
        next_seven_days.append(start_date + timedelta(days=i))
    days = []
    for date in next_seven_days:
        days.append(days_of_week[date.weekday()])
    return days

def get_orders_by_time(time):

    conn = sqlite3.connect('cafe_bot\orders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT tg_id, product, time FROM orders WHERE time = ?", (time,))
    rows = cursor.fetchall()
    orders_dict = {}
    for row in rows:
        tg_id, product, order_time = row
        if tg_id not in orders_dict:
            orders_dict[tg_id] = []
        orders_dict[tg_id].append((product, order_time))
    conn.close()

    result = ""
    for tg_id, orders in orders_dict.items():
        result += f"tg_id ({tg_id}):\n"
        for order in orders:
            product, order_time = order
            result += f"    {product}\n"
    return result

