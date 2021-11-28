
from app import app
from flask import render_template,request
from run import *
from sqlalchemy.orm import session

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
    phonenum = db.Column(db.String(20), nullable=False)
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
    quantity = db.Column(db.Integer, nullable=False)
    minquantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Item('{self.itemid}', '{self.itemname}', '{self.deliverydate}', '{self.expirydate}' '{self.costprice}', '{self.sellingprice}', '{self.quantity}', '{self.minquantity}', '{self.status}')"

db.create_all()

######################################################################################################################
######################################################################################################################

@app.route('/')
def index():
    print(Customer.query.all())
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
    customerdetails = Customer(username = uname, fullname = name, email = email, phonenum = phno, password = psw)
    db.session.add(customerdetails)
    db.session.commit()
    return render_template("CustomerLogin.html")

@app.route('/customerlogin')
def customerlogin():
    return render_template("CustomerLogin.html")

@app.route('/loginvalidation', methods =['POST'])
def loginvalidation():
    uname = str(request.form['username'])
    psd = str(request.form['password'])
    tableentryname = db.session.query(Customer).filter(Customer.username == uname)
    tableentry = db.session.query(Customer.password).filter(Customer.username == uname)
    for validationvar in tableentry:
        if validationvar.password == psd:
            for testusn in tableentryname:
                global usn
                usn = testusn.username
            return render_template("CustomerLoggedIn.html")
    return "<H2>The password/username entered is incorrect. Please go back and try again.</H2>" 
    

       
@app.route('/customerloggedin')
def customerloggedin():
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
    selectedfield = str(request.form['selectedfield'])
    updatevalue = str(request.form['updatevalue'])
    customerupdate = Customer.query.filter_by(username = usn).first()
    customerupdate.fullname = updatevalue
    db.session.commit()
    return render_template("CustomerLoggedIn.html")

@app.route('/balancerecharge')
def balancerecharge():
    return render_template("BalanceRecharge.html")

@app.route('/balanceupdate', methods =['POST'])
def balanceupdate():
    # check type casting to Integer from String!!!!!!!!!!!!
    rechargeamt = int(request.form['rechargeamt'])
    balanceupdate = Customer.query.filter_by(username = usn).first()
    balanceupdate.accountbalance = balanceupdate.accountbalance + int('newbalance')
    db.session.commit()
    return render_template("CustomerLoggedIn.html")

@app.route('/deleteaccount')
def deleteaccount():
    return render_template("DeleteAccount.html")

@app.route('/accountremoval')
def accountremoval():
    db.session.delete(usn)
    db.session.commit()
    return render_template("CustomerLogin.html") 

@app.route('/adminlogin')
def adminlogin():
    return render_template("AdminLogin.html")

@app.route('/adminvalidation', methods = ['POST'])
def adminvalidation():
    uname = str(request.form['username'])
    psd = str(request.form['password'])
    if uname == 'Admin' and psd == 'password':
        return render_template("AdminDashboard.html")
    else:
        return "<h2>The password or username entered was incorrect, please go back and try again.</h2>" 

@app.route('/admindashbard')
def admindashboard():
    return render_template("AdminDashboard.html")