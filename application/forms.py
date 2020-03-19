from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users, Players, Stats
from flask_login import current_user
from wtforms.ext.sqlalchemy.fields import QuerySelectField

#============= Players Management Forms =======================
#================== Add New Player Form =======================
class PlayerForm(FlaskForm):
    
    player_name = StringField('Player Full Name',
        validators = [
            DataRequired(),
            Length(min=2, max=100)
        ]
    )
    player_age = StringField('Player Age',
        validators = [
            DataRequired(),
            Length(min=1, max=3)
        ]
    )
    player_team = StringField('Player Team',
        validators = [
            DataRequired(),
            Length(min=2, max=100)
        ]
    )
    submit = SubmitField('Add Player')

#============= Add Stats to a Player Form =======================
class StatsForm(FlaskForm):
   
    player_id = QuerySelectField(
        'Choose a Player',
        query_factory=lambda: Players.query.filter_by(id=current_user.id),
        allow_blank=False
    )
    
    goals = StringField('Goals',
        validators = [
            DataRequired(),
            Length(min=1, max=2)
        ]
    )
    assists = StringField('Assists',
        validators = [
            DataRequired(),
            Length(min=1, max=3)
        ]
    )
    chances = StringField('Chances',
        validators = [
            DataRequired(),
            Length(min=1, max=3)
        ]
    )

    shots = StringField('Shots',
        validators = [
            DataRequired(),
            Length(min=1, max=3)
        ]
    )
    minutes = StringField('Minutes Played',
        validators = [
            DataRequired(),
            Length(min=1, max=3)
        ]
    )
    date = DateField('Enter Date(dd-mm-yy)',
            format="%d-%m-%Y")
        
    
    submit = SubmitField('Add Stats')


#============= Update Players Form =======================

class UpdatePlayersForm(FlaskForm):
    first_name = StringField('First Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    last_name = StringField('Last Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ])
    submit = SubmitField('Update')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use')


#============= Update Stats Form =======================

class UpdateStatsForm(FlaskForm):

    player_name = StringField('Player Full Name',
        validators = [
            DataRequired(),
            Length(min=2, max=100)
        ]
    )
    
    goals = StringField('Goals',
        validators = [
            DataRequired(),
            Length(min=1, max=2)
        ]
    )
    assists = StringField('Assists',
        validators = [
            DataRequired(),
            Length(min=1, max=3)
        ]
    )
    chances = StringField('Chances',
        validators = [
            DataRequired(),
            Length(min=1, max=3)
        ]
    )

    shots = StringField('Shots',
        validators = [
            DataRequired(),
            Length(min=1, max=3)
        ]
    )
    minutes = StringField('Minutes Played',
        validators = [
            DataRequired(),
            Length(min=1, max=3)
        ]
    )
    date = DateField('Enter Date(dd-mm-yy)',
            format="%d-%m-%Y")
        
    
    submit = SubmitField('Update Stats')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use')

#============= Users Management Forms =======================

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',
        validators = [
            DataRequired(),
            Length(min=2, max=30)
        ]
    )
    last_name = StringField('Last Name',
        validators = [
            DataRequired(),
            Length(min=2, max=30)
        ]
    )
    email = StringField('Email',
        validators = [
            DataRequired(),
            Email(message='Please Input a valid Email Address')
        ]
    )
    password = PasswordField('Password',
        validators = [
            DataRequired(message='Passwords can not be empty'), 
        ]
    )
    confirm_password = PasswordField('Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already in use')


class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField('Password',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    last_name = StringField('Last Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ])
    submit = SubmitField('Update')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use')