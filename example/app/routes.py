from flask import redirect, url_for, flash, render_template
from flask_login import login_user, logout_user
from flask_modals import render_template_modal

from app import app, user
from app.forms import LoginForm, NewsletterForm


@app.route('/', methods=['GET', 'POST'])
def index():
    '''This index route handles the login form as well. The login form
    is present in a modal.

    `render_template_modal` takes 2 extra arguments - `modal` (the id of
    modal) and `turbo` (whether modal should be displayed. Set to True
    by default). Only the `modal` argument is used below. See the
    commented out code below for usage of `turbo`.
    '''

    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data != 'test' or form.password.data != 'pass':
            flash('Invalid username or password', 'danger')
            return redirect(url_for('index'))

        login_user(user, remember=form.remember_me.data)

        flash('You have logged in!', 'success')
        return redirect(url_for('home'))

    return render_template_modal('index.html', form=form, modal='modal-form')

# Use the following code if you want to redirect to the same page that
# contained the modal.
#
# @app.route('/', methods=['GET', 'POST'])
# def index():

#     if 'check' in session:
#         check = session['check']
#         del session['check']
#     else:
#         check = True

#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.username.data != 'test' or form.password.data != 'pass':
#             flash('Invalid username or password', 'danger')
#             return redirect(url_for('index'))

#         login_user(user, remember=form.remember_me.data)

#         flash('You have logged in!', 'success')
#         session['check'] = False
#         return redirect(url_for('index'))

#     return render_template_modal('index.html', form=form,
#                                  modal='modal-form', turbo=check)


@app.route('/home', methods=['GET', 'POST'])
def home():
    '''This is a normal route without a modal form.'''

    form = NewsletterForm()

    if form.validate_on_submit():
        flash('You have subscribed to the newsletter!', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out!', 'success')
    return redirect(url_for('index'))
