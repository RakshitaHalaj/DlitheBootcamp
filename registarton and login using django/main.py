from flask import Flask, render_template, request, redirect, url_for, session 
from flask_mysqldb import MySQL 
import MySQLdb.cursors 
import MySQLdb.cursors, re, hashlib 

app = Flask(__name__)
app.secret_key = 'test'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rohan@1530'
app.config['MYSQL_DB'] = 'user_db1'

mysql = MySQL(app)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accountuser WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            print(account['id'])
            return 'Logged in successfully!'
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts')
        accounts = cursor.fetchall()
        return render_template('dashboard.html', accounts=accounts)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/signup/', methods=['GET', 'POST'])
def registr():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        #confirm-password=request.form['confirm-password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accountuser WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accountuser (username, password, email) VALUES ( %s, %s,%s)',
                           (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('registration.html', msg=msg)



if __name__ == '__main__':
    app.run()
