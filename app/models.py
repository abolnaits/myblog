from datetime import datetime
from app import db
from app import login_manager
#Requerido para las validacion
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

#Clase usuario 
class Usuario(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),unique=False,nullable=False,default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

    #Print the objeto
    def __repr__(self):
        return 'User ==> {0} {1} {2}'.format(self.id,self.username,self.email)
    

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.Text,nullable=False)
    #ForeignKey
    user_id = db.Column(db.Integer,db.ForeignKey('usuario.id'),nullable=False)

     #Print the objeto
    def __repr__(self):
        return 'Post ==> {0} {1} {2}'.format(self.id,self.title,self.date_posted)
    
        
   