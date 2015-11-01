from flask import render_template, flash, redirect
from restaurantApp import app
from restaurantApp.security.access_control import *
from restaurantApp.persistence import data_access as db
from restaurantApp.session import userData 
from restaurantApp.authentication import interface
from restaurantApp.helpers import filesHandler, jsonHandler
from restaurantApp.response import handler as response

# For money convertion
from re import sub
from decimal import Decimal


# app routes
# ShowLogin
@app.route("/login")
def showLogin():
    # this will generate an anti-forgery state token, for each session
    state = antiForgeryGenToke()
    return render_template( 'login.html', STATE=state )


# Sign Up
@app.route("/signup", methods=['GET','POST'])
def showSignup():

    if request.method == 'POST':

        data = jsonHandler.loadsJSON(request.data)
        email = validateEmail( data["email"] )

        if validateStateToke( data["token"] ):
            if not userData.getUserID( email ) and email:
                name = data["name"]
                password = saltAndHashed( data["password"] )

                if db.createUser(name = name,
                    email = email,password = password):
                    # Register successfully performed
                    return response.builder( 'Register successfully performed', 200 )
                
                return response.builder( 'Error creating the user, please try again later.', 401 )
            
            return response.builder( 'The user is already registered or entered data are wrong.', 401 )
        return response.builder( 'Invalid state parameter.', 401 )
    else:
        return render_template( 'signUp.html', token = antiForgeryGenToke() )


# root route and shows all restaurants
@app.route('/')
@app.route("/restaurants")
def showRestaurants():
    # Get user info for the user menu
    user = userData.getCurrentUserInfo()
    
    # Fetch restaurants
    restaurants = db.getAllRestaurants()
    
    # Render template
    return render_template(
        'restaurants.html',
        filesPath = filesHandler.getFilesFolder(),
        restaurants = list(restaurants), 
        username = user['name'], 
        user_id = user['id'], 
        user_picture = user['picture']
    )


# Create new restaurant
@app.route("/restaurant/new", methods=['GET','POST'])
@authRequired
def newRestaurant():
    # Get user info for the user menu
    user = userData.getCurrentUserInfo()
    
    if request.method == 'POST':
        
        file_path = filesHandler.uploadImage( request.files['file'] )
        
        # Save the new restaurant
        db.newRestaurant( 
            name = request.form['name'],
            file = file_path,
            user_id = user["id"] 
        )
        
        # Inform the user
        flash("New restaurant created!", "alert-success")

        # Redirects to the new area
        return redirect( url_for('showRestaurants') )
    else:
        # Render template
        return render_template( 
            'newRestaurant.html', 
            username = user['name'],
            user_picture = user['picture'] 
        )

# Edit restaurant
@app.route("/restaurant/<int:restaurant_id>/edit", methods=['GET','POST'])
@authRequired
def editRestaurant(restaurant_id):
    # Get user info for the user menu
    user = userData.getCurrentUserInfo()
    
    # Fetches the restaurant to edit
    restaurant = db.getRestaurant( restaurant_id )

    # Checks whether the user has access to this content
    if not allowAccess( restaurant.user_id, user["id"] ):
        # Inform the user
        output = "You are not authorized to edit the %s restaurant. Please create your own restaurant in order to edit!" % restaurant.name
        flash(output, "alert-danger")
        # Redirects to the new area
        return redirect( url_for('showRestaurants') )

    if request.method == 'POST':
        
        if validateStateToke( request.form['csrf'] ):
            # Save the edited restaurant
            name = request.form['name']
            
            file_path = filesHandler.uploadImage( request.files['file'] )
            print "----------->"
            db.updateRestaurant( restaurant = restaurant, 
                name = name, picture = file_path )

            # Inform the user
            output = "Restaurant %s was edited!" % name
            flash( output, "alert-success" )
        
        # Redirects to the new area
        return redirect( url_for('showRestaurants') )
    else:
        # Render template
        return render_template(
            'editRestaurant.html', 
            restaurant = restaurant,
            token = antiForgeryGenToke(),
            username = user['name'],
            user_picture = user['picture'] 
        )


# Delete restaurant
@app.route("/restaurant/<int:restaurant_id>/delete", methods=['GET','POST'])
@authRequired
def deleteRestaurant(restaurant_id):
    # Get user info for the user menu
    user = userData.getCurrentUserInfo()
    
    # Fetches the restaurant to delete
    restaurant = db.getRestaurant( restaurant_id )
    
    # Checks whether the user has access to this content
    if not allowAccess( restaurant.user_id, user["id"] ):
        # Inform the user
        output = "You are not authorized to delete the %s restaurant. Please create your own restaurant in order to delete!" % restaurant.name
        flash( output, "alert-danger" )
        # Redirects to the new area
        return redirect( url_for('showRestaurants') )

    if request.method == 'POST':
        
        if validateStateToke( request.form['csrf'] ):
            # Deleting from database
            db.deleteRestaurant( restaurant )
            
            # Inform the user
            output = "Restaurant %s was deleted!" % restaurant.name
            flash(output, "alert-success")

        # Redirects to the new area
        return redirect( url_for('showRestaurants') )
    else:
        # Render template
        return render_template( 
            'deleteRestaurant.html',
            restaurant = restaurant,
            token = antiForgeryGenToke(),
            username = user['name'],
            user_picture = user['picture'] 
        )


# Shows all menu items
@app.route("/restaurant/<int:restaurant_id>/menu")
def showmenu(restaurant_id):
    # Get user info for the user menu
    user = userData.getCurrentUserInfo()

    # Fetches the context restaurant
    restaurant = db.getRestaurant( restaurant_id )
    
    # Fetches all items from the context restaurant
    items = db.getAllRestaurantMenuItems( restaurant )

    # Fetches all courses type, and respective menu items
    courses = db.getAllRestItemsByCourses( restaurant )

    # Render template
    return render_template(
        'menu.html',
        filesPath = filesHandler.getFilesFolder(),
        restaurant = restaurant,
        items = list(items), 
        courses = courses, 
        user_id = user['id'], 
        username = user['name'],
        user_picture = user['picture'] 
    )


# New menu item
@app.route("/restaurant/<int:restaurant_id>/menu/new", methods=['GET','POST'])
@authRequired
def NewMenuItem(restaurant_id): 
    # Get user info for the user menu
    user = userData.getCurrentUserInfo()
    
    # Fetches the context restaurant
    restaurant = db.getRestaurant( restaurant_id )
    
    # Checks whether the user has access to this content
    if not allowAccess( restaurant.user_id, user["id"] ):
        # Inform the user
        output = "You are not authorized to add menu items to %s restaurant. Please create your own restaurant in order to add items." % restaurant.name
        flash(output, "alert-danger")
        # Redirects to the new area
        return redirect( url_for('showmenu', restaurant_id = restaurant_id) )

    # Fetches all courses type    
    courses = db.getAllCourses()

    if request.method == 'POST':
       
        if validateStateToke( request.form['csrf'] ):
            # Save the new menu item
            db.newRestaurantMenuItem( 
                name = request.form['name'], 
                restaurant_id = restaurant_id,
                description = request.form['description'], 
                price = '${:,.2f}'.format(float(request.form['price'])),
                user_id = user["id"],
                course_name = request.form['course']
            )
            
            # Inform the user
            flash("New menu item created!", "alert-success")
        
        # Redirects to the new area
        return redirect( url_for('showmenu', restaurant_id = restaurant_id) )
    else:
        # Render template
        return render_template(
            'newMenuItem.html', 
            restaurant = restaurant, 
            courses = courses,
            token = antiForgeryGenToke(),
            username = user['name'],
            user_picture = user['picture'] 
        )


# Edit menu item
@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit", methods=['GET','POST'])
@authRequired
def editMenuItem(restaurant_id, menu_id):
    # Get user info for the user menu
    user = userData.getCurrentUserInfo()

    # Fetches the context item
    item = db.getRestaurantMenuItem( menu_id )
    
    # Checks whether the user has access to this content
    if not allowAccess( item.user_id, user["id"] ):
        # Inform the user
        output = "You are not authorized to edit menu items to %s restaurant. Please create your own restaurant in order to edit items." % restaurant.name
        flash(output, "alert-danger")
        # Redirects to the new area
        return redirect( url_for('showmenu', restaurant_id = restaurant_id) )

    # Fetches all courses type    
    courses = db.getAllCourses()

    if request.method == 'POST':

        if validateStateToke( request.form['csrf'] ):

            money = request.form['price']
            value = Decimal(sub(r'[^\d.]', '', money))
            name = request.form['name']
            
            db.updateRestaurantMenuItem(
                item,
                name = name,
                description = request.form['description'],
                price = '${:,.2f}'.format(float(value)),
                course_name = request.form['course'],
            )
            
            # Inform the user
            output = "%s menu item edited!" % name
            flash( output, "alert-success" )

        # Redirects to the new area
        return redirect(url_for('showmenu', restaurant_id = restaurant_id))
    else:
        # Convert price to number
        item.price = Decimal(sub(r'[^\d.]', '', item.price))
        # Render template
        return render_template(
            'editMenuItem.html', 
            restaurant_id = restaurant_id, 
            menu_id = menu_id, 
            item = item, 
            courses = courses,
            token = antiForgeryGenToke(),
            username = user['name'],
            user_picture = user['picture'] 
        )


# Delete menu item
@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete", methods=['GET','POST'])
@authRequired
def deleteMenuItem(restaurant_id, menu_id):
    # Get user info for the user menu
    user = userData.getCurrentUserInfo()
    
    # Fetches the context item
    item = db.getRestaurantMenuItem( menu_id )
    
    # Checks whether the user has access to this content
    if not allowAccess( item.user_id, user["id"] ):
        # Inform the user
        output = "You are not authorized to delete menu item to %s. Please create your own restaurant in order to delete items." % item.name
        flash(output, "alert-danger")
        # Redirects to the new area
        return redirect( url_for('showmenu', restaurant_id = restaurant_id) )

    if request.method == 'POST':
        if validateStateToke( request.form['csrf'] ):
            # Deleting item
            db.deleteRestaurantMenuItem( item )

            # Inform the user
            output = "%s menu item deleted!" % item.name
            flash(output, "alert-success")

        # Redirects to the new area
        return redirect(url_for('showmenu', restaurant_id = restaurant_id))
    else:
        # Render template
        return render_template(
            'deleteMenuItem.html', 
            restaurant_id = restaurant_id, 
            menu_id = menu_id, 
            item = item, 
            token = antiForgeryGenToke(),
            username = user['name'],
            user_picture = user['picture'] 
        )