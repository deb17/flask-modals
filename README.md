## Modals for Flask

Use forms in Bootstrap modals with Flask.

### Description

Plain forms can be boring. Using them in modals is possible, but requires
JavaScript. Normal form submission in modals has its own problems.

This Flask extension eases the process of using forms in Bootstrap modals.
Bootstrap versions 4 and 5 are supported. No JavaScript coding is required on 
your part. The ajax calls are handled behind the scenes with html-over-the-wire
[Turbo](https://turbo.hotwire.dev/) library. You can code in pure Python -
flashing messages and rendering templates.

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
the modal form. It takes as arguments `modal` (the modal `id`), and optionally
`turbo` and `redirect` (discussed next), in addition to the arguments passed to
`render_template`.

Example route handler:

```Python
from flask_modals import render_template_modal

@app.route('/', methods=['GET', 'POST'])
def index():

    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data != 'test' or form.password.data != 'pass':
            flash('Invalid username or password', 'danger')
            # You can use `render_template_modal` here
            return redirect(url_for('index'))

        login_user(user, remember=form.remember_me.data)

        flash('You have logged in!', 'success')
        return redirect(url_for('home'))

    return render_template_modal('index.html', form=form, modal='modal-form')
```

### Other usage

1. If you want to redirect to the same page outside the modal, use Flask's
`session` proxy and the `turbo` argument as follows:

    ```Python
    @app.route('/', methods=['GET', 'POST'])
    def index():

        flag = session.pop('flag', True)

        form = LoginForm()
        if form.validate_on_submit():
            if form.username.data != 'test' or form.password.data != 'pass':
                flash('Invalid username or password', 'danger')
                return redirect(url_for('index'))

            login_user(user, remember=form.remember_me.data)

            flash('You have logged in!', 'success')
            session['flag'] = False
            return redirect(url_for('index'))

        return render_template_modal('index.html', form=form,
                                    modal='modal-form', turbo=flag)
    ```
    <br>
2. If you want to render a template and not redirect, then use the `turbo` and
`redirect` arguments as follows:

    ```Python
    @app.route('/', methods=['GET', 'POST'])
    def index():

        form = LoginForm()
        if form.validate_on_submit():
            if form.username.data != 'test' or form.password.data != 'pass':
                flash('Invalid username or password', 'danger')
                return render_template_modal('index.html', form=form,
                                            modal='modal-form', redirect=False)

            login_user(user, remember=form.remember_me.data)

            flash('You have logged in!', 'success')
            return render_template_modal('index.html', form=form, turbo=False,
                                        modal='modal-form', redirect=False)

        return render_template_modal('index.html', form=form,
                                    modal='modal-form', redirect=False)
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
        return {'form': form, 'modal': 'modal-form', 'redirect': False}
    ```
    <br>
3. If you want to reload the page on form submit (for example, to refresh the
`head` tag), you can use `redirect_to` function in the modal route and
`render_template_redirect` function in the target route. They take in the same
arguments as Flask's `redirect` and `render_template` functions respectively.

### Note

1. See the examples folder in the repo for more details.

2. The extension loads the NProgress js library to display a progress bar during
form submission.  
