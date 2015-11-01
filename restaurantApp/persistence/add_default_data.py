from restaurantApp.persistence import data_access as db

user = db.getUserByEmail("marcofspires@gmail.com")
if not user:
	from restaurantApp.persistence import lotsofmenus
	print "-------------> DEFAULT DATA"