
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
    address = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    accountbalance = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"Customer('{self.custid}', '{self.username}', '{self.fullname}', '{self.email}','{self.phonenum}', '{self.password}')"

class Item(db.Model):
    itemid = db.Column(db.Integer, primary_key = True, autoincrement = True)
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
    customerdetails = Customer(username = request.form['uname'], fullname = request.form['name'], email = request.form['email'], phonenum = request.form['phoneNo'], password = request.form['psw'], address = request.form['address'])
    db.session.add(customerdetails)
    db.session.commit()
    return render_template("CustomerLogin.html")

@app.route('/customerlogin')
def customerlogin():
    return render_template("CustomerLogin.html")

@app.route('/loginvalidation', methods =['POST', 'GET'])
def loginvalidation():
    uname = str(request.form['username'])
    psd = str(request.form['password'])
    tableentryname = db.session.query(Customer).filter(Customer.username == uname)
    tableentry = db.session.query(Customer.password).filter(Customer.username == uname)
    for validationvar in tableentry:
        if validationvar.password == psd:
            for testdata in tableentryname:
                global usn
                usn = testdata.username
                global password
                password = testdata.password
            return render_template("CustomerDashboard.html")
    return "<H2>The password/username entered is incorrect. Please go back and try again.</H2>" 

@app.route('/customerdashboard')
def customerloggedin():
    return render_template("CustomerDashboard.html")

@app.route('/manageaccount')
def manageaccount():
    return render_template("ManageAccount.html")

@app.route('/updatevalues', methods =['POST'])
def getupdatevalue():
    selectedfield = str(request.form['selectedfield'])
    customerupdate = Customer.query.filter_by(username = usn).first()
    if selectedfield == "1":
        customerupdate.fullname = str(request.form['updatename'])
    elif selectedfield == "2":
        customerupdate.phonenum = str(request.form['updatenum'])
    elif selectedfield == "3":
        customerupdate.address = str(request.form['updateadd'])
    elif selectedfield == "4":
        customerupdate.email = str(request.form['updateemail'])
    elif selectedfield == "5":
        customerupdate.password = str(request.form['updatepsw'])
    db.session.commit()
    print(Customer.query.all())
    return render_template("CustomerDashboard.html")

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

@app.route('/accountremoval')
def accountremoval():
    deleteval = Customer.query.filter_by(username = usn).first()
    db.session.delete(deleteval)
    db.session.commit()
    print(Customer.query.all())
    return render_template("CustomerLogin.html") 

@app.route('/ownerlogin')
def adminlogin():
    return render_template("OwnerLogin.html")

@app.route('/ownervalidation', methods = ['POST'])
def adminvalidation():
    uname = str(request.form['username'])
    psd = str(request.form['password'])
    if uname == 'Owner' and psd == 'password':
        return render_template("OwnerDashboard.html")
    else:
        return "<h2>The password or username entered was incorrect, please go back and try again.</h2>" 

@app.route('/ownerdashbard')
def admindashboard():
    return render_template("OwnerDashboard.html")