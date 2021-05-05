from flask import Blueprint, g, render_template, get_flashed_messages
from jinja2 import Markup
from turbo_flask import Turbo

from flask_modals.parser import add_turbo_stream_ids

turbo = Turbo()


def modal_messages():

    return Markup(render_template('modals/modal_messages.html'))


def render_template_modal(*args, **kwargs):

    modal = kwargs.pop('modal', None)
    check_turbo = kwargs.pop('turbo', True)
    g._include = True

    if check_turbo:
        if turbo.can_stream():
            g._modal = True

    html, stream, target = add_turbo_stream_ids(
        render_template(*args, **kwargs),
        modal
    )

    if g.get('_modal'):
        return turbo.stream(turbo.replace(stream, target=target))

    return html


class Modal:
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):

        self.app = app
        turbo.init_app(app)
        self.registed_blueprint(app)
        self.app.add_template_global(modal_messages)
        self.app.jinja_env.globals['modals'] = self.load
        self.app.jinja_env.globals['show_flashed_messages'] = \
            self.show_flashed_messages

    def registed_blueprint(self, app):

        bp = Blueprint('modals', __name__, template_folder='templates',
                       static_folder='static',
                       static_url_path='/modals/static')
        app.register_blueprint(bp)

    @staticmethod
    def show_flashed_messages(*args, **kwargs):

        if not g.get('_modal'):
            return

        return get_flashed_messages(*args, **kwargs)

    def load(self):

        html = (Markup(render_template('modals/turbo.html') +
                       render_template('modals/nprogress.html') +
                       render_template('modals/jstemplate.html') +
                       render_template('modals/bodyattr.html')))

        return html
