from base_email import *

class MailgunEmail(BaseEmail):

	def __init__(self, request):
		super(MailgunEmail, self).__init__()

		self.data['to'] = cgi.escape(request.get("addressee_email"))
		self.data['subject'] = cgi.escape(request.get("subject"))
		self.data['text'] = cgi.escape(request.get("message"))
		self.data['from'] = 'postmaster@' + MAILGUN_SUBDOMAIN

		# Test URl to see POST request data
		# self.url = 'http://bin.mailgun.net/157be06f'
		self.url = 'https://api.mailgun.net/v2/' + MAILGUN_SUBDOMAIN + '/messages'	

		self.required = {'to' : True, 'subject' : True, 'text' : True, 'from' : True}

		self.set_up_auth()

	def set_up_auth(self):
		# create a password manager
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

		# Add the username and password.
		password_mgr.add_password(None, self.url, 'api', MAILGUN_API_KEY)
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)

		# Create "opener" (OpenerDirector instance)
		opener = urllib2.build_opener(handler)

		# Use the opener to fetch a URL
		# This is commented out because calling it results in an HTTP Error 405
		# opener.open(self.url)

		# Install the opener.
		urllib2.install_opener(opener)