import sqlite3
from datetime import datetime, timedelta

def save_username_to_database(tg_id, username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE tg_id = ?', (tg_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        cursor.execute('UPDATE users SET username = ? WHERE tg_id = ?', (username, tg_id))
    else:
        cursor.execute('INSERT INTO users (tg_id, username) VALUES (?, ?)', (tg_id, username))
    conn.commit()
    conn.close()

def available_products_and__groups():

    conn_products = sqlite3.connect('products.db')
    cursor_products = conn_products.cursor()

    cursor_products.execute("SELECT id, product_group FROM products WHERE status = 'В наличии'")

    available_ids = []
    available_groups = set() 
    for row in cursor_products.fetchall():
        available_ids.append(row[0])
        available_groups.add(row[1])

    conn_products.close()

    conn_product_group = sqlite3.connect('product_group.db')
    cursor_product_group = conn_product_group.cursor()
    cursor_product_group.execute("SELECT product_group FROM product_group ORDER BY id")
    ordered_groups = [row[0] for row in cursor_product_group.fetchall()]
    conn_product_group.close()
    sorted_groups = sorted(available_groups, key=lambda x: ordered_groups.index(x))

    return available_ids, sorted_groups

def get_product_names_by_group(group):
    
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM products WHERE product_group = ?", (group,))
    rows = cursor.fetchall()
    product_names = [row[0] for row in rows]
    conn.close()

    return product_names

def get_product_names_by_ids(product_ids):

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    placeholders = ', '.join('?' for _ in product_ids)
    query = f"SELECT name FROM products WHERE id IN ({placeholders})"
    cursor.execute(query, product_ids)
    rows = cursor.fetchall()
    product_names = [row[0] for row in rows]
    conn.close()

    return product_names

def get_products():

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    products_dict = {}
    for row in rows:
        name = row[1]

        products_dict[name] = {
            'id': row[0],
            'image': row[2],
            'price': row[3],
            'status': row[4],
            'product_group': row[5]
        }
    conn.close()
    return products_dict

def day_list():

    now = datetime.now()

    if now.hour >= 14:
        start_date = now + timedelta(days=2)
    else:
        start_date = now + timedelta(days=1)

    next_seven_days = []

    for i in range(7):
        next_seven_days.append(start_date + timedelta(days=i))

    days_of_week = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    days = []

    for date in next_seven_days:
        days.append(days_of_week[date.weekday()])

    return days

def add_choise(tg_id, choises):
    conn = sqlite3.connect('choise.db')
    c = conn.cursor()
    c.execute("INSERT INTO choises (tg_id, choises) VALUES (?, ?)", (tg_id, choises))
    conn.commit()
    conn.close()

def delete_choise(tg_id):
    conn = sqlite3.connect('choise.db')
    c = conn.cursor()
    c.execute("DELETE FROM choises WHERE tg_id=?", (tg_id,))
    conn.commit()
    conn.close()

def add_order(tg_id, product, time, date):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (tg_id, product, time, date) VALUES (?, ?, ?, ?)", (tg_id, product, time, date))
    conn.commit()
    conn.close()

def get_choises_by_id(tg_id):
    conn = sqlite3.connect('choise.db')
    c = conn.cursor()
    c.execute("SELECT choises FROM choises WHERE tg_id = ?", (tg_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None
    
def next_day_of_week(day_of_week):
    current_date = datetime.now().date()
    weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    day_of_week_lower = day_of_week.lower().replace(" ", "")
    day_of_week_index = weekdays.index(day_of_week_lower)
    current_day_of_week_index = current_date.weekday()
    days_until_next = (day_of_week_index - current_day_of_week_index) % 7
    if days_until_next <= 0:
        days_until_next += 7

    next_day_date = current_date + timedelta(days=days_until_next)

    return next_day_date
