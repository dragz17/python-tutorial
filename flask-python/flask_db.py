from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

def getSession():
	engine = create_engine('sqlite:///restaurantmenu.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind = engine)
	return DBSession()

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	session = getSession()
	restro = session.query(Restaurant).filter_by(id = restaurant_id).first()
	menuitems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html', menuitems = menuitems, restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/new', methods = ['GET','POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
	   	newMenuItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
	   	session = getSession()
	   	session.add(newMenuItem)
	   	session.commit()
	   	flash('New menu item has been added')
	   	return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
   		return render_template('newItem.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
    	editedMenuItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
    	session = getSession()
    	session.add(editedMenuItem)
    	session.commit()
    	flash('Menu item edited')
    	return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
    	session = getSession()
    	originaleMenuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    	return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, menuName = originaleMenuItem.name)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	if request.method == 'POST':
		session = getSession()
		deleteItem = session.query(MenuItem).filter_by(id = menu_id).first()
		session.delete(deleteItem)
		session.commit()
		flash('Menu item deleted')
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		session = getSession()
		originaleMenuItem = session.query(MenuItem).filter_by(id = menu_id).one()
		return render_template('deletemenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, menuitem = originaleMenuItem)

#API endpoints designing
@app.route('/restaurants/<int:restaurant_id>/menu/json/')
def restaurantMenuJson(restaurant_id):
	session = getSession()
	menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return jsonify(MenuItems = [i.serialize for i in menuItems])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/json/')
def menuJson(restaurant_id, menu_id):
	session = getSession()
	menuItem = session.query(MenuItem).filter_by(id = menu_id).first()
	return jsonify(MenuItems = menuItem.serialize)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)

