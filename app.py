from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
import ctypes
import yaml



app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_HOST'] = db['mysql_host']
mysql = MySQL(app)

userd = ""
passd = ""

@app.route("/", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        log = request.form
        u = log['user']
        p = log['pas']
        if u == "" or p == "" :
            flash("!All fields are required")
            return render_template("website/login.html")
        else :
            cur = mysql.connection.cursor()
            cur.execute('select * from user where email="%s" and password="%s";'%(u, p))
            rs = cur.fetchall()
            if rs[0][1] == u and rs[0][2] == p :
                global userd
                global passd
                userd = u
                passd = p
                return redirect(url_for('home'))
    elif request.method == 'GET':
        return render_template("website/login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        details = request.form
        n = details['name']
        u = details['user']
        p = details['pas']
        cpas = details['cpas']
        m = details['mob']
        if n == "" or u == "" or p == "" or cpas == "" or m == "" :
            flash("!All fields are required")
            return render_template("website/signup.html")
        else:
            if p != cpas:
                flash("!Password did not match")
                return render_template("website/signup.html")
            else:
                cur = mysql.connection.cursor()
                rs =cur.execute('insert into user values("%s","%s","%s","%s");'%(n,u,p,m))
                mysql.connection.commit()
                return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template("website/signup.html")



@app.route("/profile", methods=['POST', 'GET'])
def profile():
    global userd
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('select * from user where email="%s" and password="%s";'%(userd, passd))
        rs = cur.fetchall()
        user = rs[0][0]
        email = rs[0][1]
        pas = rs[0][2]
        mob = rs[0][3]
        return render_template("website/profile.html", user=user, email=email, mob=mob)
    elif request.method == 'POST':
        details = request.form
        n = details['name']
        u = details['user']
        m = details['mob']
        cur = mysql.connection.cursor()
        cur.execute('update user set name="%s",email="%s",phone="%s" where email="%s" and password="%s";' %(n, u, m, userd, passd))
        mysql.connection.commit()
        userd = u
        return render_template("website/profile.html", user=n, email=u, mob=m)


@app.route("/home")
def home():
    return render_template("website/newindex.html")


if __name__ == "__main__":
    app.secret_key = "name11"
    app.run(debug=True)