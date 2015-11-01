from restaurantApp.session import storage as session, userData
from restaurantApp.response import handler as response
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, redirect, url_for, flash
from functools import wraps
import random, string
import re


# Checks whether the user has access to this content
def allowAccess(dataCreatorID, userID):
    """Check the access permissions to content"""
    if dataCreatorID != userID:
        return False
    return True

# this will generate an anti-forgery state token, for each session
def antiForgeryGenToke():
    """Generate an anti-forgery state token"""
    toke = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    session.set('state', toke)
    return toke


def validateStateToke(state):
    """Validates that the token generated is equal to the received"""
    toke = session.get('state')
    return toke == state


def checkAuthenticationCredentials(email, passw):
    """Validates user access credentials"""
    user = userData.getUserByEmail(email)
    print "---------------->", user.password
    print "---------------->", check_password_hash( user.password, passw )
    if user and check_password_hash( user.password, passw ):
        return user
    return False


def validateEmail(email):
    """Validates user email"""
    if re.search(r'[\w.-]+@[\w.-]+.\w+', email):
        return email
    return False


def saltAndHashed(passw):
    """salt and hashed user password"""
    return generate_password_hash( passw )


# Routes decorators
def checkStateToke(func):
    """Decorators - only allow access to route if toke is valide"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not validateStateToke( request.args.get('state') ):
            return response.builder( 'Invalid state parameter.', 401 )
        return func(*args, **kwargs)

    return decorated_function


def authRequired(func):
    """Authentication required - check if user can access route"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = userData.getCurrentUserInfo()
        if not user['name']:
            flash("Authentication required", "alert-danger")
            return redirect( url_for('showLogin') )
        return func(*args, **kwargs)
    
    return decorated_function