#Application for routes
from app import app,bcrypt,db
from flask import request
from flask import render_template
from flask import url_for
from flask import flash
from flask import redirect
from flask import abort
#Formas 
from app.forms import RegistrationForm,LoginForm,UpdateProfileForm
from app.forms import PostForm
#Modelos
from app.models import Usuario,Post
#Login manager
from flask_login import login_user
from flask_login import current_user
from flask_login import logout_user
from flask_login import login_required
#Save image
import secrets
import os 
#Pillow to manipulate images
from PIL import Image

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

'''
Get all the post from the DB
Those posts will be paginated
'''
@app.route('/home')
@login_required
def home():
    #Get the page GET value
    page = request.args.get('page',1,type=int)
    #Get all posts
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5,page=page)
    

    return render_template('home.html',posts = posts)

#Perfil del usuario
@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        #If there is a new profile pic
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
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


#Create new post
@app.route('/post/add',methods=['GET','POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        try:
            db.session.add(post)
            db.session.commit()
            flash('Post agregado','success')
        except Exception as e:
            flash('No se pudo agregar post','danger')
            #print(e)
        
        return redirect(url_for('home'))
    return render_template('add_post.html',title='Create post',form=form)

@app.route('/post/<int:post_id>')
def post(post_id):
    #Get the post by id
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)

#Update post
@app.route('/post/update/<int:post_id>',methods=['GET','POST'])
@login_required
def update_post(post_id):
    print('Update post ==> ',post_id)
    #Get the post 
    post = Post.query.get_or_404(post_id)
    #print('Post ==> ',post)
    #Chek if the user is the person who wrote the post
    if post.author != current_user:
        #print('Abort')
        abort(403)

    form = PostForm()
    #Populate the form
    form.title.data = post.title
    form.content.data = post.content

    if request.method == 'POST':
        #Validar, lleno la forma con los datos del form
        form = PostForm(request.form)
        if form.validate():
            post.title = form.title.data
            post.content = form.content.data
            print('Title ==> ',form.title.data)
            print('Content ==> ',form.content.data)
            try:
            #db.session.add(post)
                print('Post data ==> ',post)
                db.session.commit()
                flash('Post modificado','success')
            except Exception as e:
                flash('No se pudo modificar post','danger')
                print(e)
            
            return redirect(url_for('post',post_id = post.id))
        else:
            return render_template('update_post.html',title='Update post',form=form)

    else:
        print('Mostrar post update')
        return render_template('update_post.html',title='Update post',form=form)

#Delete post from DB
@app.route('/del_post/<int:post_id>',methods=['POST'])
def del_post(post_id):
    #Get post by id
    post = Post.query.get_or_404(post_id)
    #Check the author
    if post.author != current_user:
        abort(403)

    try:
        db.session.delete(post)
        db.session.commit()
        flash('Post eliminado','danger')
    except Exception as e:
        flash('No se pudo eliminar post','danger')
    return redirect(url_for('home'))
    return '{0}'.format(post_id)

#Show all post by author
@app.route('/user/<string:username>',methods=['GET'])
def user_posts(username):
    #Get the page variable GET
    page = request.args.get('page',1,type=int)
    #Get the user by this username
    user = Usuario.query.filter_by(username=username).first_or_404()
    #Filter post by username
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
    return render_template('user_posts.html',posts = posts,user=user)

#Salir del sistema
@app.route('/logout')
#@login_required
def logout():
    #print(current_user.is_authenticated)
    if current_user.is_authenticated:
        logout_user()
        flash('Sesion terminada','danger')
    
    return redirect(url_for('index')) 

        
#   
#Functions
#

#Save the new profile pic
#Copy the form_picture into the server
#form_picture : form.picture.data, type: FileStorage

def save_picture(form_picture):
    #print(type(form_picture))
    random_hex = secrets.token_hex(8)
    #Get the extension
    _, f_ext = os.path.splitext(form_picture.filename)
    #print('Ext ==> ',f_ext)
    #print('Name ==> ',random_hex)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/img',picture_fn)
    #Resize the image with Pillow
    output_size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    #form_picture.save(picture_path)
    #print('Path img ==> ',picture_path)
    #Return the string of the file
    return picture_fn

