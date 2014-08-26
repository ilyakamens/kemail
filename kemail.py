import webapp2
import json
import httplib

from backend.emailer import *

class DefaultHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(open('./frontend/emailform.html', 'r').read())

class EmailHandler(webapp2.RequestHandler):
    def post(self):
		
        # validate data...
        # if validation passes...

        if Emailer.send_email(self.request):
            message = "Your message was sent!"
        else:
            message = "Your message could not be sent at this time."


        self.response.write(message)

application = webapp2.WSGIApplication([
    ('/', DefaultHandler),
    ('/email', EmailHandler)
], debug=True)
