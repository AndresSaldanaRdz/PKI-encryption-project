from flask import render_template, Blueprint, redirect, url_for, session
from flask_login import login_required
from pkiwebapp.core.forms import SignInForm 
from pkiwebapp.models import Crypto, Tiempo
import plotly.graph_objects as go
from pkiwebapp import db
import pandas as pd
import datetime
import random 

core = Blueprint('core', __name__)

@core.route('/', methods=['GET', 'POST'])
def homeview():
    form = SignInForm()
    session["CHECK2"] = 99

    if form.validate_on_submit():
        session.permanent = True
        session["CHECK2"] = random.randint(100,999)
        return redirect(url_for('core.insideview', check1 = session["CHECK2"]))

    return render_template('home.html', form = form)

@core.route('/inside/<check1>', methods=['GET', 'POST'])
def insideview(check1):

    if str(check1) != str(session["CHECK2"]):
        return redirect(url_for("core.homeview"))
    else:
        pass

    #new_record = Crypto(fecha=datetime.date.today(), intervalo=1, medida=4.7, identificador='P')
    #db.session.add(new_record)
    #db.session.commit()

    return render_template('inside.html')

@core.route('/inside/history', methods=['GET', 'POST'])
def historyview():

    df = pd.read_csv("/Users/andressaldana/Documents/GitHub/PKI-encryption-project/pkiwebapp/Test.csv")

    df['Fecha'] = pd.to_datetime(df['Fecha'],dayfirst = True)
    df1 = df.groupby(['Fecha']).mean()

    dates = df1.index
    values = df1["Medida"]

    fig = go.Figure() # Create the plotly figure
    fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers'))
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Medidas') # Set x-axis and y-axis labels
    graph = fig.to_html(full_html=False) # Render the plot in HTML

    return render_template('history.html', graph=graph)

@core.route('/inside/daily', methods=['GET', 'POST'])
def dailyview():

    results = Crypto.query.all()
    for result in results:
        print(result.id)

    #SUBIR LA BASE DE DATOS

    return render_template('daily.html', graph=results)

@core.route('/inside/compare', methods=['GET', 'POST'])
def compareview():

    df = pd.read_csv("/Users/andressaldana/Documents/GitHub/PKI-encryption-project/pkiwebapp/Test.csv")
    #df['Fecha'] = pd.to_datetime(df['Fecha'])

    dates = df["Fecha"]
    #values = df.groupby('Fecha')['Medida'].mean().reset_index()
    values = df["Medida"]

    fig = go.Figure() # Create the plotly figure
    fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers'))
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Medidas') # Set x-axis and y-axis labels
    graph = fig.to_html(full_html=False) # Render the plot in HTML

    return render_template('compare.html', graph=graph)

@core.route('/inside/upload_csv', methods=['GET', 'POST'])
def uploadview():

    #new_record = Tiempo(dato=3)
    #db.session.add(new_record)
    #db.session.commit()

    test = Tiempo.query.first()
    print(test.dato)

    return render_template('upload.html')