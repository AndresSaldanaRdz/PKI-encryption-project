from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, ValidationError
from wtforms.validators import InputRequired

class SignInForm(FlaskForm):

    email = EmailField("Please provide your Email", validators=[InputRequired("Please input your Email")])
    password = PasswordField("Please Provide your Password", validators=[InputRequired("Please input your password")])
    submit = SubmitField("Submit")

    def validate_password(self, password):
        if str(password.data) != "123":
            raise ValidationError("Wrong Password")