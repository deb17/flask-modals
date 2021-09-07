from flask import redirect, url_for, flash, session, render_template
from flask_login import login_user, logout_user
from flask_modals import render_template_modal, response

from app import app, user
from app.forms import LoginForm, NewsletterForm


@app.route('/', methods=['GET', 'POST'])
def index():
    '''This index route handles the login form as well. The login form
    is present in a modal.

    `render_template_modal` takes the modal id as an argument apart
    from the `render_template` arguments.
    '''
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data != 'test' or form.password.data != 'pass':
            flash('Invalid username or password', 'danger')
            return redirect(url_for('index'))

        login_user(user, remember=form.remember_me.data)

        flash('You have logged in!', 'success')
        return redirect(url_for('home'))

    return render_template_modal('index.html', title='Index page', form=form,
                                 modal='modal-form')


# Use the following code if you want to redirect to the same page that
# contained the modal.
#
# @app.route('/', methods=['GET', 'POST'])
# def index():

#     modal = session.pop('modal', 'modal-form')

#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.username.data != 'test' or form.password.data != 'pass':
#             flash('Invalid username or password', 'danger')
#             return redirect(url_for('index'))

#         login_user(user, remember=form.remember_me.data)

#         flash('You have logged in!', 'success')
#         session['modal'] = None
#         return redirect(url_for('index'))

#     return render_template_modal('index.html', title='Index page', form=form,
#                                  modal=modal)

# Use the following code if you want to render a template instead of
# redirecting.
#
# @app.route('/', methods=['GET', 'POST'])
# def index():

#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.username.data != 'test' or form.password.data != 'pass':
#             flash('Invalid username or password', 'danger')
#             return render_template_modal('index.html', title='Index page',
#                                          form=form, modal='modal-form')

#         login_user(user, remember=form.remember_me.data)

#         flash('You have logged in!', 'success')
#         return render_template_modal('index.html', title='Index page',
#                                      form=form, modal=None)

#     return render_template_modal('index.html', title='Index page', form=form,
#                                  modal='modal-form')

# Use the following code if you want to render a template instead of
# redirecting and make the code less verbose.
#
# @app.route('/', methods=['GET', 'POST'])
# @response('index.html')
# def index():

#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.username.data != 'test' or form.password.data != 'pass':
#             flash('Invalid username or password', 'danger')
#             return {'title': 'Index page', 'form': form,
#                     'modal': 'modal-form'}

#         login_user(user, remember=form.remember_me.data)

#         flash('You have logged in!', 'success')
#         return {'title': 'Index page', 'form': form, 'modal': None}

#     return {'title': 'Index page', 'form': form, 'modal': 'modal-form'}


@app.route('/home', methods=['GET', 'POST'])
def home():
    '''This is a normal route without a modal form.'''

    form = NewsletterForm()

    if form.validate_on_submit():
        flash('You have subscribed to the newsletter!', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', title='Home page', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out!', 'success')
    return redirect(url_for('index'))
