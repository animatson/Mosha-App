from Bakery.factory import db, login_manager
from flask_login import UserMixin
from datetime import datetime, date
from sqlalchemy import Boolean, text

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    is_active = db.Column(Boolean, nullable=False, server_default=text('FALSE'))  # default False
    position_as = db.Column(db.String(150), nullable=True)
    phone_no = db.Column(db.String(20), nullable=False, server_default="0000000000")  # string with default
    password = db.Column(db.String(150), nullable=False)
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id', name='fk_user_shift_id'), nullable=True)

    manunuzi = db.relationship('ManunuziData', backref='buyer', lazy=True)
    mauzo = db.relationship('Mauzo', backref='seller', lazy=True)
    mpishi = db.relationship('Mpishi', backref='cooker', lazy=True)
    store = db.relationship('Store', backref='storekeeper', lazy=True)

class ManunuziData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)  # pass function, not call it
    maligafi = db.Column(db.String(150), nullable=False)
    unit = db.Column(db.String(50), nullable=True)
    idadi = db.Column(db.Integer, nullable=False)
    bei = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_manunuzi_user_id'), nullable=False)

class Bidhaa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    b_name = db.Column(db.String(100), nullable=False, unique=True)
    b_bei = db.Column(db.Integer, nullable=False)
    uzal = db.relationship('Uzalishaji', backref='bid', lazy=True)
    mauzo = db.relationship('Mauzo', backref='bid', lazy=True)
    madeni = db.relationship('Madeni', backref='bid', lazy=True)
    mpishi = db.relationship('Mpishi', backref='bid', lazy=True)

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    maligafi = db.Column(db.String(50), nullable=False)
    units = db.Column(db.String(50), nullable=True)
    idadi = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_store_user_id'), nullable=False)

class Madeni(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    kiasi_kalipa = db.Column(db.Integer, nullable=False)
    kiasi_baki = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)  # changed to string for phone numbers
    date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Integer, default=1)
    bid_id = db.Column(db.Integer, db.ForeignKey('bidhaa.id', name='fk_madeni_bid_id'), nullable=False)

class Uzalishaji(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    b_jumla = db.Column(db.Integer, nullable=False)
    bid_id = db.Column(db.Integer, db.ForeignKey('bidhaa.id', name='fk_uzalishaji_bid_id'), nullable=False)

class Mauzo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=date.today)
    b_uza = db.Column(db.Integer, nullable=True, default=0)
    b_bei_uza = db.Column(db.Integer, nullable=True, default=0)
    jumla = db.Column(db.Integer, nullable=True, default=0)
    bid_id = db.Column(db.Integer, db.ForeignKey('bidhaa.id', name='fk_mauzo_bid_id'), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_mauzo_user_id'), nullable=False)

class Mpishi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=date.today)
    pondo = db.Column(db.Integer, nullable=False)
    idadi = db.Column(db.Integer, nullable=False)
    bid_id = db.Column(db.Integer, db.ForeignKey('bidhaa.id', name='fk_mpishi_bid_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_mpishi_user_id'), nullable=False)

class Mapato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kiasi = db.Column(db.Float, nullable=False)
    aina = db.Column(db.String(255))
    date = db.Column(db.Date, default=date.today)

class Matumizi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kiasi = db.Column(db.Float, nullable=False)
    aina = db.Column(db.String(255))
    date = db.Column(db.Date, default=date.today)

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    employees = db.relationship('Users', backref='my_shift', lazy=True)
