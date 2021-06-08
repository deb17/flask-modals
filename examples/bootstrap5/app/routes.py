from flask import render_template, redirect, url_for, flash, session, request
from flask_modals import (render_template_modal, response, redirect_to,
                          render_template_redirect)
from email_validator import validate_email, EmailNotValidError

from app import app
from app.utils import login, register, logout
from app.forms import LoginForm, RegistrationForm


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    '''This page has 2 modal forms. (For a simpler example, see the
    bootstrap 4 example.) Call `render_template_modal` instead of
    `render_template`. It takes the modal id as an argument apart from
    the arguments passed to `render_template`. There are 2 optional
    arguments - `turbo` (`False` if redirecting to the same page) and
    `redirect` (`False` if rendering a template instead of redirecting).
    Only `turbo` is needed below.
    '''

    form1 = RegistrationForm()
    form2 = LoginForm()
    modal = session.pop('modal', None)
    flag = session.pop('flag', True)

    if form1.validate_on_submit():
        if register(form1):
            flash(
                'You have registered successfully! Please login.',
                'success'
            )
            session['flag'] = False
            return redirect(url_for('auth'))
        else:
            flash('Could not register.', 'danger')
            session['modal'] = 'register-modal'
            return redirect(url_for('auth'))

    if form2.validate_on_submit():
        if login(form2.username.data, form2.password.data):
            flash('You have logged in successfully!', 'success')
            session['flag'] = False
            return redirect(url_for('subscribe'))
        else:
            flash('Invalid credentials.', 'danger')
            session['modal'] = 'login-modal'
            return redirect(url_for('auth'))

    form = 'form1' if request.form.get('submit1') else ''

    if form1.errors and form == 'form1':
        modal = 'register-modal'
    elif form2.errors:
        modal = 'login-modal'

    return render_template_modal('auth.html', form1=form1, form2=form2,
                                 modal=modal, turbo=flag)


@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    '''Example of one modal page redirecting to another modal page.
    `flag` is not required if not redirecting from a modal page (auth).
    '''

    flag = session.pop('flag', True)
    if 'id' not in session:
        flash('You need to be logged in to access the page.', 'info')
        return redirect(url_for('index'))

    name = email = ''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if not name:
            flash('Name is required.', 'danger')
        if not email:
            flash('Email is required.', 'danger')
        else:
            try:
                valid = validate_email(email)
                email = valid.email
            except EmailNotValidError:
                flash('Email is invalid.', 'danger')
            else:
                if name:
                    flash('You have been subscribed!', 'success')
                    return redirect(url_for('feedback'))

    return render_template_modal('subscribe.html', modal='modal-form',
                                 turbo=flag, name=name, email=email)

# Use `redirect_to` for a full page reload. Pair it with
# `render_template_redirect` in the non-modal target route.
#
# @app.route('/subscribe', methods=['GET', 'POST'])
# def subscribe():
#     '''Example of one modal page redirecting to another modal page.
#     `flag` is not required if not redirecting from a modal page (auth).
#     '''

#     flag = session.pop('flag', True)
#     if 'id' not in session:
#         flash('You need to be logged in to access the page.', 'info')
#         return redirect(url_for('index'))

#     name = email = ''
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         if not name:
#             flash('Name is required.', 'danger')
#         if not email:
#             flash('Email is required.', 'danger')
#         else:
#             try:
#                 valid = validate_email(email)
#                 email = valid.email
#             except EmailNotValidError:
#                 flash('Email is invalid.', 'danger')
#             else:
#                 if name:
#                     flash('You have been subscribed!', 'success')
#                     return redirect_to(url_for('feedback'))

#     return render_template_modal('subscribe.html', modal='modal-form',
#                                  turbo=flag, name=name, email=email)

# Example of redirecting to the same page
#
# @app.route('/subscribe', methods=['GET', 'POST'])
# def subscribe():

#     flag = session.pop('flag', True)
#     if 'id' not in session:
#         flash('You need to be logged in to access the page.', 'info')
#         return redirect(url_for('index'))

#     name = email = ''
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         if not name:
#             flash('Name is required.', 'danger')
#         if not email:
#             flash('Email is required.', 'danger')
#         else:
#             try:
#                 valid = validate_email(email)
#                 email = valid.email
#             except EmailNotValidError:
#                 flash('Email is invalid.', 'danger')
#             else:
#                 if name:
#                     flash('You have been subscribed!', 'success')
#                     session['flag'] = False
#                     return redirect(url_for('subscribe'))

#     return render_template_modal('subscribe.html', modal='modal-form',
#                                  name=name, email=email, turbo=flag)

# Example of rendering a template instead of redirecting
#
# @app.route('/subscribe', methods=['GET', 'POST'])
# def subscribe():

#     if 'id' not in session:
#         flash('You need to be logged in to access the page.', 'info')
#         return redirect(url_for('index'))

#     name = email = ''
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         if not name:
#             flash('Name is required.', 'danger')
#         if not email:
#             flash('Email is required.', 'danger')
#         else:
#             try:
#                 valid = validate_email(email)
#                 email = valid.email
#             except EmailNotValidError:
#                 flash('Email is invalid.', 'danger')
#             else:
#                 if name:
#                     flash('You have been subscribed!', 'success')
#                     return render_template_modal(
#                         'subscribe.html', modal='modal-form',
#                         name=name, email=email,
#                         turbo=False, redirect=False
#                     )

#     return render_template_modal('subscribe.html', modal='modal-form',
#                                  name=name, email=email, redirect=False)

# Example of rendering a template instead of redirecting - less verbose.
#
# @app.route('/subscribe', methods=['GET', 'POST'])
# @response('subscribe.html')
# def subscribe():

#     if 'id' not in session:
#         flash('You need to be logged in to access the page.', 'info')
#         return redirect(url_for('index'))

#     name = email = ''
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         if not name:
#             flash('Name is required.', 'danger')
#         if not email:
#             flash('Email is required.', 'danger')
#         else:
#             try:
#                 valid = validate_email(email)
#                 email = valid.email
#             except EmailNotValidError:
#                 flash('Email is invalid.', 'danger')
#             else:
#                 if name:
#                     flash('You have been subscribed!', 'success')
#                     return {
#                         'modal': 'modal-form', 'name': name, 'email': email,
#                         'turbo': False, 'redirect': False
#                     }

#     return {'modal': 'modal-form', 'name': name, 'email': email,
#             'redirect': False}


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():

    email = feedback = ''
    if request.method == 'POST':
        email = request.form['email']
        feedback = request.form['feedback']

        if not email:
            flash('Email is required.', 'danger')
        if not feedback:
            flash('Feedback is required.', 'danger')

        if email:
            try:
                valid = validate_email(email)
                email = valid.email
            except EmailNotValidError:
                flash('Email is invalid.', 'danger')
            else:
                if feedback:
                    flash('Thanks for your feedback!', 'success')
                    return redirect(url_for('feedback'))

    return render_template('feedback.html', email=email, feedback=feedback)

# Use `render_template_redirect` for a full page reload.
#
# @app.route('/feedback', methods=['GET', 'POST'])
# def feedback():

#     email = feedback = ''
#     if request.method == 'POST':
#         email = request.form['email']
#         feedback = request.form['feedback']

#         if not email:
#             flash('Email is required.', 'danger')
#         if not feedback:
#             flash('Feedback is required.', 'danger')

#         if email:
#             try:
#                 valid = validate_email(email)
#                 email = valid.email
#             except EmailNotValidError:
#                 flash('Email is invalid.', 'danger')
#             else:
#                 if feedback:
#                     flash('Thanks for your feedback!', 'success')
#                     return redirect(url_for('feedback'))

#     return render_template_redirect('feedback.html', email=email,
#                                     feedback=feedback)


@app.route('/logout')
def logout_user():

    logout()
    return redirect(url_for('index'))
