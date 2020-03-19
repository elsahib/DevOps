from application.models import Users, Players, Stats
# import render_template function from the flask module
from flask import render_template, redirect, url_for, request
# import the app object from the ./application/__init__.py
from application import app, db, bcrypt
# import PostForm from application.forms
from application.forms import StatsForm, RegistrationForm, LoginForm, PlayerForm, UpdateStatsForm, UpdatePlayersForm
# import from Flask_login module
from flask_login import login_user, current_user, logout_user, login_required
# import further forms functionality
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm


# define routes for / & /home, this function will be called when these are accessed
# General site information accessable to everyone
#========== Home Page ============
@app.route('/')
@app.route('/home')
def home():
 playerData = Players.query.all()
 return render_template('home.html', title='Home', posts=playerData)

#========== About Page ============
@app.route('/about')
def about():
    return render_template('about.html', title='About')

########### Players & Stats Management ########
#========== Adding a Player ===================
@app.route('/addplayer', methods=['GET', 'POST'])
@login_required 
def addplayer():
    form = PlayerForm()
    if form.validate_on_submit():
        playerData = Players(player_name = form.player_name.data,player_age = form.player_age.data,player_team =form.player_team.data, author=current_user)
        db.session.add(playerData)
        db.session.commit()
        return redirect(url_for('addplayer'))

    else:
        print(form.errors)

    return render_template('addplayer.html', title='Add A Player', form=form)

#========= Adding Stats =====================
@app.route('/addstats', methods=['GET', 'POST'])
@login_required 
def addstats():

    form = StatsForm()
    if form.validate_on_submit():
        statsData = Stats(goals = form.goals.data,assists = form.assists.data,chances =form.chances.data,shots =form.shots.data,minutes =form.minutes.data,date =form.date.data, stat=form.player_id.data)
        db.session.add(statsData)
        db.session.commit()
        return redirect(url_for('addstats'))

    else:
        print(form.errors)

    return render_template('playerstats.html', title='Add Stats', form=form)

#========= Editing Stats ====================
<<<<<<< HEAD

=======
# @app.route('/editstats', methods=['GET', 'POST'])
# @login_required
# def account():
#     form = UpdateStatsForm()
#     if form.validate_on_submit():
#         current_user.first_name = form.first_name.data
#         current_user.last_name = form.last_name.data
#         current_user.email = form.email.data
#         db.session.commit()
#         return redirect(url_for('home'))
#     elif request.method == 'GET':
#         form.first_name.data = current_user.first_name
#         form.last_name.data = current_user.last_name        
#         form.email.data = current_user.email        
#     return render_template('editstats.html', title='Edit Stats', form=form)
>>>>>>> master
#========= Editing Players ==================

#========= Removing a Player ================

#========= Removing a Stat ==================



########### User Management #################
#========== User Registration Page ===========
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(first_name=form.first_name.data,last_name=form.last_name.data,email=form.email.data, password=hash_pw)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

#========== User Login  ================

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

#========= User Logout =================
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#========= Manage User Account ===============
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name        
        form.email.data = current_user.email        
    return render_template('account.html', title='Account', form=form)

#========= Delete User Account ================
@app.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
    user = current_user.id
    account = Users.query.filter_by(id=user).first()
    players = Players.query.filter_by(player_id=user)
    posts = Stats.query.filter_by(player_id=user)
    for post in posts :
        db.session.delete(post)
    logout_user()
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('register'))