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
            return render_template('/dashboard.html',ad=admin)
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

@app.route('/dashboard/stock/update_product')
def update_product():
    c.execute("select * from product_details")
    prdts = c.fetchall()
    return render_template('/pro_update.html',prdts=prdts)

@app.route('/dashboard/stock/update_product2',methods = ['POST','GET'])
def update_product2():
    cashon = request.form['cashon']
    debton = request.form['debton']
    producton = request.form['producton']
    c.execute("update product_details set cash_price = '{}', debt_price = '{}' where product_name = '{}'".format(cashon,debton,producton))
    conn.commit()
    return redirect(url_for('stock'))

@app.route('/dashboard/stock/add_stock')
def add_stock():
    return render_template('/add_stock.html')

@app.route('/dashboard/stock/add_stock2',methods = ['POST','GET'])
def add_stock2():
    product = request.form['product']
    quantity = request.form['quantity']
    c.execute("update stocks set quantity = quantity + '{}' where product_name = '{}'".format(quantity,product))
    conn.commit()
    return redirect(url_for('stock'))

@app.route('/dashboard/stats')
def stats():
    return render_template('/stats.html')

@app.route('/dashboard/stats/dstats')
def dstats():
    return render_template('/dstats.html')

@app.route('/dashboard/stats/dstats/db', methods = ['POST','GET'])
def db():
    date = request.form['date']
    c.execute("select sum(amount) from paid_customer_details where date = '{}'".format(date))
    camt = c.fetchall()
    c.execute("select sum(amount) from debt_customer_details where date = '{}'".format(date))
    damt = c.fetchall()
    c.execute("select sum(amount) from paid_customer_details where date = '{}' and product_name = 'Clearance'".format(date))
    ccamt = c.fetchall()
    c.execute("select count(*) from paid_customer_details where date = '{}'".format(date))
    c_ct = c.fetchall()
    c.execute("select count(*) from debt_customer_details where date = '{}'".format(date))
    d_ct = c.fetchall()
    return render_template('stats_f.html',ccash = camt[0][0],dcash = damt[0][0],c_amt = ccamt[0][0],cash_count = c_ct[0][0], debt_count = d_ct[0][0])

@app.route('/dashboard/stats/mstats')
def mstats():
    return render_template('/mstats.html')

@app.route('/dashboard/stats/mstats/mb', methods = ['POST','GET'])
def mb():
    date = request.form['month']
    c.execute("select sum(amount) from paid_customer_details where Month(date) = '{}' and Year(date) = '{}'".format(int(date[5:]),int(date[:4])))
    camt = c.fetchall()
    c.execute("select sum(amount) from debt_customer_details where Month(date) = '{}' and Year(date) = '{}'".format(int(date[5:]),int(date[:4])))
    damt = c.fetchall() 
    c.execute("select sum(amount) from paid_customer_details where Month(date) = '{}' and product_name = 'Clearance' and Year(date) = '{}'".format(int(date[5:]),int(date[:4])))
    ccamt = c.fetchall()
    c.execute("select count(*) from paid_customer_details where Month(date) = '{}' and Year(date) = '{}'".format(int(date[5:]),int(date[:4])))
    c_ct = c.fetchall()
    c.execute("select count(*) from debt_customer_details where Month(date) = '{}' and Year(date) = '{}'".format(int(date[5:]),int(date[:4])))
    d_ct = c.fetchall()
    return render_template('stats_f.html',ccash = camt[0][0],dcash = damt[0][0],debt_count = d_ct[0][0],cash_count = c_ct[0][0],c_amt = ccamt[0][0])

@app.route('/dashboard/stats/ystats')
def ystats():
    return render_template('/ystats.html')

@app.route('/dashboard/stats/ystats/yb', methods = ['POST','GET'])
def yb():
    date = request.form['year']
    c.execute("select sum(amount) from paid_customer_details where Year(date) = '{}'".format(int(date)))
    camt = c.fetchall()
    c.execute("select sum(amount) from debt_customer_details where Year(date) = '{}'".format(int(date)))
    damt = c.fetchall() 
    c.execute("select sum(amount) from paid_customer_details where product_name = 'Clearance' and Year(date) = '{}'".format(int(date)))
    ccamt = c.fetchall()
    c.execute("select count(*) from paid_customer_details where Year(date) = '{}'".format(int(date)))
    c_ct = c.fetchall()
    c.execute("select count(*) from debt_customer_details where Year(date) = '{}'".format(int(date)))
    d_ct = c.fetchall()
    return render_template('stats_f.html',ccash = camt[0][0],dcash = damt[0][0],debt_count = d_ct[0][0],cash_count = c_ct[0][0],c_amt = ccamt[0][0])

@app.route('/dashboard/stats/stocks')
def stocks():
    c.execute("select * from stocks")
    stcks = c.fetchall()
    return render_template('/stockstats.html',stcks = stcks)

@app.route('/dashboard/stats/products')
def products():
    c.execute("select * from product_details")
    prdts = c.fetchall()
    return render_template('/productstats.html',prdts = prdts)

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
    c.execute("update stocks set quantity = quantity-1 where product_name = '{}'".format(product))
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
    c.execute("update stocks set quantity = quantity-1 where product_name = '{}'".format(product))
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

@app.route('/dashboard/worker/view')
def view():
    c.execute('select * from worker_details')
    res = c.fetchall()
    return render_template('Worker_view.html',workers = res)

@app.route('/dashboard/worker/add_worker')
def add_worker():
    return render_template('add_worker.html')

@app.route('/dashboard/worker/add_worker2', methods = ['POST','GET'])
def add_worker2():
    name = request.form['name']
    age = request.form['age']
    phone = request.form['phone']
    salary = request.form['salary']
    job = request.form['job']
    c.execute("insert into worker_details values('{}','{}','{}','{}','{}')".format(name,job,phone,salary,age))
    conn.commit()
    return redirect(url_for('worker'))

@app.route('/dashboard/worker/update_worker')
def update_worker():
    c.execute('Select * from worker_details')
    res = c.fetchall()
    return render_template('worker_update.html',workers = res)

@app.route('/dashboard/worker/update_worker2', methods = ['POST','GET'])
def update_worker2():
    name = request.form['name']
    age = request.form['age']
    phone = request.form['phone']
    salary = request.form['salary']
    job = request.form['job']
    c.execute("update worker_details set age = '{}', phone = '{}', salary = '{}', job = '{}' where name = '{}'".format(age,phone,salary,job,name))
    conn.commit()
    return redirect(url_for('worker'))

if __name__ == '__main__':
    app.run(debug=True)