from flask import session


def login(username, password):

    if username == 'test' and password == 'pass':
        session['id'] = 1
        return True
    return False


def register(form):
    '''Logic to register a new user with valid credentials.'''

    return True


def logout():

    session.pop('id', None)
