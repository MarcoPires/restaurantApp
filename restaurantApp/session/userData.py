from restaurantApp.session import storage as session
from restaurantApp.persistence import data_access as db

# User Helper Functions
def getUserID(email):
    """Receives email and returns one user id"""
    try:
        user = db.getUserByEmail( email )
        return user.id
    except:
        return None


def ifnotUser(email):
    """Receives email, and check if it has not user ID creat new user"""
    user_id = getUserID( email )
    if not user_id:
        return creatUser()
    return user_id


def creatUser():
    """ Create new based on session data, returns the new user id"""
    print "----------------> AKI1.2"
    newUser = db.createUser( name = session.get('username'), 
        email = session.get('email'), picture = session.get('picture') )
    return newUser.id


def getUserInfo(user_id):
    """Receives user id and returns one user"""
    user = db.getUserById( user_id )
    return user


def getUserByEmail(email):
    """Receives email and returns user"""
    try:
        user = db.getUserByEmail( email )
        return user
    except:
        return None


def getCurrentUserInfo():
    """Returns the current session user info"""
    return {
        'id' : session.get('user_id'),
        'name' : session.get('username'),
        'picture' : session.get('picture'),
        'email' : session.get('email'),
    }


def getCurrentUserID():
    """Returns the current session user ID"""
    return session.get('user_id')