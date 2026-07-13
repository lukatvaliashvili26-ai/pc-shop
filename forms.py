from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField("enter username",
                           validators=[DataRequired(message="username is required"),
                                       Length(min=8, max=16,
                                              message="the name must be between 8 and 16 characters long")])

    password = PasswordField("enter password",
                             validators=[DataRequired(message="username is required"),
                                         Length(min=8, max=16,
                                                message="the password must be between 8 and 16 characters long")])

    repeat_password = PasswordField("repeat password",
                                    validators=[EqualTo("password", message="passwords must be same")])

    birthday = DateField("mark your date of birth",
                         validators=[DataRequired(message="birthday data selection is required")])

    gender = RadioField("choose gender",
                        validators=[DataRequired(message="Gender selection is required")],
                        choices=["Male", "Female"])
    comment = TextAreaField("your comment")
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("enter username",
                           validators=[DataRequired(message="username is required"),
                                       Length(min=8, max=16,
                                              message="the name must be between 8 and 16 characters long")])

    password = PasswordField("enter password",
                             validators=[DataRequired(message="password is required"),
                                         Length(min=8, max=16,
                                                message="the password must be between 8 and 16 characters long")])

    submit = SubmitField("log in")

