from account_info import MAILGUN_SUBDOMAIN, MAILGUN_SUBDOMAIN, MAILGUN_API_KEY
from base_email import *

class MailgunDynamicEmail(BaseEmail):
	"""Email class to send emails via Mailgun's API

	This class encapsulates the Mailgun-specific data needed
	to send an HTTP request to Mailgun (i.e. to send an email via their API)
	"""

	def __init__(self, request, user):
		"""Initialize this class with all the Mailgun-specific data needed
		to send an email using their service.

		Specifically, parse out the desired email data sent to us from the user,
		add the destination URL, the authentication info, and specify what data
		is required for the POST request.

		Note that because of my free account, the sender email must be from
		their subdomain and is consequently hard-coded below.
		"""
		super(MailgunDynamicEmail, self).__init__()

		self.data['to'] = cgi.escape(request.get("addressee_email"))
		self.data['subject'] = cgi.escape(request.get("subject"))
		self.data['text'] = cgi.escape(request.get("message"))
		# Emails won't sent if not from this addres... due to free account
		self.data['from'] = 'postmaster@' + MAILGUN_SUBDOMAIN

		# Test URl to see our request data
		# self.url = 'http://bin.mailgun.net/157be06f'
		self.url = 'https://api.mailgun.net/v2/' + MAILGUN_SUBDOMAIN + '/messages'	

		self.required = {'to' : True, 'subject' : True, 'text' : True, 'from' : True}

		self.auth = ('api', MAILGUN_API_KEY)