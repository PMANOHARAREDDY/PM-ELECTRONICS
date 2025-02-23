from flask import *
import pyttsx3
import mysql.connector as sql

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

@app.route('/dashboard',methods = ['POST'])
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

@app.route('/customer')
def customer():
    return "HI customer function"

if __name__ == '__main__':
    app.run()