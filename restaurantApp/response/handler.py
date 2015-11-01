from flask import make_response
import json

def builder( message = '', error_code = 401, content_type = 'application/json' ):
    """Builds response"""
    response = make_response( json.dumps( message ), error_code )
    response.headers['Content-Type'] = content_type
    return response 

def successLoginMsg(username, picture):
    return '<h1> Welcome, %s!</h1> <img class="login-img" src="%s">' % (username, picture)