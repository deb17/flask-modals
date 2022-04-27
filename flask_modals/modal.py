from functools import wraps

from flask import (Blueprint, render_template, get_flashed_messages,
                   _app_ctx_stack, request)
from jinja2 import Markup
from flask_modals.partial import get_partial


def modal_messages():
    '''This will be available in the app templates for use in the modal
    body.
    '''
    return Markup(render_template('modals/modalMessages.html'))


def render_template_modal(*args, **kwargs):
    '''Call this function instead of render_template when the page
    contains a modal form.

    It accepts all the arguments passed to `render_template` apart
    from `modal` which is the `id` of the modal.
    '''

    ctx = _app_ctx_stack.top
    modal = kwargs.pop('modal', 'modal-form')

    if can_stream():
        # prevent flash messages from showing both outside and
        # inside the modal
        ctx._modal = True
        partial = get_partial(modal, *args, **kwargs)
        return f'<template>{partial}</template>'
    else:
        return render_template(*args, **kwargs)


def can_stream():
    '''Returns `True` if the client accepts streams.'''

    return 'text/modal-stream.html' in request.accept_mimetypes.values()


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

    def load(self):
        '''Load the following markup:

        1. nprogress.html - NProgress js library for progress bar
        2. jstemplate.html - Load js for fetch call
        '''

        nprogress_html = render_template('modals/nprogress.html')
        main_html = render_template('modals/jstemplate.html')

        html = Markup(nprogress_html + main_html)

        return html
