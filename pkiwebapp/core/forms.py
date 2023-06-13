from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, ValidationError, SelectField
from wtforms.validators import InputRequired, DataRequired

class SignInForm(FlaskForm):

    email = EmailField("Please provide your Email", validators=[InputRequired("Please input your Email")])
    password = PasswordField("Please Provide your Password", validators=[InputRequired("Please input your password")])
    submit = SubmitField("Submit")

    def validate_password(self, password):
        if str(password.data) != "123":
            raise ValidationError("Wrong Password")
        

# class DialyForm(FlaskForm):

#     selection =

class SelectDay(FlaskForm):

    years = [(str(year), str(year)) for year in range(2013, 2015)] 

    months = [ ('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'), ('04', 'Abril'), ('05', 'Mayo'), ('06', 'Junio'),
        ('07', 'Julio'), ('08', 'Agosto'), ('09', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')]
    days = [(str(day), str(day)) for day in range(1, 32)] 

    year = SelectField('Year', choices=years, validators=[DataRequired()])
    month = SelectField('Month', choices=months, validators=[DataRequired()])
    day = SelectField('Day', choices=days, validators=[DataRequired()])
    cOp = SelectField('C o P', choices=[("C", "Consumo"), ("P", "Producción")], validators=[DataRequired()])
    submit = SubmitField('Buscar')

class SelectDay2(FlaskForm):

    years = [(str(year), str(year)) for year in range(2013, 2015)] 

    months = [ ('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'), ('04', 'Abril'), ('05', 'Mayo'), ('06', 'Junio'),
        ('07', 'Julio'), ('08', 'Agosto'), ('09', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')]
    days = [(str(day), str(day)) for day in range(1, 32)] 

    year = SelectField('Year', choices=years, validators=[DataRequired()])
    year2 = SelectField('Year', choices=years, validators=[DataRequired()])
    month = SelectField('Month', choices=months, validators=[DataRequired()])
    month2 = SelectField('Month', choices=months, validators=[DataRequired()])
    day = SelectField('Day', choices=days, validators=[DataRequired()])
    day2 = SelectField('Day', choices=days, validators=[DataRequired()])
    cOp = SelectField('C o P', choices=[("C", "Consumo"), ("P", "Producción")], validators=[DataRequired()])
    cOp2 = SelectField('C o P', choices=[("C", "Consumo"), ("P", "Producción")], validators=[DataRequired()])
    submit = SubmitField('Buscar')


class CambiarDelay(FlaskForm):

    delays = [("1","1"),("3","3"),("5","5")]
    newDelay = SelectField('Year', choices=delays, validators=[DataRequired()])
    submit = SubmitField('Cambiar')