from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .forms import RegistrationForm, LoginForm  # Assuming forms.py contains the form definitions
from Bakery.database import Users
from Bakery.factory import db,bcrypt
from flask_login import login_required, login_user, logout_user, current_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data) and user.is_active:
             login_user(user,remember=form.remember.data)
             #next = request.args.get('next')

             if user.id == 1 or user.id == 2:
                 session['user_id'] = user.id
                 flash("Login Successfully",'info')
                 return redirect(url_for('users.boss'))
             elif user.position_as == 'Manunuzi':
                 session['position_as'] = "Manunuzi"
                 session['user'] = user.id
                 flash("Login Successfully",'info')
                 return redirect(url_for('users.manunuzi'))
             elif user.position_as == 'Mpishi':
                 session['position_as'] = "Mpishi"
                 session['user_id'] = user.id
                 flash("Login Successfully",'info')
                 return redirect(url_for('users.mpishi'))
             elif user.position_as == 'Mauzo':
                 session['position_as'] = "Mauzo"
                 session['user_id'] = user.id
                 flash("Login Successfully",'info') 
                 return redirect(url_for('users.mauzo'))
             elif user.position_as == 'Store':
                 session['position_as'] = "Store"
                 session['user_id'] = user.id
                 flash("Login Successfully",'info') 
                 return redirect(url_for('users.store'))
             else:
                 flash("You are not allowed to access this page",'warning')
                 return redirect(url_for('auth.index'))
        else:
            flash("Login Unsuccessfully check Email and Password Or Maybe Deactivated",'warning')
    return render_template('login.html', title="login",form=form)
    

@auth_bp.route('/registerUser',methods=['GET','POST'])
def registerUser():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_passwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(name=form.username.data,email=form.email.data,is_active=True,position_as=form.position.data,phone_no=form.phone.data,password=hash_passwd)
        db.session.add(user)
        db.session.commit()
        flash("User is successfully registered",'primary')
        return redirect(url_for('users.user_status'))
    return render_template('registration.html', form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout Successfully",'info')
    return redirect(url_for('auth.index'))


            
