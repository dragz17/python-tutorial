from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class webRequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith('/restaurants'):
				session = connectDB()
				restaurants = session.query(Restaurant).all()
				output = ""
				output += "<html><body>"
				output += "<a href='/restaurant/new'>Make a new Restaurant</a>"
				output += "</br>"
				for restaurant in restaurants:
					output += "<h2>"
					output += restaurant.name
					output += "</h2>"
					output += "<a href='/restaurant/%d/edit'>Edit</a>" % restaurant.id
					output += "</br>"
					output += "<a href='/restaurant/%d/delete'>Delete</a>" % restaurant.id
					output += "</br>"
				output += "</body></html>"
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				self.wfile.write(output.encode())
				print(output)
			if self.path.endswith('/restaurant/new'):
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h2> Add new Restaurant to list</h2>"
				output += """<form method='POST' action='/restaurant/new' enctype='multipart/form-data'>
							<input name='name' type='text'><input value='Add' type='submit'>
							</form>"""
				output += "</body></html>"
				self.wfile.write(output.encode())
				print(output)
			if self.path.endswith('/edit'):
				restaurantid = int(self.path.split("/")[2])
				session = connectDB()
				restaurant = session.query(Restaurant).filter_by(id = restaurantid).one()
				output = ""
				output += "<html><body>"
				output += "<h2>%s</h2>" % restaurant.name
				output += """<form method='POST', action='/edit' enctype='multipart/form-data'>
							<input type='text' placeholder=%s name='newName'>
							<input type='submit' value='Edit'>
							<input type='hidden' value=%d name='id'>
							</form>""" % (restaurant.name,restaurantid)
				output += "</body></html>"
				self.send_response(200)
				self.send_header('Content-type','text/html')
				self.end_headers()
				self.wfile.write(output.encode())
			if self.path.endswith('/delete'):
				restaurantid = int(self.path.split("/")[2])
				session = connectDB()
				restaurant = session.query(Restaurant).filter_by(id = restaurantid).one()
				output = ""
				output += "<html><body>"
				output += "<h2> Are you sure you want to delete %s?</h2>" % restaurant.name
				output += """<form method='POST' action='restaurant/%d/delete' enctype='multipart/form-data'>
							<input type='submit' value='Yes!!Delete it'>
							</form>""" % restaurantid
				output += "</body></html>"
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				self.wfile.write(output.encode())	
		except IOError:
			print("404 file path not found")

	def do_POST(self):
		if self.path.endswith('/restaurant/new') :
			ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
			pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
			if ctype == "multipart/form-data":
				fields = cgi.parse_multipart(self.rfile, pdict)
			restaurantName = fields.get('name')
			#add to database
			session = connectDB()
			newRestaurant = Restaurant(name = restaurantName[0].decode('utf-8'))
			session.add(newRestaurant)
			session.commit()

			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.send_header('Location', '/restaurants')
			self.end_headers()
				
		if self.path.endswith('/edit'):
			ctype,pdict = cgi.parse_header(self.headers.get('content-type'))
			pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
			if ctype == 'multipart/form-data':
				fields = cgi.parse_multipart(self.rfile, pdict)
			newName = fields.get('newName')[0].decode('utf-8')
			restaurantid = int(fields.get('id')[0].decode('utf-8'))
			session = connectDB()
			restaurant = session.query(Restaurant).filter_by(id = restaurantid).one()
			restaurant.name = newName
			session.add(restaurant)
			session.commit()

			self.send_response(301)
			self.send_header('Content-type','text/html')
			self.send_header('Location','/restaurants')
			self.end_headers()

		if self.path.endswith('/delete'):
			restaurantid = int(self.path.split("/")[2])
			session = connectDB()
			restaurant = session.query(Restaurant).filter_by(id = restaurantid).one()
			session.delete(restaurant)
			session.commit()

			self.send_response(301)
			self.send_header('Content-type','text/html')
			self.send_header('Location','/restaurants')
			self.end_headers()
#Method to connect to database
def connectDB():
	engine = create_engine('sqlite:///restaurantmenu.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind = engine)
	return DBSession()

def main():
	try:
		port = 8080
		server = HTTPServer(('',port),webRequestHandler)
		print("Starting server on port %d" % port)
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()
		print('^C pressed, stopped server')
	

if __name__ == '__main__':
	main()