from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restuarantmenu.db')
Base.metadata.bind = engine #Makes connection between class data and database table
DBSession = sessionmaker(bind = engine) #link of communication between code and engine
#all commands we want to execute are collected and sent to database when we execute commit
session = DBSession()
myFirstRestaurant = Restaurant(name="PizzaMaker")
session.add(myFirstRestaurant)
session.commit()
myMenuItem = MenuItem(name = "Pizza", description = "Tasty Pizza",
	course = "Entree", price = "$5.66", restaurant = myFirstRestaurant)
session.add(myMenuItem)
session.commit()