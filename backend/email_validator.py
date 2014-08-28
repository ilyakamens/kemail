import json
import cgi
import webapp2

from request import *
from account_info import MAILGUN_PUB_API_KEY

class EmailValidator(Request):

	VALIDATION_URL = "https://api.mailgun.net/v2/address/validate"

	def __init__(self, request):
		super(EmailValidator, self).__init__(self.VALIDATION_URL,
											{'address' : cgi.escape(request.get("addressee_email"))},
											('api', MAILGUN_PUB_API_KEY))
	
	def is_valid_email(self):
		http_response = self.send_request(Request.GET)
		if http_response:
			api_response = json.loads(http_response.read())
			return api_response['is_valid'], api_response['address'], api_response['did_you_mean']

		return http_response, None, None