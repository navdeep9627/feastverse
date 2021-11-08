from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/createaccount')
def createaccount():
    return render_template("customer/CreateAccount.html")

@app.route('/customerlogin')
def customerlogin():
    return render_template("customer/CustomerLogin.html")

@app.route('/customerloggedin')
def customerloggedin():
    return render_template("customer/CustomerLoggedIn.html")

@app.route('/profilepage')
def profilepage():
    return render_template("customer/ProfilePage.html")

@app.route('/manageaccount')
def manageaccount():
    return render_template("customer/ManageAccount.html")

@app.route('/updateaccount')
def updateaccount():
    return render_template("customer/UpdateAccount.html")

@app.route('/balancerecharge')
def balancerecharge():
    return render_template("customer/BalanceRecharge.html")

@app.route('/deleteaccount')
def deleteaccount():
    return render_template("customer/DeleteAccount.html")