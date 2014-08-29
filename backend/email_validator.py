import json

from request import *
from account_info import MAILGUN_PUB_API_KEY

class EmailValidator(Request):
	"""Class to validate email addresses.

	Uses Mailgun's email validation API to validate addressee
	emails, and can even make smart suggestions if the emails
	aren't valid.

	Attributes:
		VALIDATION_URL: Class attribute that just a reference to Mailgun's URL for email validation
	"""

	# URL for Mailgun's email validation
	VALIDATION_URL = "https://api.mailgun.net/v2/address/validate"

	def __init__(self, request):
		"""Initializes EmailValidator and passes the necessary information,
		such as the URL, request data, and authentication data to the super class.

		Args:
			request: An instance of Google's Request class (https://developers.google.com/appengine/docs/python/tools/webapp/requestclass)
		"""

		super(EmailValidator, self).__init__(self.VALIDATION_URL,
											{'address' : request.get("addressee_email")},
											('api', MAILGUN_PUB_API_KEY))
	
	def is_valid_email(self):
		"""Determines if this instance's email address is valid.

		Determines if the given email address is valid using Mailgun's
		API. This can sometimes provide suggestions if a bit of syntax is off
		or if the domain name is misspelled.

		Returns:
			If the HTTP response came back without issue, return a 3 item tuple containing an
			indication if the email was valid, the email address we were validating, and a possible
			suggestion if the email address was invalid. Not that there can still be a suggestion even
			if the email address was syntactically valid if Mailgun thinks there's a typo. Example:

			(False, example@gmailcom, example@gmail.com)

			If there was an issue with the HTTP request and we didn't get a normal response,
			then return:

			(False, None, None)

			Note that although we return http_response instead of explicitly False, we know
			send_request() returns False in this case.
		"""
		
		http_response = self.send_request(Request.GET)
		if http_response:
			api_response = json.loads(http_response.read())
			return api_response['is_valid'], api_response['address'], api_response['did_you_mean']

		return http_response, None, None