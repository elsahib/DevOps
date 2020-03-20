from application.models import Users, Players, Stats
# import render_template function from the flask module
from flask import render_template, redirect, url_for, request
# import the app object from the ./application/__init__.py
from application import app, db, bcrypt
# import PostForm from application.forms
from application.forms import StatsForm, RegistrationForm, LoginForm, PlayerForm, UpdateForm, UpdatePlayer
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
    playerData = db.session.query(Players).all()
    return render_template('home.html', title='Home', posts=playerData)

#========== About Page ============
@app.route('/about')
def about():
    return render_template('about.html', title='About')

########### Players & Stats Management ######
#========== Adding a Player =================
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

#========= View Stats =======================
@app.route('/view')
@login_required
def view():
    statdata = db.session.query(Players, Stats).select_from(db.join(Stats, Players)).filter(Stats.player_id == Players.player_id)\
        .filter(Players.id == current_user.id).all()
    return render_template('view.html', title='View Stats', stats=statdata)

#========= Edit Stats  ======================
@app.route('/editstats/<player_id>', methods=['GET', 'POST'])
@login_required
def editstats(player_id):
    current_record = db.session.query(Players, Stats).select_from(db.join(Stats, Players))\
        .filter(Players.player_id== player_id).filter(Stats.player_id == Players.player_id).first()
    form = UpdateForm()
    if form.validate_on_submit():
        current_record.Stats.goals = form.goals.data
        current_record.Stats.assists = form.assists.data
        current_record.Stats.chances = form.chances.data
        current_record.Stats.shots = form.shots.data
        current_record.Stats.minutes = form.minutes.data
        current_record.Stats.date = form.date.data
        db.session.commit()
        return redirect(url_for('view'))
    elif request.method=='GET':
        form.goals.data = current_record.Stats.goals 
        form.assists.data = current_record.Stats.assists
        form.chances.data = current_record.Stats.chances
        form.shots.data = current_record.Stats.shots
        form.minutes.data = current_record.Stats.minutes
        form.date.data = current_record.Stats.date
    return render_template('editstats.html', title='Edit Stats Data', form=form, current= current_record)

#========= remove stats =====================
@app.route('/deletestats/<stat_id>')
@login_required
def deletestats(stat_id):
    db.session.query(Stats).filter_by(stat_id = stat_id).delete(synchronize_session=False)
    db.session.commit()
    return redirect(url_for('view'))

#========= View players =======================
@app.route('/vplayers')
@login_required
def vplayers():
    playerdata = db.session.query(Players).select_from(Players).filter_by(id = current_user.id).all()
    return render_template('vplayers.html', title='View Players', players=playerdata)

#========= Edit players  ======================
@app.route('/editplayer/<player_id>', methods=['GET', 'POST'])
@login_required
def editplayer(player_id):
    current_record = db.session.query(Players).select_from(Players).filter(player_id == player_id).first()
    form = UpdatePlayer()
    if form.validate_on_submit():
        current_record.player_name = form.player_name.data
        current_record.player_age = form.player_age.data
        current_record.player_team = form.player_team.data
        db.session.commit()
        return redirect(url_for('vplayers'))
    elif request.method=='GET':
        form.player_name.data = current_record.player_name
        form.player_age.data = current_record.player_age
        form.player_team.data = current_record.player_team

    return render_template('editplayer.html', title='Edit Player Data', form=form )

#========= remove players =====================
@app.route('/deleteplayer/<player_id>')
@login_required
def deleteplayer(player_id):
    stats = db.session.query(Stats).select_from(Stats).filter_by( player_id = player_id).all()
    for stat in stats:
        db.session.delete(stat)
    db.session.query(Players).filter_by(player_id = player_id).delete(synchronize_session=False)
    db.session.commit()
    return redirect(url_for('vplayers'))


########### User Management ##################
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

#========== User Login  ======================
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

#========= User Logout =======================
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
    players = Players.query.filter_by(id=user)
    for player in players :
        stats = db.session.query(Stats).select_from(Stats).filter_by( player_id = player.player_id).all()
        # stat_counter = db.session.query(Stats).filter(player_id=player.player_id).count()     
        for stat in stats :
            db.session.delete(stat)
        db.session.delete(player)
    logout_user()
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('register'))
    # stats = db.session.query(Stats).select_from(Stats).filter(Stats.player_id == players.player_id)
    # stats = 

# #====== last version on github =========================
# @app.route("/account/delete", methods=["GET", "POST"])
# @login_required
# def account_delete():
#     user = current_user.id
#     account = Users.query.filter_by(id=user).first()
#     players = Players.query.filter_by(player_id=user)
#     posts = Stats.query.filter_by(player_id=user)
#     for post in posts :
#         db.session.delete(post)
#     logout_user()
#     db.session.delete(account)
#     db.session.commit()
#     return redirect(url_for('register'))