from app import db

from flask_login import UserMixin
from app import login
from werkzeug.security import generate_password_hash,check_password_hash


@login.user_loader
def load_user(id):
    return staff.query.get(int(id))

class staff(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_no = db.Column(db.String(64), index = True, unique = True)
    dob = db.Column(db.String(64))
    name = db.Column(db.String(100))
    password_harsh = db.Column(db.String(128))
    username = db.Column(db.String(64), index=True, unique=True)
    gender = db.Column(db.String(64))
    email = db.Column(db.String(64),index=True,unique=True)
    phone = db.Column(db.String(64),index=True,unique=True)
    adress = db.Column(db.String(100))
    position = db.Column(db.String(64))
    type= db.Column(db.String(64),default='active')
    pic = db.Column(db.String(150))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


#class user(UserMixin,db.Model):
    #id =db.Column(db.Integer,primary_key=True)
    #username =db.Column(db.String(64),index=True,unique=True)
    #password_harsh=db.Column(db.String(128))
    #email = db.Column(db.String(120),index=True,unique=True)
    #role=db.Column(db.String(64))

    #def set_password(self, password):
        #self.password_hash = generate_password_hash(password)

    #def check_password(self, password):
        #return check_password_hash(self.password_hash, password)

    #def __repr__(self):
        #return '<User {}>'.format(self.username)


class menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meal_name = db.Column(db.String(64))
    description = db.Column(db.String(100))
    type = db.Column(db.String(64))
    week_day = db.Column(db.String(64))
    status = db.Column(db.String(64))

class meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(100))
    price = db.Column(db.Numeric(11,2))
    img = db.Column(db.String(200))