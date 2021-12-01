
from flask.helpers import url_for
from werkzeug.utils import redirect
from app import app
from flask import render_template,request
from run import *
from sqlalchemy.orm import session

######################################################################################################################
######################################################################################################################

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feastverse.db'
db = SQLAlchemy(app)

class Customer(db.Model):
    custid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(20), unique = True, nullable=False)
    fullname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phonenum = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    accountbalance = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Customer('{self.custid}', '{self.username}', '{self.fullname}', '{self.email}','{self.phonenum}', '{self.password}', '{self.address}', '{self.accountbalance}')"

class Item(db.Model):
    itemid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    itemname = db.Column(db.String(20), unique = True, nullable=False)
    deliverydate = db.Column(db.String(20), nullable=False, default = datetime.utcnow)
    expirydate = db.Column(db.String(20), nullable=False)
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

@app.route('/loginvalidation', methods =['POST'])
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
            return render_template("CustomerDashboard.html", username = testdata.username, fullname = testdata.fullname, email = testdata.email, phonenum = testdata.phonenum, address = testdata.address, accountbalance = testdata.accountbalance)
    return "<H2>The password/username entered is incorrect. Please go back and try again.</H2>" 

@app.route('/customerdashboard')
def customerdashboard():
    tableentryname = db.session.query(Customer).filter(Customer.username == usn)
    for testdata in tableentryname:
        return render_template("CustomerDashboard.html", username = testdata.username, fullname = testdata.fullname, email = testdata.email, phonenum = testdata.phonenum, address = testdata.address, accountbalance = testdata.accountbalance)
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
    return render_template("CustomerDashboard.html",username = customerupdate.username, fullname = customerupdate.fullname, email = customerupdate.email, phonenum = customerupdate.phonenum, address = customerupdate.address, accountbalance = customerupdate.accountbalance)

@app.route('/updateItems', methods =['POST'])
def getupdateItem():
    selectedid=str(request.form['selectedfield1'])
    selectedfield = str(request.form['selectedfield2'])
    Itemupdate = Item.query.filter_by(itemid = selectedid).first()
    if selectedfield == "1":
        Itemupdate.itemname = str(request.form['updatename'])
    elif selectedfield == "2":
        Itemupdate.quantity = str(request.form['updatequantity'])
        if int(request.form['updatequantity']) >= int(Itemupdate.quantity):
            Itemupdate.status = 'delivered'
    elif selectedfield == "3":
        Itemupdate.deliverydate = str(request.form['updatedd'])
    elif selectedfield == "4":
        Itemupdate.expirydate = str(request.form['updateed'])
    elif selectedfield == "5":
        Itemupdate.costprice = str(request.form['updatecp'])
    elif selectedfield == "6":
        Itemupdate.sellingprice = str(request.form['updatesp'])
    db.session.commit()
    items=[]
    tableentryname = db.session.query(Item)
    for testdata in tableentryname:
        a={'itemid':testdata.itemid,
                'itemname':testdata.itemname,
                'deliverydate':testdata.deliverydate,
                'expirydate':testdata.expirydate,
                'costprice':testdata.costprice,
                'sellingprice':testdata.sellingprice,
                'quantity':testdata.quantity,
                'minimumquantity':testdata.minquantity,
                'status':testdata.status}
        items.append(a)
    return render_template("OwnerDashboard.html", items=items)
    
@app.route('/balancerecharge')
def balancerecharge():
    return render_template("BalanceRecharge.html")

@app.route('/balanceupdate', methods =['POST'])
def balanceupdate():
    rechargeamt = 0
    rechargeamt = int(request.form['rechargeamt'])
    balanceupdate = Customer.query.filter_by(username = usn).first()
    balanceupdate.accountbalance = int(balanceupdate.accountbalance) + rechargeamt
    db.session.commit()
    tableentryname = db.session.query(Customer).filter(Customer.username == usn)
    for testdata in tableentryname:
        print("hi")
    return render_template("CustomerDashboard.html", username = testdata.username, fullname = testdata.fullname, email = testdata.email, phonenum = testdata.phonenum, address = testdata.address, accountbalance = testdata.accountbalance)

@app.route('/accountremoval')
def accountremoval():
    deleteval = Customer.query.filter_by(username = usn).first()
    db.session.delete(deleteval)
    db.session.commit()
    # print(Customer.query.all())
    return render_template("CustomerLogin.html") 

@app.route('/ownerlogin')
def adminlogin():
    return render_template("OwnerLogin.html")

@app.route('/ownervalidation', methods = ['POST'])
def adminvalidation():
    uname = str(request.form['username'])
    psd = str(request.form['password'])
    tableentryname = db.session.query(Item)
    if uname == 'Owner' and psd == 'password':
        items=[]
        for testdata in tableentryname:
            a={'itemid':testdata.itemid,
                'itemname':testdata.itemname,
                'deliverydate':testdata.deliverydate,
                'expirydate':testdata.expirydate,
                'costprice':testdata.costprice,
                'sellingprice':testdata.sellingprice,
                'quantity':testdata.quantity,
                'minimumquantity':testdata.minquantity,
                'status':testdata.status}
            items.append(a)
        return render_template("OwnerDashboard.html", items=items)
    else:
        return "<h2>The password or username entered was incorrect, please go back and try again.</h2>" 

@app.route('/ownerdashbard')
def admindashboard():
    tableentryname = db.session.query(Item)
    items = []
    for testdata in tableentryname:
        print("hi")
        a={'itemid':testdata.itemid,
            'itemname':testdata.itemname,
            'deliverydate':testdata.deliverydate,
            'expirydate':testdata.expirydate,
            'costprice':testdata.costprice,
            'sellingprice':testdata.sellingprice,
            'quantity':testdata.quantity,
            'minimumquantity':testdata.minquantity,
            'status':testdata.status}
        items.append(a)
    return render_template("OwnerDashboard.html", items=items)

