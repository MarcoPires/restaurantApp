from restaurantApp import app
from restaurantApp.persistence import data_access as db
from flask import make_response
from xml.etree.ElementTree import tostring, Element, SubElement
from xml.dom import minidom


# XML APIs to view Restaurant Information
@app.route("/restaurants/XML")
def showRestaurantsXML(): 
    restaurants = db.getAllRestaurants()

    xml = Element('restaurants')
    for restaurant in restaurants:
        xml.append(restaurant.serialize_xml)

    return xmlResponse(xml)


@app.route("/restaurant/<int:restaurant_id>/XML")
def showRestaurantXML(restaurant_id):
    restaurant = db.getRestaurant( restaurant_id )
    return xmlResponse( restaurant.serialize_xml )


@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/XML")
def menuItemXML(restaurant_id, menu_id): 
    item = db.getRestaurantMenuItem( menu_id )
    return xmlResponse( item.serialize_xml )


@app.route("/restaurant/<int:restaurant_id>/menu/XML")
def showMenuXML(restaurant_id): 
    restaurant = db.getRestaurant( restaurant_id )
    items      = db.getAllRestaurantMenuItems( restaurant )
    
    xml = Element('restaurant')
    xml.set('id', str(restaurant.id))
    xml.set('name', restaurant.name)
    for item in items:
        xml.append(item.serialize_xml)

    return xmlResponse(xml)


@app.route("/restaurants/menu/course/XML")
def menuItemCoursesXML(): 
    courses = db.getAllCourses()
    
    xml = Element('restaurants')
    child = SubElement(xml, 'courses')
    for course in courses:
        child.append(course.serialize_xml)

    return xmlResponse(xml)


#XML helpers
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def xmlResponse(xml):
    xml.set('version', '1.0')
    response = make_response(prettify(xml))
    response.mimetype = "text/xml"
    response.headers['Content-type'] = 'text/xml; charset=utf-8'
    return response