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

    return render_template('inside.html')

@core.route('/inside/history', methods=['GET', 'POST'])
def historyview():

    query = Crypto.query.all()

    df = pd.DataFrame(columns=['fecha','intervalo','medida','identificador'])

    for x in query:
        new_rows = pd.DataFrame([[x.fecha, x.intervalo, x.medida, x.identificador]], columns=['fecha','intervalo','medida','identificador'])
        # Append new rows
        df = pd.concat([df, new_rows], ignore_index=True)

    df['fecha'] = pd.to_datetime(df['fecha'],dayfirst = True)
    df1 = df.groupby(['fecha']).mean()

    dates = df1.index
    values = df1["medida"]

    fig = go.Figure() # Create the plotly figure
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines+markers',
        line=dict(color='black'),  # Change the line color
        marker=dict(
            color='red',  # Change the plot points color
            size=6,  # Set the size of the plot points
            symbol='circle'  # Set the symbol of the plot points
        )
    ))
    # Customize the graph
    fig.update_layout(
        xaxis_title='Fecha',  # Set the x-axis label
        yaxis_title='Promedio de medidas diaria',  # Set the y-axis label
        xaxis=dict(
            showgrid=False,  # Remove x-axis grid lines
            showline=True,  # Show x-axis line
            linecolor='black',  # Set x-axis line color
            linewidth=2,  # Set x-axis line thickness
            zeroline=False,  # Remove x-axis zero line
            tickfont=dict(size=12, family='Arial'),  # Customize x-axis tick labels font
            ticks='outside',  # Set x-axis ticks outside the plot
            ticklen=8,  # Set length of the x-axis ticks
            tickwidth=0  # Remove separation lines between axis line and tick labels
        ),
        yaxis=dict(
            showgrid=False,  # Remove y-axis grid lines
            showline=True,  # Show y-axis line
            linecolor='black',  # Set y-axis line color
            linewidth=2,  # Set y-axis line thickness
            zeroline=False,  # Remove y-axis zero line
            tickfont=dict(size=12, family='Arial'),  # Customize y-axis tick labels font
            ticks='outside',  # Set y-axis ticks outside the plot
            ticklen=8,  # Set length of the y-axis ticks
            tickwidth=0  # Remove separation lines between axis line and tick labels
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Set the plot background color
        paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background color
        font=dict(size=12, family='Avenir')  # Customize the font of the graph
    )
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

    test = Crypto.query.all()
    for x in test:
        print(x)

    return render_template('upload.html')