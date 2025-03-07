from flask import *
import pyttsx3
import mysql.connector as sql
import datetime,math

def interest(p,day_took):
    today = datetime.date.today()
    diff = (today-day_took).days
    return math.ceil((p*0.067*diff)/100)

conn = sql.connect(host="localhost",user="root",passwd="Pavitra@01",database="fertilizer_shop")
app = Flask(__name__)
engine = pyttsx3.init()
c = conn.cursor()

voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

if conn.is_connected():
    engine.say("Connection Successful")
    engine.runAndWait()


@app.route('/')
def home():
    return render_template('/home.html')

@app.route('/dashboard',methods = ['POST','GET'])
def authorize():
    admin = request.form['name']
    passwd = request.form['pass']
    c.execute("select * from access")
    for i in c.fetchall():
        if str(i[0]) == admin and str(i[1]) == passwd:
            c.execute("select * from debt_customer_details ")
            res1 = c.fetchall()
            c.execute("select * from paid_customer_details ")
            res2 = c.fetchall()
            return render_template('/dashboard.html',paid_customers=res2,ad=admin,debt_customers = res1)
    return redirect(url_for('home'))

@app.route('/dashboard/customer')
def customer():
    return render_template('/customer.html')

@app.route('/dashboard/worker')
def worker():
    return render_template('/worker.html')

@app.route('/dashboard/stock')
def stock():
    return render_template('/stock.html')

@app.route('/dashboard/stats')
def stats():
    return render_template('/stats.html')

@app.route('/dashboard/customer/cash')
def cash():
    return render_template('/cash.html')

@app.route('/dashboard/customer/cash2',methods = ['POST'])
def cash2():
    name = request.form['name']
    phone = request.form['phone']
    product = request.form['product']
    c.execute("select cash_price from product_details where product_name = '{}'".format(str(product)))
    amount = c.fetchone()[0]
    c.execute("insert into paid_customer_details values('{}','{}','{}','{}','{}')".format(name,phone,product,amount,datetime.date.today()))
    conn.commit()
    return redirect(url_for('customer'))

@app.route('/dashboard/customer/debt')
def debt():
    return render_template('/debt.html')

@app.route('/dashboard/customer/debt2',methods = ['POST'])
def debt2():
    name = request.form['name']
    phone = request.form['phone']
    product = request.form['product']
    c.execute("select cash_price from product_details where product_name = '{}'".format(str(product)))
    amount = c.fetchone()[0]
    c.execute("insert into debt_customer_details values('{}','{}','{}','{}','{}')".format(name,phone,product,amount,datetime.date.today()))
    conn.commit()
    return redirect(url_for('customer'))

@app.route('/dashboard/customer/clear')
def clear():
    return render_template('clear.html')

@app.route('/dashboard/customer/clear2',methods = ['POST'])
def clear2():
    Phone = request.form['phone']
    c.execute("select amount,date from debt_customer_details where phone = '{}'".format(Phone))
    res = c.fetchall()
    debt = 0
    for i in res:
        debt += (i[0]+interest(i[0],i[1]))
    return render_template('clear2.html',debt=debt,phone=Phone)

@app.route('/dashboard/customer/clear3',methods = ['POST'])
def clear3():
    Phone = request.form['phone']
    c.execute("select amount,date from debt_customer_details where phone = '{}'".format(Phone))
    res = c.fetchall()
    debt = 0
    for i in res:
        debt += (i[0]+interest(i[0],i[1]))
    c.execute("select * from debt_customer_details where phone = '{}'".format(Phone))
    res2 = c.fetchall()
    name = res2[0][0]
    c.execute("delete from debt_customer_details where phone = '{}'".format(Phone))
    conn.commit()
    product = "Clearance"
    c.execute("insert into paid_customer_details values('{}','{}','{}','{}','{}')".format(name,Phone,product,debt,datetime.date.today()))
    conn.commit()
    return redirect(url_for('customer'))

if __name__ == '__main__':
    app.run()