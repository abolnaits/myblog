#Application for routes
from app import app

from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect

#Formas 
from app.forms import RegistrationForm,LoginForm
#Modelos
from app.models import Usuario,Post


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