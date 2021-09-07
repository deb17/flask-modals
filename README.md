## Modals for Flask

Use forms in Bootstrap modals with Flask.

### Description

Plain forms can be boring. Using them in modals is possible, but requires
JavaScript. Normal form submission in modals has its own problems.

This Flask extension eases the process of using forms in Bootstrap modals.
Bootstrap versions 4 and 5 are supported. No JavaScript coding is required on 
your part. The JavaScript is handled behind the scenes and uses
html-over-the-wire. You can code in pure Python - flashing messages and rendering
templates.

### Installation

```Shell
pip install Flask-Modals
```

### Setup

1. Import the `Modal` class and instantiate it in your `app.py` file.

    ```Python
    from flask_modals import Modal

    app = Flask(__name__)
    modal = Modal(app)
    ```
    You will also need a secret key in the app config (not shown).
    <br>
2. Alternatively if you are using the application factory pattern:

    ```Python
    from flask_modals import Modal

    modal = Modal()

    def create_app():
        app = Flask(__name__)
        modal.init_app(app)
    ```
    <br>
3. Include the following in the head tag of your base template.

    ```html
    {{ modals() }}
    ```
    <br>
4. Include the following in the modal body.

    ```html
    <div class="modal-body">
    {{ modal_messages() }}
    <form method="post">
    ...
    ```

### Basic usage

You only need to import the function `render_template_modal` in your `routes.py`
file. Use it instead of `render_template` in the route handler for the page with
the modal form. It takes an extra argument - `modal` (the modal `id`).

Example route handler:

```Python
from flask_modals import render_template_modal

@app.route('/', methods=['GET', 'POST'])
def index():

    # Following code is standard in any application
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data != 'test' or form.password.data != 'pass':
            flash('Invalid username or password', 'danger')
            return redirect(url_for('index'))

        login_user(user, remember=form.remember_me.data)

        flash('You have logged in!', 'success')
        return redirect(url_for('home'))

    # Following line is new
    return render_template_modal('index.html', form=form, modal='modal-form')
```

### Other usage

1. If you want to redirect to the same page outside the modal, use Flask's
`session` proxy:

    ```Python
    @app.route('/', methods=['GET', 'POST'])
    def index():

        flag = session.pop('flag', False)

        form = LoginForm()
        if form.validate_on_submit():
            if form.username.data != 'test' or form.password.data != 'pass':
                flash('Invalid username or password', 'danger')
                return redirect(url_for('index'))

            login_user(user, remember=form.remember_me.data)

            flash('You have logged in!', 'success')
            session['flag'] = True
            return redirect(url_for('index'))

        modal = None if flag else 'modal-form' 
        return render_template_modal('index.html', form=form, modal=modal)
    ```
    <br>
2. If you want to render a template and not redirect:

    ```Python
    @app.route('/', methods=['GET', 'POST'])
    def index():

        form = LoginForm()
        if form.validate_on_submit():
            if form.username.data != 'test' or form.password.data != 'pass':
                flash('Invalid username or password', 'danger')
                return render_template_modal('index.html', form=form, modal='modal-form')

            login_user(user, remember=form.remember_me.data)

            flash('You have logged in!', 'success')
            return render_template_modal('index.html', form=form, modal=None)

        return render_template_modal('index.html', form=form, modal='modal-form')
    ```
    If the above looks verbose, you can use the `response` decorator and
    return a context dictionary, like so:

    ```Python
    from flask_modals import response

    @app.route('/', methods=['GET', 'POST'])
    @response('index.html')
    def index():
        ...
        ...
        return {'form': form, 'modal': 'modal-form'}
    ```
    <br>

### Note

1. See the examples folder in the repo for more details.

2. The extension loads the NProgress js library to display a progress bar during
form submission.  

3. If you have custom javascript which has global constants, you need to wrap it
in an IIFE. Otherwise, there could be redeclaration errors.
