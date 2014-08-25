import urllib
import urllib2
import webapp2

from base_email import *
from send_grid_account_info import *

class SendGridEmail(BaseEmail):

	URL = "https://api.sendgrid.com/api/mail.send.json"

	def send_email(self):
		values = {
			"api_user" : API_USER,
        	"api_key" : API_KEY,
        	"to" : self.addressee_email,
        	"toname" : self.to_name,
        	"subject" : self.subject,
        	"text" : self.message,
        	"from" : self.sender_email }

		data = urllib.urlencode(values)
		req = urllib2.Request(self.URL, data)
		response = urllib2.urlopen(req)
		return response
