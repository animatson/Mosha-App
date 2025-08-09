from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField, ValidationError,SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, InputRequired
from Bakery.database import User

class LoginForm(FlaskForm):
    email = StringField('Email (Barua Pepe)', validators=[DataRequired(), Email()])
    password = PasswordField('Password (Nenosiri)', validators=[DataRequired()])
    remember = BooleanField('Remember Me ')
    submit = SubmitField('Login ')



class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    position = SelectField('Nafasi Kazini',choices=['Manunuzi', 'Mauzo', 'Mpishi','Store',''])
    phone = IntegerField('Namba za Simu',validators=[InputRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                      validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is Already registered")
class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')