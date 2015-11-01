from flask import jsonify
from restaurantApp import app
from restaurantApp.persistence import data_access as db


# JSON APIs to view Restaurant Information
@app.route("/restaurants/JSON")
def showRestaurantsJSON(): 
    restaurants = db.getAllRestaurants()
    return jsonify( restaurants=[restaurant.serialize_json for restaurant in restaurants] )


@app.route("/restaurant/<int:restaurant_id>/JSON")
def showRestaurantJSON(restaurant_id):
    restaurant = db.getRestaurant( restaurant_id )
    return jsonify( restaurant.serialize_json )


@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON")
def menuItemJSON(restaurant_id, menu_id):
    item = db.getRestaurantMenuItem( menu_id )
    return jsonify( item.serialize_json )


@app.route("/restaurant/<int:restaurant_id>/menu/JSON")
def showMenuJSON(restaurant_id): 
    restaurant = db.getRestaurant( restaurant_id )
    items      = db.getAllRestaurantMenuItems( restaurant )
    return jsonify( MenuItems=[i.serialize_json for i in items] )


@app.route("/restaurants/menu/course/JSON")
def menuItemCoursesJSON(): 
    courses = db.getAllCourses()
    return jsonify( courses=[course.serialize_json for course in courses] )