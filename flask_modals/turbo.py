'''Copyright notice - The code below is adapted from the Turbo-Flask
extension by Miguel Grinberg (https://github.com/miguelgrinberg/turbo-flask),
which is under MIT license.
'''

from flask import request, current_app
from jinja2 import Markup


_CDN = 'https://cdn.skypack.dev'
_PKG = '@hotwired/turbo'
_VER = 'v7.0.0-beta.5-LhgiwOUjafYu3bb8VbTv'


class Turbo:

    def load(self, version=_VER, url=None):

        if url is None:
            url = f'{_CDN}/pin/{_PKG}@{version}/min/{_PKG}.js'
        return Markup(f'<script type="module" src="{url}"></script>')

    def can_stream(self):
        '''Returns `True` if the client accepts turbo streams.'''

        stream_mimetype = 'text/vnd.turbo-stream.html'
        best = request.accept_mimetypes.best_match([
            stream_mimetype, 'text/html'])
        return best == stream_mimetype

    def _make_stream(self, action, content, target):
        return (f'<turbo-stream action="{action}" target="{target}">'
                f'<template>{content}</template></turbo-stream>')

    def replace(self, content, target):
        return self._make_stream('replace', content, target)

    def update(self, content, target):
        return self._make_stream('update', content, target)

    def stream(self, response_stream):
        '''Create a turbo stream response.'''

        return current_app.response_class(
            response_stream, mimetype='text/vnd.turbo-stream.html')
