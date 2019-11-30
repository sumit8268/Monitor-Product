import random
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
import yaml
import pricescrap
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_HOST'] = db['mysql_host']
mysql = MySQL(app)




userd = ""
passd = ""
url1 = ""
@app.route("/", methods=['POST', 'GET'])
def login():
    try:
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
    except:
        flash("!Something went wrong , Try Again...")
        return render_template("website/login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    try:
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
    except :
        flash("!Something went wrong , Try Again...")
        return render_template("website/signup.html")



@app.route("/profile", methods=['POST', 'GET'])
def profile():

    global userd
    try:
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
    except :
        flash("!Something went wrong , Try Again...")
        return render_template("website/profile.html", user=user, email=email, mob=mob)

site = ""
title = ""
price = ""
img = ""


@app.route("/home", methods=['POST', 'GET'])
def home():
    global title, price, img, site, userd, url1
    try:
        if request.method == 'POST':
            page = request.form
            try:
                url = page['search']
                url1 = url
                s, t, p, i, u = pricescrap.price(url)
                site, title, price, img, url1 = s, t, p, i, u
                flash(s)
                flash(i)
                flash(t)
                flash(p)
                return redirect(url_for('home', url=u))
            except :
                img1 = request.form[img]
                site1 = request.form[site]
                title1 = request.form[title]
                price1 = request.form[price]
                pr = price1[1:].replace(',','')
                dprice = request.form['dprice']
                u1 = request.args['url']

                con = mysql.connection.cursor()
                con.execute('insert into prod values("%s","%s","%s","%s","%s","%s","%s","%s")'%(userd, site1, u1, img1, title1, pr, dprice, pr))
                mysql.connection.commit()
                return redirect(url_for('dashboard'))
                #return redirect(url_for('track_price', site=site1,img=img1,title=title1,price=pr,dprice=dprice))
        elif request.method == 'GET':
            return render_template("website/newindex.html")
    except:
        flash("!Something went wrong , Try Again...")
        return render_template("website/newindex.html")

@app.route("/sites")
def sites():
    return render_template("website/sites.html")


@app.route("/about")
def about():
    return render_template("website/about.html")


@app.route("/home/track_price")
def track_price():
    site1 = request.args['site']
    img1 = request.args['img']
    title1 = request.args['title']
    price1 = request.args['price']
    dprice = request.args['dprice']
    flash(site1)
    flash(img1)
    flash(title1)
    flash(price1)
    flash(dprice)
    return render_template("website/track_price.html")


@app.route("/dashboard")
def dashboard():
    global userd
    try:
        email = userd
        con = mysql.connection.cursor()
        con.execute('select * from prod where email="%s";'%(email))
        rs = con.fetchall()
        l = []
        m = []
        s = []
        si = []
        for row in rs:
            l.append(row[2])
            l.append(row[1])
            s.append(len(l)-2)
            si.append(len(l)-1)
            l.append(row[3])
            m.append(len(l)-1)
            l.append(row[4])
            l.append(row[5])
            l.append(row[6])
            l.append(row[7])
            l.append("next")

        return render_template("website/dashboard.html", data=l, l=len(l),m=m, s=s, s1=si)
    except :
        flash("!Something went wrong , Try Again...")
        return render_template("website/dashboard.html", data=l, l=len(l),m=m, s=s, s1=si)



@app.route("/forgetpass", methods=['POST', 'GET'])
def forgetpass():
    try:
        if request.method == 'POST':
            email = request.form['foremail']
            code = random.randint(111111, 999999)
            pricescrap.forgetpassmail(email, code)
            session['email'] = email
            session['code'] = str(code)
            return redirect(url_for('newpass'))
        elif request.method == 'GET':
            return render_template("website/forgetpass.html")
    except :
        flash("!Something went wrong , Try Again...")
        return render_template("website/forgetpass.html")


@app.route("/profile/newpass", methods=['POST', 'GET'])
def newpass():
    try:
        email = session['email']
        code = session['code']
        if request.method == 'POST':
            code1 = request.form['code']
            newp = request.form['pas']
            rnewp = request.form['cpas']
            if code == code1 and newp == rnewp:
                con = mysql.connection.cursor()
                con.execute('update user set password="%s" where email="%s"'%(newp, email))
                mysql.connection.commit()
                con.close()
                return redirect(url_for('login'))
            else:
                flash("!Something went wrong , Try Again...")
                return render_template("website/newpass.html")
        elif request.method == 'GET':
            return render_template("website/newpass.html")
    except :
        flash("!Something went wrong , Try Again...")
        return redirect(url_for('forgetpass'))





def schedule_track():
    with app.app_context():
        con = mysql.connection.cursor()
        con.execute("select * from prod;")

        rs = con.fetchall()
        if (rs):
            links = []
            for row in rs:
                links.append(row[2])
            for link in links:
                s, t, p, i, u = pricescrap.price(link)
                pr = p[1:].replace(',', '')
                con.execute('update prod set newprice="%s" where link="%s"'%(pr, link))
                mysql.connection.commit()
                con.close()



def track_price():
    with app.app_context():
        con = mysql.connection.cursor()
        con.execute('select *from prod;')
        rs = con.fetchall()
        if(rs):
            linkprice = []
            for row in rs:
                e = row[0]
                l = row[2]
                d = row[6]
                linkprice.append((l, d, e))
            for lp in linkprice:
                l1, d1, e1 = lp
                s, t, p, i, u = pricescrap.price(l1)
                pr = p[1:].replace(',', '')
                if float(d1) >= pr:
                    pricescrap.sendupdatemail(u, e1, t, pr)
        con.close()




schd = BackgroundScheduler(daemon=True)
schd.add_job(schedule_track, 'interval', minutes=180)
schd.add_job(track_price, 'interval', minutes=180)
# schd.add_job(sendmail, "interval", seconds=10)
schd.start()



if __name__ == "__main__":
    app.secret_key = "name11"
    app.run(debug=True)