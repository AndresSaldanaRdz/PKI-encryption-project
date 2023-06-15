from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, ValidationError, SelectField
from wtforms.validators import InputRequired, DataRequired

#  en este archivo estan declarados todos los formularios que se usan en las diferentes vistas, osea informacion que le pedimos al cliente

#  este formulario es es del vista de entrada, asi que pedimos al usario un correo y una contraseña, luego verificamos que esat contrasela
#  sea la correcta, en caso de que si sea los dejamos entrar al sitio
class SignInForm(FlaskForm):

    email = EmailField("Please provide your Email", validators=[InputRequired("Please input your Email")])
    password = PasswordField("Please Provide your Password", validators=[InputRequired("Please input your password")])
    submit = SubmitField("Submit")

    def validate_password(self, password):
        if str(password.data) != "123":
            raise ValidationError("Wrong Password")

#  en este formulario le pedimos al usario un año, un mes y un dia, aparte que seleccine entre consumo o produccion
#  como utilizamos "SelectField" limitamos al usario en las opciones que tiene para eligir
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

#  este formulario es muy similar al enterior solo que pedimos dos veces la misma informacion para poder poder crear la grafica con las dos lineas
#  cabe mencionar que todos los formularios tiene un boton de "submit" para conectar las acciones de presionar un boton y validar el formulario
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

#  es el ultimo formulario en el que le damos al usario la eleccion del tiempo de delay, muy parecido a los demas
# en todos los campos que consideramos que la eleccion del usario es indispensable añadimos el validador "data required"
class CambiarDelay(FlaskForm):

    delays = [("1","1"),("3","3"),("5","5")]
    newDelay = SelectField('Year', choices=delays, validators=[DataRequired()])
    submit = SubmitField('Cambiar')