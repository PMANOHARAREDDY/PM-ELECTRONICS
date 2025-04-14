from flask import *
import pyttsx3
import mysql.connector as sql
import datetime,math
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

smtp_server = "smtp.gmail.com"
port = 587
sender_email = "manoharareddyp8@gmail.com"
password = "bpgo vgji tmkq lgkv"

def send_msg4(server, sender_email, customer_mails):
    customer_mails = tuple(customer_mails)
    query = "SELECT * FROM debt_customer_details WHERE email_id IN {}".format(customer_mails)
    c.execute(query)
    rows = c.fetchall()
    plain = rows 
    text = f"The following customers have not paid in the last 3 months:\n{plain}"
    c.execute("select email_id from worker_details where job = 'recovery'")
    rc = c.fetchall()
    temp_rc = []
    for i in rc:
        temp_rc.append(i[0])
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Recovery report"
        message["From"] = sender_email
        message["To"] = ", ".join(temp_rc)
        html = """\
        <html>
            <body style="background-color: #364585; font-family: Arial, sans-serif;">
                <div style="text-align: center; margin-top: 20px;">
                    <img src="https://drive.google.com/uc?id=1rkUgCxEtznORpG6iUfw1FGpuJRXHGgXW&export=download" alt="PM Electronics Logo" style="width: 300px; height: auto; border-radius: 10px;">
                </div>

                <h1 style="text-align: center; color: darkblue; background-color: lightyellow; padding: 10px; border-radius: 10px;">
                    Greetings from PM Electronics Pvt. Ltd
                </h1>

                <h2 style="color: red; text-align: center; background-color: #ffe4e1; padding: 10px; border-radius: 8px;">
                    Alert!!! Below customers didn't pay from the past 3 Months
                </h2>
        
                <h2 style="color: red; text-align: center; background-color: #ffe4e1; padding: 10px; border-radius: 8px;">
                    TAKE IMMEDIATE ACTION & RECOVER
                </h2>
            </body>
        </html>
        """
        part_plain = MIMEText(text, "plain")
        part_html = MIMEText(html, "html")
        message.attach(part_html)
        message.attach(part_plain)   
        server.sendmail(sender_email, temp_rc, message.as_string())
        print("Email sent successfully to:", ", ".join(temp_rc))
    except Exception as e:
        print(f"Failed to send email (Recovery AGENCY): {e}")

def send_msg2(server, sender_email, receiver_mails):
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Alert!!!! You forgot paying for the electronics you purchased"
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_mails)
        html = """\
        <html>
            <body style="background-color: #364585; font-family: Arial, sans-serif;">
                <div style="text-align: center; margin-top: 20px;">
                    <img src="https://drive.google.com/uc?id=1rkUgCxEtznORpG6iUfw1FGpuJRXHGgXW&export=download" alt="PM Electronics Logo" style="width: 300px; height: auto; border-radius: 10px;">
                </div>

                <h1 style="text-align: center; color: darkblue; background-color: lightyellow; padding: 10px; border-radius: 10px;">
                    Greetings from PM Electronics Pvt. Ltd
                </h1>

                <h2 style="color: red; text-align: center; background-color: #ffe4e1; padding: 10px; border-radius: 8px;">
                    Alert!!! You bought Items and didn't pay from the past 3 Months
                </h2>
        
                <h2 style="color: #ff0000; text-align: center; background-color: #e0ffe0; padding: 10px; border-radius: 8px;">
                    You debt is automatically increasing at a rate of 36 percent a year.<br>
                    pay early.... pay less
                </h2>

                <h2 style="color: darkgreen; text-align: center; background-color: #e0ffe0; padding: 10px; border-radius: 8px;">
                    Thank you for shopping from us
                </h2>
            </body>
        </html>
        """
        message.attach(MIMEText(html, "html"))
        server.sendmail(sender_email, receiver_mails, message.as_string())
        print("Email sent successfully to:", ", ".join(receiver_mails))
    except Exception as e:
        print(f"Failed to send email (3 MONTHS CASE): {e}")
    send_msg4(server, sender_email, receiver_mails)

def send_msg3(server, sender_email, receiver_mails):
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = "Alert!!!! You forgot paying for the electronics you purchased"
        message["From"] = sender_email
        message["To"] = ", ".join(receiver_mails)
        print(receiver_mails)
        html = """\
        <html>
            <body style="background-color: #364585; font-family: Arial, sans-serif;">
                <div style="text-align: center; margin-top: 20px;">
                    <img src="https://drive.google.com/uc?id=1rkUgCxEtznORpG6iUfw1FGpuJRXHGgXW&export=download" alt="PM Electronics Logo" style="width: 300px; height: auto; border-radius: 10px;">
                </div>

                <h1 style="text-align: center; color: darkblue; background-color: lightyellow; padding: 10px; border-radius: 10px;">
                    Greetings from PM Electronics Pvt. Ltd
                </h1>

                <h2 style="color: red; text-align: center; background-color: #ffe4e1; padding: 10px; border-radius: 8px;">
                    Alert!!! You bought Items and didn't pay from the past 1 Month
                </h2>
        
                <h2 style="color: #ff0000; text-align: center; background-color: #e0ffe0; padding: 10px; border-radius: 8px;">
                    You debt is automatically increasing at a rate of 36 percent a year.<br>
                    pay early.... pay less
                </h2>

                <h2 style="color: darkgreen; text-align: center; background-color: #e0ffe0; padding: 10px; border-radius: 8px;">
                    Thank you for shopping from us
                </h2>
            </body>
        </html>

        """
        message.attach(MIMEText(html, "html"))
        server.sendmail(sender_email, receiver_mails, message.as_string())
        print("Email sent successfully to:", ", ".join(receiver_mails))
    except Exception as e:
        print(f"Failed to send email(1 Month case): {e}")


def send_msg(server, sender_email):
    c.execute("select email_id, date from debt_customer_details")
    rows = c.fetchall()
    today = datetime.date.today()
    more_than_1month = []
    more_than_3months = []
    for i in rows:
        if (today-i[1]).days>90:
            more_than_3months.append(i[0])
        elif (today-i[1]).days>30:
            more_than_1month.append(i[0])
    send_msg2(server, sender_email, more_than_3months)
    send_msg3(server, sender_email, more_than_1month)

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

@app.route('/dashboard/customer/alerts')
def alert():
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            send_msg(server, sender_email)

    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate. Check your email credentials.")

    except Exception as e:
        print(f"An error occurred: {e}")
    return redirect(url_for('customer'))

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
    c.execute("update product_details set quantity = quantity + '{}' where product_name = '{}'".format(quantity,product))
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
    c.execute("select * from product_details")
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
    email = request.form['email']
    c.execute("select cash_price from product_details where product_name = '{}'".format(str(product)))
    amount = c.fetchone()[0]
    c.execute("insert into paid_customer_details values('{}','{}','{}','{}','{}','{}')".format(name,phone,product,amount,datetime.date.today(),email))
    conn.commit()
    c.execute("update product_details set quantity = quantity-1 where product_name = '{}'".format(product))
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
    email = request.form['email']
    c.execute("select cash_price from product_details where product_name = '{}'".format(str(product)))
    amount = c.fetchone()[0]
    c.execute("insert into debt_customer_details values('{}','{}','{}','{}','{}','{}')".format(name,phone,product,amount,datetime.date.today(),email))
    conn.commit()
    c.execute("update product_details set quantity = quantity-1 where product_name = '{}'".format(product))
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
    email = res2[0][5]
    c.execute("delete from debt_customer_details where phone = '{}'".format(Phone))
    conn.commit()
    product = "Clearance"
    c.execute("insert into paid_customer_details values('{}','{}','{}','{}','{}','{}')".format(name,Phone,product,debt,datetime.date.today(),email))
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
    c.execute("update worker_details set DOB = '{}', phone = '{}', salary = '{}', job = '{}' where name = '{}'".format(age,phone,salary,job,name))
    conn.commit()
    return redirect(url_for('worker'))

if __name__ == '__main__':
    app.run(debug=True)