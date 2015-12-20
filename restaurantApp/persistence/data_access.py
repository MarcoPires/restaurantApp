# import CRUD Operations
from sqlalchemy import create_engine, desc, func
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User, Course

# bootstrap DB connection 
def connect(database='postgresql://catalog:catalog@localhost/catalog'):
    """Connect to the database.  Returns a database session."""
    try:
        engine = create_engine(database)
        Base.metadata.bind = engine
        DBSession = sessionmaker( bind = engine )
        session = DBSession()

        return session
    except:
        print("Error: Connection failed")


def closeConnection(session):
    """Close session with the database"""
    session.close()


def createUser(name, email, password = None, picture = None):
    """Create new user"""
    session = connect()
    
    newUser = User( name = name, email = email, password = password, picture = picture )

    session.add(newUser)
    session.commit()
    closeConnection(session)

    return getUserByEmail( email )


def getUserByEmail(email):
    """Receives email and returns one user"""
    try:
        session = connect()
        user = session.query(User).filter_by( email = email ).one()
        closeConnection(session)
        return user
    except:
        return None


def getUserById(id):
    """Receives id and returns one user"""
    session = connect()
    user = session.query(User).filter_by( id = id ).one()
    closeConnection(session)
    return user


def getAllRestaurants():
    """Returns all restaurants"""
    session = connect()
    restaurants = session.query(Restaurant).all()
    closeConnection(session)
    return restaurants


def getRestaurant(id):
    """Returns one restaurant"""
    session = connect()
    restaurant = session.query(Restaurant).filter_by( id = id ).one()
    closeConnection(session)
    return restaurant


def deleteRestaurant(restaurant):
    """Delete given restaurant"""
    session = connect()
    
    session.delete( restaurant )
    session.commit()
    
    closeConnection(session)


def updateRestaurant(restaurant, name = None, picture = None):
    """Update given restaurant"""
    session = connect()
    
    if name:
        restaurant.name = name
    if picture:
        restaurant.picture = picture
    
    session.add(restaurant)
    session.commit()
    
    closeConnection(session) 


def newRestaurant(name, user_id, file):
    """Create restaurant"""
    session = connect()
    
    # Save the new restaurant
    newRestaurant = Restaurant( name = name,
        user_id = user_id, picture = file )
    session.add(newRestaurant)
    session.commit()

    closeConnection(session)


def getAllRestaurantMenuItems(restaurant):
    """Returns all restaurant menu items"""
    session = connect()
    items = session.query(MenuItem).filter_by( restaurant_id = restaurant.id 
        ).order_by(desc(MenuItem.course_name))
    closeConnection(session)
    return items


def getRestaurantMenuItem(id):
    """Returns all restaurant menu items"""
    session = connect()
    item = session.query(MenuItem).filter_by( id = id ).one()
    closeConnection(session)
    return item


def getAllCourses():
    """Returns all courses"""
    session = connect()
    courses = session.query(Course).all()
    closeConnection(session)
    return courses


def getAllRestItemsByCourses(restaurant):
    """Returns restaurant course with menu items"""
    session = connect()

    courses = getAllCourses();
    for course in courses:
        course.menuItems = session.query(MenuItem).filter_by( restaurant_id = restaurant.id, 
            course_name = course.name )
        course.length = course.menuItems.count()
    
    closeConnection(session)
    return courses


def newRestaurantMenuItem(name, description, price, course_name, restaurant_id, user_id):
    """Create new restaurant menu item"""
    session = connect()
   
    # Save the new menu item
    newItem = MenuItem( 
        name = name, 
        restaurant_id = restaurant_id,
        description = description, 
        price = price,
        user_id = user_id,
        course_name = course_name
    )

    session.add(newItem)
    session.commit()

    closeConnection(session)


def updateRestaurantMenuItem(item, name = None, description = None, 
    price = None, course_name = None):
    """Update given restaurant"""
    session = connect()
    
    if name:
        item.name = name
    if description:
        item.description = description
    if price: 
        item.price = price
    if course_name:
        item.course_name = course_name

    session.add(item)
    session.commit()
    
    closeConnection(session)


def deleteRestaurantMenuItem(item):
    """Delete given menu item"""
    session = connect()
    
    session.delete( item )
    session.commit()
    
    closeConnection(session)


def newCourse(name):
    """Create new menu item course"""
    session = connect()
   
    # Save the new menu item course
    newCourse = Course( name = name )

    session.add(newCourse)
    session.commit()

    closeConnection(session)
