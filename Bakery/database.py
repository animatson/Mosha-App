
from Bakery.factory import db,login_manager
from flask_login import UserMixin
from datetime import datetime,date


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    position_as = db.Column(db.String(150), nullable=True)
    phone_no = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'),nullable=True)
    mauzo = db.relationship('Mauzo',backref='seller',lazy=True)
    mpishi = db.relationship('Mpishi',backref='cooker',lazy=True)
    store = db.relationship('Store',backref='storekeeper',lazy=True) 
    
class ManunuziData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,default=datetime.now())
    maligafi = db.Column(db.String(150), nullable=False)
    unit = db.Column(db.String(50), nullable=True)
    idadi = db.Column(db.Integer, nullable=False)
    bei = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

class Bidhaa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    b_name = db.Column(db.String(100), nullable=False,unique=True)
    b_bei = db.Column(db.Integer, nullable=False)
    uzal = db.relationship('Uzalishaji',backref='bid',lazy=True)
    mauzo = db.relationship('Mauzo',backref='bid',lazy=True)
    madeni = db.relationship('Madeni',backref='bid',lazy=True)
    mpishi = db.relationship('Mpishi',backref='bid',lazy=True)

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maligafi = db.Column(db.String(50), nullable=False)
    units = db.Column(db.String(50), nullable=True)
    idadi = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

class Madeni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    kiasi_kalipa = db.Column(db.Integer, nullable=False)
    kiasi_baki = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Integer, default=1)
    bid_id =  db.Column(db.Integer, db.ForeignKey('bidhaa.id'),nullable=False)

class Uzalishaji(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,default=datetime.now)
    b_jumla = db.Column(db.Integer, nullable=False)
    bid_id = db.Column(db.Integer, db.ForeignKey('bidhaa.id'),nullable=False)

class Mauzo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,default=date.today())
    b_uza = db.Column(db.Integer, nullable=True,default=0)
    b_bei_uza = db.Column(db.Integer, nullable=True,default=0)
    jumla = db.Column(db.Integer, nullable=True, default=0)
    bid_id = db.Column(db.Integer, db.ForeignKey('bidhaa.id'),nullable=False,unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

class Mpishi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime,default=date.today())
    pondo = db.Column(db.Integer, nullable=False)
    idadi = db.Column(db.Integer, nullable=False)
    bid_id = db.Column(db.Integer, db.ForeignKey('bidhaa.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

class Mapato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kiasi = db.Column(db.Float, nullable=False)
    aina = db.Column(db.String(255))
    date = db.Column(db.Date, default=date.today())

class Matumizi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kiasi = db.Column(db.Float, nullable=False)
    aina = db.Column(db.String(255))
    date = db.Column(db.Date, default=date.today())

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    employees = db.relationship('User',backref='my_shift',lazy=True) 