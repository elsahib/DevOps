from application.models import Posts, Users
# import render_template function from the flask module
from flask import render_template, redirect, url_for, request
# import the app object from the ./application/__init__.py
from application import app, db, bcrypt
# import PostForm from application.forms
from application.forms import PostForm, RegistrationForm, LoginForm
# import from Flask_login module
from flask_login import login_user, current_user, logout_user, login_required
# define routes for / & /home, this function will be called when these are accessed
@app.route('/')
@app.route('/home')
@login_required 
def home():
 postData = Posts.query.all()
 return render_template('home.html', title='Home', posts=postData)
 
@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)

        user = Users(email=form.email.data, password=hash_pw)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('post'))
    return render_template('register.html', title='Register', form=form)

@app.route('/posts', methods=['GET', 'POST'])
@login_required 
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            title = form.title.data,
            content = form.content.data
        )

        db.session.add(postData)
        db.session.commit()

        return redirect(url_for('home'))

    else:
        print(form.errors)

    return render_template('posts.html', title='Post', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))