from flask import request, flash, redirect, url_for
from restaurantApp import app
from restaurantApp.security.access_control import *
from restaurantApp.session import storage as session, userData 
from restaurantApp.response import handler as response
from restaurantApp.helpers import jsonHandler 
from restaurantApp import config


# imports to handle oauth flow
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests


# application login
@app.route("/authenticate", methods=['POST'])
@checkStateToke
def authenticate():
    data = jsonHandler.loadsJSON(request.data)
    user = checkAuthenticationCredentials( data['email'], data["password"] )
    if not user:
        return response.builder( 'Invalid access credentials.', 401 )
    
    session.set( 'provider', 'application' )
    session.set( 'user_id', user.id ) 
    session.set( 'username', user.name ) 
    session.set( 'picture', user.picture ) 
    session.set( 'email', user.email )

    flash("Now logged in as %s" % session.get('username'), "alert-success")
    return response.successLoginMsg( session.get('username'), session.get('picture') )


#  Login with google+
@app.route("/gconnect", methods=['POST'])
@checkStateToke
def gconnect():
    
    # Obtain authorization code
    code = request.data
    
    try:
        # Upgrade the authorization code into a credentials object 
        oauth_flow = flow_from_clientsecrets( config.data["google_data"], scope='' )
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange( code )
    except FlowExchangeError:
        return response.builder( 'Failed to upgrade the authorization code.', 401 )

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ( config.data["google_access_token_check"] + access_token )
    result = handleApiRequestsJSON( url )

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        return response.builder( 'Error', 500 )

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return response.builder( "Token's user ID doesn't match given user ID.", 401 )
    
    # Verify that the access token is valid for this app.
    gclient_id = jsonHandler.openLocalJSON( config.data["google_data"] )['web']['client_id']
    if result['issued_to'] != gclient_id:
        return response.builder( "Token's client ID does not match app's.", 401 )

    # Check if user is already logedin
    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        return response.builder( "Current user is already connected.", 200 )

    # Store the access token in the session for later use.
    session.set( 'credentials', credentials.to_json() ) 
    session.set( 'access_token', credentials.access_token ) 
    session.set( 'gplus_id', gplus_id )
    session.set( 'provider', 'google' )

    # Get user info
    userinfo_url = config.data["google_user_info"]
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get( userinfo_url, params=params )

    data = answer.json()

    # Store user data.
    session.set( 'username', data['name'] ) 
    session.set( 'picture', data['picture'] ) 
    session.set( 'email', data['email'] ) 

    # See if user exists, if it doesn't make a new one
    session.set( 'user_id', userData.ifnotUser( data['email'] ) )

    flash("Now logged in as %s" % session.get('username'), "alert-success")      
    return response.successLoginMsg( session.get('username'), session.get('picture') )
    

#  Login with facebook
@app.route("/fbconnect", methods=['POST'])
@checkStateToke
def fbconnect():
    # Obtain authorization code
    access_token = request.data

    fb_credentials =  jsonHandler.openLocalJSON( config.data["facebook_data"] )
    app_id = fb_credentials['web']['app_id']
    app_secret = fb_credentials['web']['app_secret']
    url = config.data["facebook_access_token_check"] % ( app_id, app_secret, access_token )
    result = handleApiRequests( url )
    
    # Use token to get user info from API
    userinfo_url = config.data["facebook_me_endpoint"] 
    # strip expire tag from access token
    token = result.split("&")[0]

    url = userinfo_url + '?%s&fields=name,id,email' % token
    data = handleApiRequestsJSON( url )

    session.set( 'provider', 'facebook' )  
    session.set( 'username', data["name"] )
    session.set( 'email', data["email"] )
    session.set( 'facebook_id', data["id"] ) 

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    session.set( 'access_token', stored_token )

    # Get user picture
    url = userinfo_url + '/picture?%s&redirect=0&height=200&width=200' % token
    data = handleApiRequestsJSON( url )

    session.set( 'picture', data["data"]["url"] ) 

    # See if user exists, if it doesn't make a new one
    session.set( 'user_id', userData.ifnotUser( session.get( 'email') ) )    
    

    flash("Now logged in as %s" % session.get('username'), "alert-success")
    return response.successLoginMsg( session.get('username'), session.get('picture') )


# Disconnect based on provider
@app.route('/logout')
def disconnect():
    provider = session.get('provider')
    if provider:
        if provider == 'google':
            gdisconnect()
            session.delete('gplus_id')
            session.delete('credentials')
        if provider == 'facebook':
            fbdisconnect()
            session.delete('facebook_id')
        
        session.delete('username')
        session.delete('email')
        session.delete('picture')
        session.delete('user_id')
        session.delete('provider')
        session.delete('access_token')

        flash("You have successfully been logged out.", "alert-success")
        return redirect(url_for('showRestaurants'))
    else:
        flash("You were not logged in", "alert-danger")
        return redirect(url_for('showRestaurants'))


# Logout with google+
@app.route("/gdisconnect")
def gdisconnect():
    # only disconnect a connected user.
    credentials = session.get("access_token")
    if credentials is None:
        return response.builder( 'Current user not connected.', 401 )
    
    # Execute HTTP GET request to revoke current token.
    access_token = session.get("access_token")
    url = config.data['google_logout'] % access_token
    result = handleApiRequests( url = url, index = 0 )
    return "you have been logged out"


# Logout with facebook
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = session.get('facebook_id')
    # The access token must me included to successfully logout
    access_token = session.get('access_token')
    url = config.data['facebook_logout'] % (facebook_id,access_token)
    result = handleApiRequests( url, 'DELETE' )
    return "you have been logged out"


# helper for third-party api requests
def handleApiRequestsJSON(url):
    return jsonHandler.loadsJSON( handleApiRequests( url )  )


def handleApiRequests( url, verb = 'GET', index = 1 ):
    h = httplib2.Http()
    return h.request( url, verb )[index]