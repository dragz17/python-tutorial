from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from io import BytesIO

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith('/hello'):
				#Sending header
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output +="<html><body>Hello!!"
				output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                       <h2>What would you like me to say?</h2><input name='message' type='text'>
                       <input type='submit' value='Submit'></form>"""
				output+="</body></html>"
				self.wfile.write(output.encode()) #Send response to client
				print(output)
				return
			if self.path.endswith('/hola'):
				#Sending header
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output +="<html><body>Hola!!"
				output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
                       <h2>What would you like me to say?</h2><input name='message' type='text'>
                       <input type='submit' value='Submit'></form>"""
				output+="</body></html>"
				self.wfile.write(output.encode()) #Send response to client
				print(output)
				return

		except IOError:
			print("404 Not Found!s")
	def do_POST(self):
		try:
			self.send_response(301)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			#gets type and paramater dictionary of HTML form headers
			ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
			pdict['boundary'] = bytes(pdict['boundary'], "utf-8") #required to use cgi in python 3
			if ctype == "multipart/form-data":
				fields = cgi.parse_multipart(self.rfile, pdict)
				messagecontent = fields.get('message')
			output = ""
			output += "<html><body>"
			output += "<h2> Okay how about this </h2>"
			output += "<h1> %s </h1>" % messagecontent[0]
			output += """<form method='POST' enctype='multipart/form-data' action='/hello'>
			<h2>What would you like me to say?</h2><input name='message' type='text'>
			<input type='submit' value='Submit'></form>"""
			output += "</body></html>"
			self.wfile.write(output.encode())
			print(output)

		except Exception as e:
			raise

def main():
	try:
		port = 8080
		server = HTTPServer(('',port),webserverHandler)
		print("The server is running on port",port)
		server.serve_forever()

	except KeyboardInterrupt:
		print('^C pressed, stopping server')
		server.socket.close()

if __name__ == '__main__':
	main()
