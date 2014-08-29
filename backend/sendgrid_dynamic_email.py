from account_info import SENDGRID_API_USER, SENDGRID_API_KEY
from base_email import *

class SendgridDynamicEmail(BaseEmail):
	"""Email class to send emails via SendGrid's API

	This class encapsulates the SendGrid-specific data needed
	to send an HTTP request to SendGrid (i.e. to send an email via their API)
	"""

	def __init__(self, request, user):
		"""Initialize this class with all the SendGrid-specific data needed
		to send an email using their service.

		Specifically, parse out the desired email data sent to us from the user,
		add the destination URL, and specify what data is required for the POST request.
		"""
		super(SendgridDynamicEmail, self).__init__()

		self.data['api_user'] = SENDGRID_API_USER
		self.data['api_key'] = SENDGRID_API_KEY
		self.data['to'] = cgi.escape(request.get("addressee_email"))
		self.data['subject'] = cgi.escape(request.get("subject"))
		self.data['text'] = cgi.escape(request.get("message"))
		self.data['from'] = user.email()
		self.data['toname'] = cgi.escape(request.get("to_name"))

		self.url = "https://api.sendgrid.com/api/mail.send.json"

		self.required = {'to' : True, 'subject' : True, 'text' : True, 'from' : True}

