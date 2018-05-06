import webapp2
import jinja2
import os 

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class MainPage(Handler):
	def get(self):
		t = jinja_env.get_template('index.html')
		self.response.write(t.render(var = "Hello World"))

app = webapp2.WSGIApplication([('/',MainPage)], debug = True)