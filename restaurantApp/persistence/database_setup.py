import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from xml.etree.ElementTree import Element, SubElement, tostring

Base = declarative_base()

class User(Base):
	"""docstring for User"""

	__tablename__ = 'user'
	
	id = Column( Integer, primary_key = True )
	name = Column( String(260), nullable = False )
	email = Column( String(260), nullable = False )
	picture = Column( String(1000), nullable = True, default='/static/img/defaultUser.jpg')
	password = Column( String(260), nullable = False, default='pbkdf2:sha1:1000$0XYv4m0$8a2389bb391f92813706d48beb9c7ab7025fc452')
	
	@property
	def serialize(self):
		#Returns obect data in easily serializeable format
	    return {
	    	'picture' : self.picture,
	    	'email' : self.email,
	    	'name' : self.name,
	    	'id' : self.id
	    }

	@property
	def serialize_xml(self):
	    root = Element('user')

	    id_child= SubElement(root, 'id')
	    id_child.text = str(self.id)

	    name_child= SubElement(root, 'name')
	    name_child.text = self.name
	    
	    email_child= SubElement(root, 'email')
	    email_child.text = self.email

	    picture_child= SubElement(root, 'picture')
	    picture_child.text = self.picture

	    return root;


class Restaurant(Base):
	"""docstring for Restaurant"""

	__tablename__ = 'restaurant'
	
	id = Column( Integer, primary_key = True )
	name = Column( String(260), nullable = False )
	user_id = Column( Integer, ForeignKey('user.id') )
	picture = Column( String(1000), nullable = True, default='default.jpg')
	user = relationship(User)

	@property
	def serialize_json(self):
		#Returns obect data in easily serializeable format
	    return {
	    	'name' : self.name,
	    	'id' : self.id
	    }

	@property
	def serialize_xml(self):
	    root = Element('restaurant')

	    id_child= SubElement(root, 'id')
	    id_child.text = str(self.id)

	    name_child= SubElement(root, 'name')
	    name_child.text = self.name

	    return root;


class Course(Base):
	"""docstring for Course"""

	__tablename__ = 'course'

	name = Column( String(250), nullable = False, primary_key = True )
	
	@property
	def serialize_json(self):
		#Returns obect data in easily serializeable format
	    return {
	    	'name' : self.name
	    }

	@property
	def serialize_xml(self):
	    root = Element('course')

	    name_child= SubElement(root, 'name')
	    name_child.text = self.name

	    return root;


class MenuItem(Base):
	"""docstring for MenuItem"""
	
	__tablename__ = 'menu_item'

	name = Column( String(80), nullable = False )
	id = Column( Integer, primary_key = True )
	description = Column( String(250) )	
	price = Column( String(8) )
	course_name = Column( String(250), ForeignKey('course.name') )
	course = relationship(Course)
	restaurant_id = Column( Integer, ForeignKey('restaurant.id') )
	restaurant = relationship(Restaurant)
	user_id = Column( Integer, ForeignKey('user.id') )
	user = relationship(User)

	@property
	def serialize_json(self):
		#Returns obect data in easily serializeable format
	    return {
	    	'name' : self.name,
	    	'description' : self.description,
	    	'id' : self.id,
	    	'price' : self.price,
	    	'course' : self.course_name
	    }

	@property
	def serialize_xml(self):
	    root = Element('menuitem')

	    id_child= SubElement(root, 'id')
	    id_child.text = str(self.id)

	    name_child= SubElement(root, 'name')
	    name_child.text = self.name
	    
	    description_child= SubElement(root, 'description')
	    description_child.text = self.description
	    
	    price_child= SubElement(root, 'price')
	    price_child.text = self.price

	    course_name_child= SubElement(root, 'course_name')
	    course_name_child.text = self.course_name

	    return root;


####### insert at end of file #######

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

Base.metadata.create_all(engine)
