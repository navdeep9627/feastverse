from flask import render_template
from app import app

@app.route('/adminlogin')
def adminlogin():
    return render_template("admin/AdminLogin.html")