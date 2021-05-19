## Modals for Flask

Use forms in Bootstrap 4 modals with Flask.

### Description

Plain forms can be boring. Using them in modals is possible, but requires
JavaScript. Normal form submission in modals has its own problems.

This Flask extension eases the process of using forms in (Bootstrap 4) modals.
No JavaScript coding is required on your part. The ajax calls are handled behind
the scenes with html-over-the-wire Turbo library. You can code in pure Python -
flashing messages and rendering templates.

### Installation

```Shell
pip install Flask-Modals
```

### Usage

1. Import the `Modal` class and instantiate it in your `app.py` file.

    ```Python
    from flask_modals import Modal

    app = Flask(__name__)
    modal = Modal(app)
    ```
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
    <br>
5. Import the function `render_template_modal` in your `routes.py` file and use
it instead of `render_template` in the route handler for the page with the modal
form. It takes the same arguments as `render_template`, apart from `modal` (the
modal `id`), and optionally `turbo` (`False` if modal is not to be displayed) and
`redirect` (`False` if you are not redirecting). See the next examples for use of
`turbo` and `redirect`. Use `redirect_to` function if redirecting to a page
without modal forms.

    Example route handler:

    ```Python
    from flask_modals import render_template_modal, redirect_to

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
            return redirect_to(url_for('home'))

        return render_template_modal('index.html', form=form, modal='modal-form')
    ```
    
    In the target route, use `render_template_redirect` with the same arguments
    as `render_template`.
    
    ```Python
    from flask_modals import render_template_redirect

    @app.route('/home')
    def home():
        ...
        ...
        return render_template_redirect('home.html', ...) 
    ```
    See the example folder in the repo for more details.
    <br>

6. If you want to redirect to the same page outside the modal, use Flask's
`session` proxy as follows:

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
7. If you want to render a template and not redirect, then use the following
pattern:

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

### Note

1. The extension loads the Turbo library only in pages that have a modal
form.

2. It loads the NProgress js library to display a progress bar during form
submission.  
