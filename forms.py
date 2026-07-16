from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField, TextAreaField, FloatField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('მომხმარებელი', validators=[DataRequired(), Length(min=3, max=16)])
    password = PasswordField('პაროლი', validators=[DataRequired(), Length(min=8, max=16)])
    repeat_password = PasswordField('გაიმეორე პაროლი', validators=[EqualTo('password')])
    birthday = DateField('დაბადების თარიღი', validators=[DataRequired()])
    gender = RadioField('სქესი', choices=[('Male', 'Male'), ('Female', 'Female')])
    submit = SubmitField('რეგისტრაცია')

class LoginForm(FlaskForm):
    username = StringField('მომხმარებელი', validators=[DataRequired()])
    password = PasswordField('პაროლი', validators=[DataRequired()])
    submit = SubmitField('შესვლა')

class AddComponentForm(FlaskForm):
    title = StringField('ნივთის სახელი', validators=[DataRequired()])
    cost = FloatField('ფასი ($)', validators=[DataRequired()])
    info = TextAreaField('აღწერა', validators=[DataRequired()])
    image = FileField('სურათის ატვირთვა', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('დამატება')
