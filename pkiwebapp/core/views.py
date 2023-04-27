from flask import render_template, Blueprint, redirect, url_for, session
from flask_login import login_required
from pkiwebapp.core.forms import SignInForm 

core = Blueprint('core', __name__)

@core.route('/', methods=['GET', 'POST'])
def homeview():
    form = SignInForm()

    if form.validate_on_submit():
        session.permanent = True
        return redirect(url_for('core.insideview'))

    return render_template('home.html', form = form)

@core.route('/inside', methods=['GET', 'POST'])
def insideview():
    return render_template('inside.html')