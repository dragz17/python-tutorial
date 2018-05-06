from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

menuItems = session.query(MenuItem).all()
for item in menuItems:
	print(item.name)

print("Deleting tandoori chicken")

Chicken= session.query(MenuItem).filter_by(name = 'Tandoori Chicken').one()
session.delete(Chicken)
session.commit()

menuItems = session.query(MenuItem).all()
for item in menuItems:
	print(item.name)