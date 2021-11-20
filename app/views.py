
from app import app
from flask import render_template,request
from run import *
from sqlalchemy.orm import session
# global usn
# usn = ""

######################################################################################################################
######################################################################################################################

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coen6311.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    custid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(20), unique = True, nullable=False)
    fullname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phonenum = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    accountbalance = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Customer('{self.custid}', '{self.username}', '{self.fullname}', '{self.email}','{self.phonenum}', '{self.password}')"

class Item(db.Model):
    itemid = db.Column(db.Integer, primary_key = True)
    itemname = db.Column(db.String(20), unique = True, nullable=False)
    deliverydate = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    expirydate = db.Column(db.DateTime, nullable=False)
    costprice = db.Column(db.Integer, nullable=False)
    sellingprice = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Item('{self.itemid}', '{self.itemname}', '{self.deliverydate}', '{self.expirydate}' '{self.costprice}', '{self.sellingprice}')"

db.create_all()

######################################################################################################################
######################################################################################################################

@app.route('/')
def index():
    # print(Customer.query.all())
    # usnfiltered = Customer.query.filter_by(username = "TarunR123")
    # print(usnfiltered)
    return render_template("Index.html")

@app.route('/createaccount')
def createaccount():
    return render_template("CreateAccount.html")

@app.route('/getcreatedaccount', methods =['POST'])
def getcreatedaccount(): 
    name = request.form['name']
    phno = request.form['phoneNo']
    address = request.form['address']
    email = request.form['email']
    uname = request.form['uname']
    psw = request.form['psw']
    # newcustdetails = {"name": name, "phonenum": phno, "address": address, "email":email, "username":uname, "password":psw}
    # print(newcustdetails)
    customerdetails = Customer(username = uname, fullname = name, email = email, phonenum = int(phno), password = psw)
    db.session.add(customerdetails)
    db.session.commit()
    print(Customer.query.all())
    return render_template("CustomerLogin.html")

@app.route('/customerlogin')
def customerlogin():
    return render_template("CustomerLogin.html")

@app.route('/loginvalidation', methods =['POST'])
def loginvalidation():
    uname = str(request.form['username'])
    psd = str(request.form['password'])
    tableentry = db.session.query(Customer.password).filter(Customer.username == uname)
    for validationvar in tableentry:
        if validationvar.password == psd:
            return render_template("CustomerLoggedIn.html", usn = uname)
        else:
            return "<H2>The password/username entered is incorrect. Please go back and try again.</H2>" 
        break
       
@app.route('/customerloggedin')
def customerloggedin():
    # if methods =['GET']:
    #     return render_template("CustomerLogin.html")
    return render_template("CustomerLoggedIn.html")

@app.route('/profilepage')
def profilepage():
    return render_template("ProfilePage.html")

@app.route('/manageaccount')
def manageaccount():
    return render_template("ManageAccount.html")

@app.route('/updateaccount')
def updateaccount():
    return render_template("UpdateAccount.html")

@app.route('/updatevalues', methods =['POST'])
def getupdatevalue():
    customerupdate = Customer.query.filter_by(username = 'usernamefromearlierpage').first()
    customerupdate.fullname = 'newfullname'
    customerupdate.email = 'newemail'
    customerupdate.phonenum = int('newnumber')
    customerupdate.password = 'newpassword'
    db.session.commit()
    return render_template("CustomerLoggedIn.html")

@app.route('/balancerecharge')
def balancerecharge():
    return render_template("BalanceRecharge.html")

@app.route('/balanceupdate', methods =['POST'])
def balanceupdate():
    rechargeamt = int(request.form['rechargeamt'])
    balanceupdate = Customer.query.filter_by(username = 'usernamefromearlierpage').first()
    balanceupdate.accountbalance = balanceupdate.accountbalance + int('newbalance')

@app.route('/deleteaccount')
def deleteaccount():
    return render_template("DeleteAccount.html")

@app.route('/accountremoval')
def accountremoval():
    psd = str(request.form['username'])
    db.session.delete(psd)
    db.session.commit() 

@app.route('/adminlogin')
def adminlogin():
    return render_template("AdminLogin.html")

@app.route('/adminvalidation', methods = ['POST'])
def adminvalidation():
    uname = str(request.form['username'])
    psd = str(request.form['password'])
    if uname == 'Admin' and psd == 'password':
        return render_template("")
    else:
        return "<h2>The password or username entered was incorrect, please go back and try again.</h2>" 