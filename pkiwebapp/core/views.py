from flask import render_template, Blueprint, redirect, url_for, session
from flask_login import login_required
from pkiwebapp.core.forms import SignInForm, SelectDay, SelectDay2, CambiarDelay
from pkiwebapp.models import Crypto, Tiempo
import plotly.graph_objects as go
from pkiwebapp import db
import pandas as pd
import datetime
import random

core = Blueprint('core', __name__)

#  funcion para generar la grafica desde un query, regresando una grafica en "html"
def genGraph(query, mean=1):
    # la funcion recive un query y un indicador mean, puede ser 1 o 2, para saber si se agruparan las columnas por la media o no
    df = pd.DataFrame(columns=['fecha','intervalo','medida','identificador'])

    # añadimos todos los renglones al dataframe que creamos al principio, poblandolo con los elementos del query con un loop "for"
    for x in query:
        new_rows = pd.DataFrame([[x.fecha, x.intervalo, x.medida, x.identificador]], columns=['fecha','intervalo','medida','identificador'])
        df = pd.concat([df, new_rows], ignore_index=True)

    # convertimos la columa fecha a dormato date time
    df['fecha'] = pd.to_datetime(df['fecha'],dayfirst = True)

    # en caso de que el indicador de mean sea igual a 1, agrupamos la columnas por fecha, es decir agrupamos por dias, ya que puede haber varias medidas en un solo dia
    # tambien calculamos la media para ese dia
    if mean == 1:
        df1 = df.groupby(['fecha']).mean()
    else:
        df1 = df

    # tomamos las columnas de interes del datafrmae
    dates = df1.index
    values = df1["medida"]

    fig = go.Figure() # creamos un plotly figure
    fig.add_trace(go.Scatter(
        x=dates,  # ponemos los valores de X y Y
        y=values,
        mode='lines+markers',
        line=dict(color='black'),  # cambiamos le color de la linea
        marker=dict(
            color='red',  # cambiamos el color de los puntos y otros atributos
            size=6,
            symbol='circle'
        )
    ))

    # cambiamos el aspecta de la grafica como; el color de linea, los titulos de los ejes, el grosor de la linea, etc. 
    fig.update_layout(
        xaxis_title='Tiempo del dia',
        yaxis_title='Valor de Medida',
        xaxis=dict(
            showgrid=False,  # quitamos el las lineas diagrama
            showline=True,
            linecolor='black',  # cambiamos el color de la linea
            linewidth=2,  # cambiamos el grosor de la linea
            zeroline=False,
            tickfont=dict(size=12, family='Arial'),  # elegimos el tipo de la letra y el tamaño
            ticks='outside',
            ticklen=8,
            tickwidth=0
        ),
        yaxis=dict( # repetimos muchas de las cosas que hicimos con el eje X con el eje Y
            showgrid=False,
            showline=True,
            linecolor='black',
            linewidth=2,
            zeroline=False,
            tickfont=dict(size=12, family='Arial'),
            ticks='outside',
            ticklen=8,
            tickwidth=0 
        ),
        plot_bgcolor='rgba(0,0,0,0)', # hacemos el fondo transparente
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, family='Avenir')
    )
    
    if mean == 1:
        fig.update_layout(xaxis_title='Fechas') # en caso de que sea el caso 1 cambiamos el nombre del eje X 

    graph = fig.to_html(full_html=False) # convertimos la grafica a html

    return graph

# esta funcion es muy parecida a la anteriro solo que ahora son 2 querys o una lista de queries para poder combinar las graficas
# tambien recibe los colores los cuales queremos que se utilizen para las lineas
def genGraph2(queries, colors):
    fig = go.Figure()

    for query, color in zip(queries, colors): # hacemos un for embdido para recorrer la lista de los queries
        df = pd.DataFrame(columns=['fecha','intervalo','medida','identificador'])
        for x in query:
            new_rows = pd.DataFrame([[x.fecha, x.intervalo, x.medida, x.identificador]], columns=['fecha','intervalo','medida','identificador'])
            df = pd.concat([df, new_rows], ignore_index=True)

        df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)
        df1 = df

        dates = df1.index
        values = df1["medida"]

        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines',
            line=dict(color=color),
            name=f"Graph {x.fecha}" 
        ))

    fig.update_layout(
        xaxis_title='Tiempo del Dia',
        yaxis_title='Valor de Medidas',
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='black',
            linewidth=2,
            zeroline=False,
            tickfont=dict(size=12, family='Arial'),
            ticks='outside',
            ticklen=8,
            tickwidth=0
        ),
        yaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='black',
            linewidth=2,
            zeroline=False,
            tickfont=dict(size=12, family='Arial'),
            ticks='outside',
            ticklen=8,
            tickwidth=0
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, family='Avenir'),
        legend=dict(
            xanchor='left',
            x=0.05
        )
    )

    graph = fig.to_html(full_html=False)  # Render the plot in HTML

    return graph

# esta es la "funcion" para la pagina de llegada donde le pedimos al ususario su contraseña y correo
@core.route('/', methods=['GET', 'POST'])
def homeview():
    form = SignInForm() # creamos una instancia del formulario
    session["CHECK2"] = 99

    if form.validate_on_submit(): # en caso de que el formulario sea valido a la hora de darle submit
        session.permanent = True
        session["CHECK2"] = random.randint(100,999) # generamos un numero aleatorio de 100 al 999
        return redirect(url_for('core.insideview', check1 = session["CHECK2"])) # redirigimos al usario a la pagina de adentro

    return render_template('home.html', form = form)

@core.route('/inside/<check1>', methods=['GET', 'POST'])
def insideview(check1):
# recibimos el numero aleatorio que se genero anteriormenet, de esta forma validamos que el usario hay aingresado correctamente
    if str(check1) != str(session["CHECK2"]):
        return redirect(url_for("core.homeview"))
    else:
        pass

    return render_template('inside.html')

# en esta vista hacemos un query simple de toda la base de datos
@core.route('/inside/history', methods=['GET', 'POST'])
def historyview():

    query = Crypto.query.all()

    graph = genGraph(query,1) # llamamos a la funcion descrita previamente para generar la grafica en html del query

    return render_template('history.html', graph=graph) # le pasamos la grafica en html el template de html

# esta vista es para ver un dia en especifico
@core.route('/inside/daily', methods=['GET', 'POST'])
def dailyview():

    form = SelectDay() # creamos una instancia del formulario 

    results = " "

    if form.validate_on_submit(): # cuando el usario da submit al formulario
        year = form.year.data # tomamos los valores que ingreso el ususario
        month = form.month.data
        day = form.day.data
        date = f"{year}-{month}-{day}" # creamos la variable fecha y juntamos los "inputs" del usuario

        query = Crypto.query.filter_by(fecha=date, identificador=form.cOp.data).all() # hacemos el query del dia dependiendo los datos que ingreso el usario

        if query == []:
            graph = "No results found" # en caso de que no encuentre algo el query
        else:
            graph = genGraph(query,2)

        return render_template('daily.html', form=form, graph=graph)

    return render_template('daily.html', form=form, graph=results)

# esta vista es muy similar a la anterior, solo que ahora hacemos 2 querys
@core.route('/inside/compare', methods=['GET', 'POST'])
def compareview():

    form = SelectDay2() # creamos una intancia del formulario

    results = " "

    if form.validate_on_submit():
        year = form.year.data
        month = form.month.data
        day = form.day.data
        date = f"{year}-{month}-{day}"
        query = Crypto.query.filter_by(fecha=date, identificador=form.cOp.data).all()

        year2 = form.year2.data
        month2 = form.month2.data
        day2 = form.day2.data
        date2 = f"{year2}-{month2}-{day2}"
        query2 = Crypto.query.filter_by(fecha=date2, identificador=form.cOp2.data).all()

        if query == []: # en caso de que no encuentre algunos de los dos querys
            graph = "No results found on the first query"
        elif query2 == []:
            graph = "No results found on the second query"
        else:
            graph = genGraph2([query,query2],["Red","Black"]) # le pasamos los queries y los colores a la funcion

        return render_template('compare.html', form=form, graph=graph)

    return render_template('compare.html', form=form, graph=results)

# en esta ultima vista simplemente cambiamos el delay a lo que indique el usario
@core.route('/inside/toggle', methods=['GET', 'POST'])
def uploadview():

    form = CambiarDelay()

    test = Tiempo.query.first() #hacemos un query de la bse de datos (solo hay un renglon)
    delay = test.dato

    if form.validate_on_submit():
        test.dato = int(form.newDelay.data) # cambiamos el valor a lo que haya indicado el usario en el formulario
        db.session.commit() # hacmos un commit para que guarden los cambios en la base de datos

        return redirect(url_for('core.uploadview'))

    return render_template('upload.html', form=form, delay=delay)