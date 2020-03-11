from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users

class PostForm(FlaskForm):
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
    title = StringField('Title',
        validators = [
            DataRequired(),
            Length(min=2, max=100)
        ]
    )
    content = TextAreaField('Content',
        validators = [
            DataRequired(),
            Length(min=2, max=1000)
        ]
    )
    submit = SubmitField('Post Content')

class RegistrationForm(FlaskForm):
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
