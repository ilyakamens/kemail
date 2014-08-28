import urllib2

from account_info import MAILGUN_SUBDOMAIN, MAILGUN_SUBDOMAIN, MAILGUN_API_KEY
from base_email import *

class MailgunEmail(BaseEmail):

	def __init__(self, request):
		super(MailgunEmail, self).__init__()

		self.data['to'] = cgi.escape(request.get("addressee_email"))
		self.data['subject'] = cgi.escape(request.get("subject"))
		self.data['text'] = cgi.escape(request.get("message"))
		# Emails won't sent if not from this addres... due to free account
		self.data['from'] = 'postmaster@' + MAILGUN_SUBDOMAIN

		# Test URl to see POST request data
		# self.url = 'http://bin.mailgun.net/157be06f'
		self.url = 'https://api.mailgun.net/v2/' + MAILGUN_SUBDOMAIN + '/messages'	

		self.required = {'to' : True, 'subject' : True, 'text' : True, 'from' : True}

		self.auth = ('api', MAILGUN_API_KEY)