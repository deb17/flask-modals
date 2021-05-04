from flask import redirect, url_for, flash, session
from flask_login import login_user, logout_user
from app import app, user
from app.forms import LoginForm

from modals import render_template_modal


@app.route('/', methods=['GET', 'POST'])
def index():

    if 'show' in session:
        show = session['show']
        del session['show']
    else:
        show = True

    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data != 'test' or form.password.data != 'pass':
            flash('Invalid username or password', 'danger')
            return redirect(url_for('index'))

        login_user(user, remember=form.remember_me.data)

        flash('You have logged in!', 'success')
        session['show'] = False
        return redirect(url_for('index'))

    return render_template_modal('index.html', form=form,
                                 modal='modal-form', show=show)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out!', 'success')
    return redirect(url_for('index'))
