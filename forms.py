from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignUpForm(FlaskForm):
    nickname = StringField('მომხმარებელი', validators=[DataRequired(), Length(min=3, max=15)])
    email_address = StringField('ფოსტა', validators=[DataRequired(), Email()])
    secure_password = PasswordField('პაროლი', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('ექაუნთის შექმნა')

class SignInForm(FlaskForm):
    email_address = StringField('ფოსტა', validators=[DataRequired(), Email()])
    secure_password = PasswordField('პაროლი', validators=[DataRequired()])
    submit = SubmitField('შესვლა')

