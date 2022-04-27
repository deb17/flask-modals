from flask import session


def login(username, password, ajax):

    if username == 'test' and password == 'pass':
        if ajax:
            return None
        session['id'] = 1
        return True
    return False


def register(form, ajax):
    '''Logic to register a new user with valid credentials.'''

    if ajax:
        return None
    return True


def logout():

    session.pop('id', None)
