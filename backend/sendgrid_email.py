from base_email import *

class SendGridEmail(BaseEmail):

	def __init__(self, request):
		super(SendGridEmail, self).__init__()

		self.data['api_user'] = SENDGRID_API_USER
		self.data['api_key'] = SENDGRID_API_KEY
		self.data['to'] = cgi.escape(request.get("addressee_email"))
		self.data['subject'] = cgi.escape(request.get("subject"))
		self.data['text'] = cgi.escape(request.get("message"))
		self.data['from'] = 'potato'
		self.data['toname'] = cgi.escape(request.get("to_name"))

		self.url = "https://api.sendgrid.com/api/mail.send.json"

		self.required = {'to' : True, 'subject' : True, 'text' : True, 'from' : True}

