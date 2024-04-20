from flask import Flask, request, render_template, redirect, url_for
import os
import sqlite3
from werkzeug.utils import secure_filename
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'cafe_app/static/img'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_next_id():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(id) FROM products')
    result = cursor.fetchone()
    conn.close()
    return (result[0] + 1) if result[0] else 1

def add_product_to_db(name, image, price, status, product_group):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, image, price, status, product_group) VALUES (?, ?, ?, ?, ?)',
                   (name, image, price, status, product_group))
    conn.commit()
    conn.close()

def add_group_to_db(product_group):
    conn = sqlite3.connect('product_group.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO product_group (product_group) VALUES (?)',
                   (product_group,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    
    conn_products = sqlite3.connect('products.db')
    cursor_products = conn_products.cursor()
    cursor_products.execute('SELECT * FROM products')
    products = cursor_products.fetchall()

    conn_groups = sqlite3.connect('product_group.db')
    cursor_groups = conn_groups.cursor()
    cursor_groups.execute('SELECT * FROM product_group')
    groups = cursor_groups.fetchall()

    conn_products.close()
    conn_groups.close()

    return render_template('cafe_app.html', products=products, groups=groups, img_folder=app.config['UPLOAD_FOLDER'])

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']
    status = request.form['status']
    product_group_id = request.form['product_group']

    if 'image' in request.files:
        file = request.files['image']
        if file.filename == '':
            return 'Файл не выбран'
        if file and allowed_file(file.filename):
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
                
            filename = secure_filename(file.filename)

            filename_without_extension = name.replace(" ", "") + str(get_next_id())
            filename_with_extension = filename_without_extension + os.path.splitext(filename)[1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_with_extension))
            image_path = filename_with_extension
        else:
            return 'Недопустимый формат файла'
    else:
        return 'Картинка не найдена'

    add_product_to_db(name, image_path, price, status, product_group_id)
    return redirect(url_for('index'))

@app.route('/toggle_status_or_delete', methods=['POST'])
def toggle_status_or_delete():
    action = request.form['action']
    selected_products = request.form.getlist('selected_products')

    if not selected_products:
        return 'Не выбраны товары для изменения статуса или удаления.'

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    if action == 'in_stock':
        cursor.execute('UPDATE products SET status=? WHERE id IN ({seq})'.format(seq=','.join(['?']*len(selected_products))), ('В наличии',) + tuple(selected_products))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    elif action == 'out_of_stock':
        cursor.execute('UPDATE products SET status=? WHERE id IN ({seq})'.format(seq=','.join(['?']*len(selected_products))), ('Нет в наличии',) + tuple(selected_products))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    elif action == 'delete':

        cursor.execute('SELECT image FROM products WHERE id IN ({seq})'.format(seq=','.join(['?']*len(selected_products))), tuple(selected_products))
        image_paths = cursor.fetchall()

        for image_path in image_paths:
            if image_path[0]:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_path[0])
                if os.path.exists(image_path):
                    os.remove(image_path)

        cursor.execute('DELETE FROM products WHERE id IN ({seq})'.format(seq=','.join(['?']*len(selected_products))), tuple(selected_products))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + search_term + '%',))
    products = cursor.fetchall()
    conn.close()
    return render_template('cafe_app.html', products=products, img_folder=app.config['UPLOAD_FOLDER'])

@app.route('/add_group', methods=['POST'])
def add_group():
    product_group = request.form['name']
    add_group_to_db(product_group)
    return redirect(url_for('index'))

@app.route('/delete_groups', methods=['POST'])
def delete_groups():
    selected_groups = request.form.getlist('selected_groups')
    conn = sqlite3.connect('product_group.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM product_group WHERE id IN ({seq})'.format(seq=','.join(['?']*len(selected_groups))), selected_groups)
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/run_python_script')
def run_python_script():

    script_path = os.path.join(os.getcwd(), 'bot.py')

    try:

        activate_script = os.path.join(os.getcwd(), '.venv', 'Scripts', 'activate.bat')
        subprocess.run([activate_script], shell=True, check=True)
        
        result = subprocess.check_output(['python', script_path], shell=True)

        return render_template('cafe_app.html', output=result.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        return f"Error running script: {e}"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
