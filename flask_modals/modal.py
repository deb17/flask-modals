from functools import wraps

from flask import (Blueprint, render_template, get_flashed_messages,
                   _app_ctx_stack, session, redirect, request)
from jinja2 import Markup
from flask_modals import turbo

from flask_modals.parser import parse_html


def modal_messages():
    '''This will be available in the app templates for use in the modal
    body.
    '''
    return Markup(render_template('modals/modalMessages.html'))


def render_template_modal(*args, **kwargs):
    '''Call this function instead of render_template when the page
    contains a modal form.

    It accepts all the arguments passed to render_template and 3 others:

    modal: id of the modal
    turbo: Set this to False if modal is not be displayed. It should be
           True for initial page loads and for modal display.
    redirect: Set this to False if you want to render templates and not
              redirect.
    '''

    ctx = _app_ctx_stack.top
    modal = kwargs.pop('modal', None)
    replace = kwargs.pop('turbo', True)
    update = False
    redirect = kwargs.pop('redirect', True)
    show_modal = False

    if turbo.can_stream():
        if replace:
            show_modal = True
            # prevent flash messages from showing both outside and
            # inside the modal
            ctx._modal = True
        else:
            update = False if redirect else True

    setup_for_reload()

    html, stream, target = parse_html(
        render_template(*args, **kwargs),
        modal,
        redirect,
        update,
        show_modal
    )

    if show_modal:
        return turbo.stream(turbo.replace(stream, target=target))

    if update:
        return turbo.stream(turbo.update(stream, target='turbo-stream__body'))

    return html


def redirect_to(*args, **kwargs):
    '''Use this function instead of Flask's `redirect` if you want to do
    a full reload of the page on form submit. Turbo Drive normally does
    an ajax load of the page.
    '''

    session['_keep_flashes'] = True
    return redirect(*args, **kwargs)


def render_template_redirect(*args, **kwargs):
    '''Reload the page if session variable is set, i.e. the route is the
    target of the `redirect_to` function.
    '''

    setup_for_reload()
    return render_template(*args, **kwargs)


def setup_for_reload():
    '''Setup for reload conditionally. App context variable `_reload`
    causes the reload to happen - see template `turbo.html`. Flashes
    need to be saved so that they are again available on reload.
    '''

    if '_keep_flashes' in session:
        del session['_keep_flashes']
        ctx = _app_ctx_stack.top
        ctx._reload = True
        session['_flashes'] = get_flashed_messages(with_categories=True)


def response(template=None):
    '''Use this decorator if coding `render_template_modal` in a number
    of places in a view function looks verbose.
    '''
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = f"{request.endpoint.replace('.', '/')}.html"
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template_modal(template_name, **ctx)
        return decorated_function
    return decorator


class Modal:
    def __init__(self, app=None):

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        '''Initialize the extension.

        Call method for blueprint and register template globals for app.
        '''

        self.register_blueprint(app)
        app.add_template_global(modal_messages)
        app.jinja_env.globals['modals'] = self.load
        app.jinja_env.globals['show_flashed_messages'] = \
            self.show_flashed_messages

    def register_blueprint(self, app):

        bp = Blueprint('modals', __name__, template_folder='templates',
                       static_folder='static',
                       static_url_path='/modals/static')

        app.register_blueprint(bp)

    @staticmethod
    def show_flashed_messages(*args, **kwargs):
        '''Delegate to get_flashed_messages if _modal is set on the
        app context. If it is not set, it means modal is not being
        displayed and so we do not flash messages in it.
        '''

        ctx = _app_ctx_stack.top
        if not getattr(ctx, '_modal', None):
            return

        return get_flashed_messages(*args, **kwargs)

    def load(self, url=None):
        '''Load the following markup:

        1. turbo.html - Hotwire Turbo library
        2. nprogress.html - NProgress js library for progress bar
        3. jstemplate.html - Remove extra modal-backdrop divs, control
                             progress bar, add body attribute
                             `data-turbo="false"`.
        '''

        ctx = _app_ctx_stack.top
        reload = getattr(ctx, '_reload', None)

        turbo_html = render_template(
            'modals/turbo.html',
            turbo=turbo.load,
            url=url,
            reload=reload
        )
        nprogress_html = render_template('modals/nprogress.html')
        main_html = render_template('modals/jstemplate.html')

        html = Markup(turbo_html + nprogress_html + main_html)

        return html
