from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

menuItems= session.query(MenuItem).filter_by(name = 'Veggie Burger')
for item in menuItems:
	print(item.restaurant.name)
	print(item.id)
	print(item.price)

print("Updating value")
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 1).one()
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()

menuItems= session.query(MenuItem).filter_by(name = 'Veggie Burger')
for item in menuItems:
	print(item.restaurant.name)
	print(item.id)
	print(item.price)