# import os

import yaml, secrets
from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
# from werkzeug.security import generate_password_hash

app = Flask(__name__)
Bootstrap(app)
secrets = secrets.token_urlsafe(32)

# DB connection
db = yaml.full_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = secrets
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            form = request.form
            name = form['name']
            age = form['age']
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO employees(name, age) VALUES(%s, %s)', (name, age))
            mysql.connection.commit()
            flash('Your data is successfully saved!', 'success')
        except:
            flash('The saving is failed', 'danger')
    return render_template('index.html')


@app.route('/employees')
def employees():
    cursor = mysql.connection.cursor()
    result_value = cursor.execute('SELECT * FROM employees')
    if result_value > 0:
        employees = cursor.fetchall()
        return render_template('employees.html', employees=employees)


if __name__ == '__main__':
    app.run(debug=True)
