from app import app
if __name__ == '__main__':
    app.debug == True
    


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

    def __repr__(self):
        return f"Customer('{self.custid}', '{self.username}', '{self.email}')"

class Item(db.Model):
    itemid = db.Column(db.Integer, primary_key = True)
    itemname = db.Column(db.String(20), unique = True, nullable=False)
    deliverydate = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    expirydate = db.Column(db.DateTime, nullable=False)
    costprice = db.Column(db.Integer, nullable=False)
    sellingprice = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Item('{self.itemid}', '{self.itemname}', '{self.sellingprice}', '{self.expirydate}')"

db.create_all()
customer1 = Customer(username = 'TarunR123', fullname = 'Tarun Ramesh', email = 'abc@gmail.com', phonenum = 1234, password = 'password')
db.session.add(customer1)
customer2 = Customer(username = 'Mayuri123', fullname = 'Mayuri Pandey', email = 'abc@gmail.com', phonenum = 12345, password = 'password')
db.session.add(customer2)
db.session.commit()
print(Customer.query.all())

 

# class Sales(db.Model):
#     itemid = db.Column(db.Integer, db.foriegn_key('item.itemid'))
#     customrid = db.Column(db.Integer, db.foriegn_key('customer.custid'))
#     itemname = db.Column(db.Integer, db.foriegn_key('Item.itemid'))
#     sellingdate = db.column(db.DateTime, nullable=False, default = datetime.utcnow)
#     costprice = db.column(db.Integer(20), nullable=False)
#     sellingprice = db.column(db.Integer(20), nullable=False)

#     def __repr__(self):
#         return f"Customer('{self.itemid}', '{self.itemname}', '{self.sellingprice}', '{self.expirydate}')"



app.run()
