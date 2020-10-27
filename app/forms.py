from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import Email
from wtforms.validators import EqualTo
#Errores de validacion
from wtforms import ValidationError

#Modelos usados para las validaciones contra el usuario
from app.models import Usuario

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Registrar')

    #Validacion para el username
    def validate_username(self,username):
        #Verifico si hay un usuario con ese username
        user = Usuario.query.filter_by(username=username.data).first()
        #print(user)
        if user:
            raise ValidationError('El usuario ya esta registrado')

    #Validacion para el email
    def validate_email(self,email):
        #Verifico si hay un usuario con ese username
        user = Usuario.query.filter_by(email=email.data).first()
        #print(user)
        if user:
            raise ValidationError('El email ya esta registrado')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')