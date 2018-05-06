from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

restaurants = session.query(Restaurant).all()

for restaurant in restaurants:
	print(restaurant.name.encode())
	print(restaurant.id)
