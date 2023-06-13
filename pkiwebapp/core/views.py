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

def genGraph(query, mean=1):
    df = pd.DataFrame(columns=['fecha','intervalo','medida','identificador'])

    for x in query:
        new_rows = pd.DataFrame([[x.fecha, x.intervalo, x.medida, x.identificador]], columns=['fecha','intervalo','medida','identificador'])
        # Append new rows
        df = pd.concat([df, new_rows], ignore_index=True)

    df['fecha'] = pd.to_datetime(df['fecha'],dayfirst = True)
    if mean == 1:
        df1 = df.groupby(['fecha']).mean()
    else:
        df1 = df

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
        xaxis_title='Tiempo del dia',  # Set the x-axis label
        yaxis_title='Valor de Medida',  # Set the y-axis label
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
    
    if mean == 1:
        fig.update_layout(xaxis_title='Fechas')

    graph = fig.to_html(full_html=False) # Render the plot in HTML

    return graph

def genGraph2(queries, colors):
    fig = go.Figure()  # Create the plotly figure

    for query, color in zip(queries, colors):
        df = pd.DataFrame(columns=['fecha','intervalo','medida','identificador'])
        for x in query:
            new_rows = pd.DataFrame([[x.fecha, x.intervalo, x.medida, x.identificador]], columns=['fecha','intervalo','medida','identificador'])
            # Append new rows
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
            name=f"Graph {x.fecha}"  # Provide a name for each line
        ))

    # Customize the graph layout
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
            xanchor='left',  # Set the anchor point of the legend to the left
            x=0.05  # Adjust the x position of the legend label
        )
    )

    graph = fig.to_html(full_html=False)  # Render the plot in HTML

    return graph

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

    graph = genGraph(query,1)

    return render_template('history.html', graph=graph)

@core.route('/inside/daily', methods=['GET', 'POST'])
def dailyview():

    form = SelectDay()

    results = " "

    if form.validate_on_submit():
        year = form.year.data
        month = form.month.data
        day = form.day.data
        date = f"{year}-{month}-{day}"

        query = Crypto.query.filter_by(fecha=date, identificador=form.cOp.data).all()

        if query == []:
            graph = "No results found"
        else:
            graph = genGraph(query,2)

        return render_template('daily.html', form=form, graph=graph)

    return render_template('daily.html', form=form, graph=results)

@core.route('/inside/compare', methods=['GET', 'POST'])
def compareview():

    form = SelectDay2()

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

        if query == []:
            graph = "No results found on the first query"
        elif query2 == []:
            graph = "No results found on the second query"
        else:
            graph = genGraph2([query,query2],["Red","Black"])

        return render_template('compare.html', form=form, graph=graph)

    return render_template('compare.html', form=form, graph=results)

@core.route('/inside/toggle', methods=['GET', 'POST'])
def uploadview():

    form = CambiarDelay()

    test = Tiempo.query.first()
    delay = test.dato

    if form.validate_on_submit():
        test.dato = int(form.newDelay.data)
        db.session.commit()

        return redirect(url_for('core.uploadview'))

    return render_template('upload.html', form=form, delay=delay)