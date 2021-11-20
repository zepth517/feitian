from flask import Flask, render_template, request, redirect
from flaskext.mysql import MySQL

import yaml

app = Flask(__name__)
mysql = MySQL()

db = yaml.safe_load(open('db.yaml'))

print(db)

app.config['MYSQL_DATABASE_HOST'] = db['mysql_host']
app.config['MYSQL_DATABASE_USER'] = db['mysql_user']
app.config['MYSQL_DATABASE_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DATABASE_DB'] = db['mysql_db']

mysql.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']

        conn = mysql.connect()
        cur = conn.cursor()

        cur.execute("INSERT INTO users(name, email) VALUES (%s, %s)", (name, email))
        conn.commit()

        cur.close()
        return redirect('/users')

    return render_template('index.html')


@app.route('/users')
def users():
        conn = mysql.connect()
        cur = conn.cursor()

        rst = cur.execute("SELECT * FROM users")
        if rst > 0:
            userDetails = cur.fetchall()
            return render_template('users.html', userDetails=userDetails)
        
        cur.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')