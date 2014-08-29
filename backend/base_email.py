import cgi
import webapp2

from abc import ABCMeta, abstractmethod
from request import *

class BaseEmail(object):
	"""Abstract email class.

	This is a stub class to encapsulate some of the data properties
	and functionality that an email class needs to send an email via
	a third party API. This should be extended by other email classes
	that provide the details to send an HTTP POST request via a specific
	third party's API (SendGrid, Mailgun, etc.)

	Attributes:
		data: The data in the POST request, such as addressee email, subject, message body, etc.
		url: The url we're making the POST request to
		required: A hash of required data that needs to be part of the request as specified by the API
		auth: Optional HTTP authentication info such as username/password
	"""
	__metaclass__ = ABCMeta

	@abstractmethod
	def __init__(self):
		"""Initialize BaseEmail with all empty attributes"""
		self.data = {}
		self.url = ''
		self.required = {}
		self.auth = ()
		pass

	def prune_data(self):
		"""Remove empty data from the request data if it's not required.

		Example, if 'cc' was an option, but no one was cc'ed, then remove that
		key from the data hash. Subclasses should specify what data is required
		for their respective API calls.

		Note: Currently every input in the email form is required, so this
		isn't really needed, but it could be useful in the future.
		"""
		for key in list(self.data.keys()):
			if not self.data[key] and key not in self.required:
				del self.data[key]

	def send_email(self):
		"""Send an email.

		Use the subclasses specified API to send an HTTP POST request
		to send an email.

		Returns:
			False if urllib2 raised an exception, otherwise the HTTP response
		"""
		self.prune_data()
		request = Request(self.url, self.data, self.auth)
		return request.send_request(Request.POST)
		

