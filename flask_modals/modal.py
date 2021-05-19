from functools import partial

from flask import (Blueprint, render_template, get_flashed_messages,
                   _app_ctx_stack, session, redirect)
from jinja2 import Markup
from flask_modals.turbo import Turbo

from flask_modals.parser import add_turbo_stream_ids

turbo = Turbo()


def modal_messages():
    '''This will be available in the app templates for use in the modal
    body.
    '''
    return Markup(render_template('modals/modal_messages.html'))


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
    ctx._include = True  # used in extension templates
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

    html, stream, target = add_turbo_stream_ids(
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
    '''Use this function instead of Flask's `redirect` if you are
    redirecting to a page without modal forms.
    '''

    session['_keep_flashes'] = True
    return redirect(*args, **kwargs)


def render_template_redirect(*args, **kwargs):
    '''Reload the page to unload the Turbo library. See template
    `turbo.html`. Flashes need to be saved so that they are again
    available on reload.
    '''

    if '_keep_flashes' in session:
        del session['_keep_flashes']
        ctx = _app_ctx_stack.top
        ctx._include = False
        session['_flashes'] = get_flashed_messages(with_categories=True)

    return render_template(*args, **kwargs)


class Modal:
    def __init__(self, app=None):

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        '''Initialize the Turbo-Flask extension and register template
        globals for app.
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
        Flask g object. If it is not set, it means modal is not being
        displayed and so we do not flash messages in it.
        '''

        ctx = _app_ctx_stack.top
        if not getattr(ctx, '_modal', None):
            return

        return get_flashed_messages(*args, **kwargs)

    def load(self, url=None):
        '''Load the following markup only if page has a modal form:

        1. turbo.html - Hotwire Turbo library
        2. nprogress.html - NProgress js library for progress bar
        3. jstemplate.html - Remove extra modal-backdrop divs and
                             control progress bar.
        '''

        ctx = _app_ctx_stack.top
        inc = getattr(ctx, '_include', None)
        render = partial(render_template, include=inc)

        html = (Markup(render('modals/turbo.html', turbo=turbo.load, url=url) +
                       render('modals/nprogress.html') +
                       render('modals/jstemplate.html')))

        return html
