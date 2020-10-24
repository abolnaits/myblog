#Package

#Init app
from datetime import datetime
#Flask
from flask import Flask
#SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
#Bcrypt
from flask_bcrypt import Bcrypt

#Export later in routes.py
app = Flask(__name__)

#Configuracion
app.config['SECRET_KEY']='a2d836649859da7b3f85c8a843ddfa16'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://webmaster:andres@localhost/myblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Init DB , export later un models.py
db = SQLAlchemy(app)
#Init Bcrypt
bcrypt = Bcrypt(app)

#Routes
from app import routes