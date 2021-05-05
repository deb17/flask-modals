## Modals for Flask

Use forms in Bootstrap 4 modals with Flask.

### Description

Plain forms can be boring. Using them in modals is possible, but requires
JavaScript coding. Normal form submission in modals is not possible in
Flask.

This extension eases the process of using forms in (Bootstrap 4) modals. No
JavaScript coding is required on your part. The ajax calls are handled behind
the scenes with html-over-the-wire Turbo library and the Turbo-Flask
extension. You can code in pure Python - flashing messages and rendering
templates.

### Installation

```
pip install Flask-Modals
```

### Usage

1. Import the `Modal` class and instantiate in your `app.py` file.

```Python
from flask_modals import Modal

app = Flask(__name__)
modal = Modal(app)
```

2. Alternatively if you are using the application factory pattern:

```Python
from flask_modals import Modal

modal = Modal()

def create_app():
    app = Flask(__name__)
    modal.init_app(app)
```

3. Include the following in the head tag of your base template.

```html
{{ modals() }}
```

4. Include the following in the modal body.

```html
<div class="modal-body">
  {{ modal_messages() }}
  <form method="post">
  ...
```

5. Import the function `render_template_modal` in your `routes.py` file
and use it instead of `render_template` in the route handler for the page
with the modal form. It takes the same arguments as `render_template`, apart
from `modal` (the modal `id`) and `turbo` (which should be `False` if modal
is not to be displayed). See next example for use of `turbo`.

Example route handler:

```Python
from flask_modals import render_template_modal

@app.route('/', methods=['GET', 'POST'])
def index():

    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data != 'test' or form.password.data != 'pass':
            flash('Invalid username or password', 'danger')
            return redirect(url_for('index'))

        login_user(user, remember=form.remember_me.data)

        flash('You have logged in!', 'success')
        return redirect(url_for('home'))

    return render_template_modal('index.html', form=form, modal='modal-form')
```
See the example folder in the repo for more details.

6. If you want to redirect to the same page (containing the modal), use Flask's
`session` proxy as follows:

```Python
@app.route('/', methods=['GET', 'POST'])
def index():

    if 'check' in session:
        check = session['check']
        del session['check']
    else:
        check = True

    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data != 'test' or form.password.data != 'pass':
            flash('Invalid username or password', 'danger')
            return redirect(url_for('index'))

        login_user(user, remember=form.remember_me.data)

        flash('You have logged in!', 'success')
        session['check'] = False
        return redirect(url_for('index'))

    return render_template_modal('index.html', form=form,
                                 modal='modal-form', turbo=check)
```

### Note

1. The extension loads the Turbo library only in pages that have a modal
form.

2. It loads the NProgress js library to display a progress bar during form
submission. 
