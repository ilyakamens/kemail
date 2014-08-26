import webapp2
import json
import httplib

from backend.sendgrid_email import *

class DefaultHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(open('./frontend/emailform.html', 'r').read())

class EmailHandler(webapp2.RequestHandler):
    def post(self):
		
        # validate data...
        # if validation passes...

        s_g_email = SendGridEmail(self.request)
        reply = s_g_email.send_email()

        if reply.code == httplib.OK:
            response = "Your message was sent!"
        else:
            response = "Your message could not be sent at this time."


        self.response.write(response)

application = webapp2.WSGIApplication([
    ('/', DefaultHandler),
    ('/email', EmailHandler)
], debug=True)
