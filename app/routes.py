#Application for routes
from app import app,bcrypt,db
from flask import request
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect

#Formas 
from app.forms import RegistrationForm,LoginForm,UpdateProfileForm
#Modelos
from app.models import Usuario,Post
#Login manager
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from flask_login import login_required


posts = [
        {'author':'Andres Benitez','titulo':'Titulo 1','content':'Contenido post 1','date':'Enero 20,2020'},
        {'author':'Leo Orellana','titulo':'Titulo 2','content':'Contenido post 2','date':'Enero 20,2020'},
    ]

#Login
@app.route('/',methods=['GET','POST'])
def index():
     #Si el usuario esta autentificado
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        #Obtengo el usuario mediante el email
        user = Usuario.query.filter_by(email=form.email.data).first()
        print('User ==> ',user)
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            #Get the next 
            next_page = request.args.get('next')
            flash('Bienvenido al sistema','success')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash('Verique su email/password!','danger')
            #return redirect(url_for('index'))

    return render_template('index.html',form=form,title='Registro')


'''
Registro de un nuevo usuario 
Usamos Bcrypt para encriptar 
'''
@app.route('/register',methods=['GET','POST'])
def register():

    #Si el usuario esta autentificado
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    #Init form Registration
    form = RegistrationForm()
    #print('Form Registration: ',form)
    if form.validate_on_submit():
        hashed_pasword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Usuario(username=form.username.data,email=form.email.data,password=hashed_pasword)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Cuenta registrada para {0}!'.format(form.username.data),'success')
        except Exception as e:
            #print(e)
            flash('No se puedo registrar la cuenta para {0}!'.format(form.username.data),'danger')
        
        return redirect(url_for('home'))
    return render_template('register.html',form=form,title='Registro')


@app.route('/home')
@login_required
def home():
    return render_template('home.html',posts = posts)

#Perfil del usuario
@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        #Update current user
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Perfil actualizado','warning')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        #Populate the form with the current user data
            form.username.data = current_user.username
            form.email.data = current_user.email
                   
    image_file = url_for('static',filename='img/'+current_user.image_file)
    return render_template('account.html',title='Account page',image_file=image_file,form=form)

#Salir del sistema
@app.route('/logout')
#@login_required
def logout():
    #print(current_user.is_authenticated)
    if current_user.is_authenticated:
        logout_user()
        flash('Sesion terminada','danger')
    
    return redirect(url_for('index')) 
        
    
    
