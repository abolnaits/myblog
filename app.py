from datetime import datetime
#Flask
from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

#Formas 
from forms import RegistrationForm,LoginForm


app = Flask(__name__)

#Configuracion
app.config['SECRET_KEY']='a2d836649859da7b3f85c8a843ddfa16'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://webmaster:andres@localhost/myblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Init DB
db = SQLAlchemy(app)

#Clase usuario 
class Usuario(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    image_file = db.Column(db.String(20),unique=True,nullable=False,default='default.jpg')
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
    
        
   
   


posts = [
        {'author':'Andres Benitez','titulo':'Titulo 1','content':'Contenido post 1','date':'Enero 20,2020'},
        {'author':'Leo Orellana','titulo':'Titulo 2','content':'Contenido post 2','date':'Enero 20,2020'},
    ]
@app.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        #print(form.email._value)
        if form.email.data == 'abol@test.com' and form.password.data == '12345':
            flash('Bienvenido {0}!'.format(form.email.data),'success')
            return redirect(url_for('home'))
        else:
            flash('Verique su email/password!','danger')
            #return redirect(url_for('index'))

    return render_template('index.html',form=form,title='Registro')


@app.route('/register',methods=['GET','POST'])
def register():
    #Init form Registration
    form = RegistrationForm()
    #print('Form Registration: ',form)
    if form.validate_on_submit():
        flash('Cuenta registrada para {0}!'.format(form.username.data),'success')
        return redirect(url_for('home'))
    return render_template('register.html',form=form,title='Registro')

@app.route('/home')
def home():
    return render_template('home.html',posts = posts)


@app.route('/about')
def about():
    return render_template('about.html',title='About page')

@app.route('/logout')
def logout():
    return 'Salir'

if __name__ == '__main__':
    app.run(debug=True)