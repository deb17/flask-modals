from flask import Blueprint, render_template, Markup
from turbo_flask import Turbo

from modals.parser import add_turbo_stream_ids

turbo = Turbo()


def modal_messages():
    return Markup(render_template('modals/modal_messages.html'))


def render_template_modal(*args, **kwargs):

    modal = kwargs.pop('modal', None)
    show = kwargs.pop('show', True)

    html, stream, target = add_turbo_stream_ids(
        render_template(*args, **kwargs),
        modal
    )
    if show:
        print('ABC')
        if turbo.can_stream():
            print('HERE')
            return turbo.stream(
                turbo.replace(stream, target=target)
            )
    print('ASDF')
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

    def registed_blueprint(self, app):

        bp = Blueprint('modals', __name__, template_folder='templates')
        app.register_blueprint(bp)

    def load_js(self):

        pass
        # if g.get('_modal'):
        # re
