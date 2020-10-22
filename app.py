from flask import Flask
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
#Formas 
from forms import RegistrationForm,LoginForm
app = Flask(__name__)

#Configuracion
app.config['SECRET_KEY']='a2d836649859da7b3f85c8a843ddfa16'

posts = [
        {'author':'Andres Benitez','titulo':'Titulo 1','content':'Contenido post 1','date':'Enero 20,2020'},
        {'author':'Leo Orellana','titulo':'Titulo 2','content':'Contenido post 2','date':'Enero 20,2020'},
    ]
@app.route('/')
def index():
    form = RegistrationForm()
    return render_template('index.html',form=form,title='Registro')


@app.route('/register',methods=['GET','POST'])
def register():
    #Init form Registration
    form = RegistrationForm()
    print('Form Registration: ',form)
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