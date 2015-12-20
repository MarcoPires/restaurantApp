import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
	"""docstring for Restaurant"""

	__tablename__ = 'restaurant'

	id = Column( Integer, primary_key = True )
	name = Column( String(260), nullable = False )


class MenuItem(Base):
	"""docstring for MenuItem"""

	__tablename__ = 'menu_item'

	name = Column( String(80), nullable = False )
	id = Column( Integer, primary_key = True )
	description = Column( String(250) )
	price = Column( String(8) )
	course = Column( String(250) )
	restaurant_id = Column( Integer, ForeignKey('restaurant.id') )
	restaurant = relationship(Restaurant)



####### insert at end of file #######

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')

Base.metadata.create_all(engine)
