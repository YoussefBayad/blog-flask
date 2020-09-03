from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm 
from wtforms import StringField , PasswordField, SubmitField ,BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length ,Email , EqualTo, ValidationError
from blog.moduls import User


class RegistrationForm(FlaskForm):
    username = StringField("username", validators=[ DataRequired(),Length(min = 2, max= 20)])
    email = StringField("Email", validators=[DataRequired(), Email("Please enter your email address.")])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    sign_up = SubmitField("sign up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Username already exist')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already exist')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    login = SubmitField("Login")
    

class UpdateAccountForm(FlaskForm):
    username = StringField("username", validators=[ DataRequired(),Length(min = 2, max= 20)])
    email = StringField("Email", validators=[DataRequired(), Email("Please enter your email address.")])
    picture = FileField("Update profile picture", validators=[FileAllowed(['jpg', 'png'])])
    password = PasswordField('Password',)
    confirm_password = PasswordField("Confirm Password", validators=[EqualTo("password")])
    sign_up = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exist')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exist')


class NewPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=25)])
    content = TextAreaField("What is on your Mind ?" , validators=[DataRequired()])
    submit = SubmitField("Post", validators=[DataRequired()])
