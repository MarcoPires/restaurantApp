from flask import session


def get(key):
    """Gets given session variavel"""
    if key in session:
        return session[key]
    return None


def set(key, value):
    """Sets given session variavel"""
    session[key] = value


def delete(key):
    """Delete given session variavel"""
    if key in session:
    	del session[key]


def getSession():
    """Gets lists of session variavels"""
    return session;