import cgi

from abc import ABCMeta, abstractmethod

class BaseEmail(object):
	__metaclass__ = ABCMeta

	UNKNOWN = "Unknown"

	#def __init__(self, addressee_email, message, sender_email=self.UNKNOWN, to_name=self.UNKNOWN, subject='No Subject'):
	def __init__(self, request):
		# Mandatory data
		self.addressee_email = cgi.escape(request.get("addressee_email"))
		self.message = cgi.escape(request.get("message"))

		# Optional data, so we set default values if needed
		self.sender_email = cgi.escape(request.get("sender_email"))
		if not self.sender_email:
			#self.sender_email = "ilyakamens@appspot.gserviceaccount.com"
			self.sender_email = self.UNKNOWN

		self.to_name = cgi.escape(request.get("to_name"))
		if not self.to_name:
			self.to_name = self.UNKNOWN

		self.subject = cgi.escape(request.get("subject"))
		if not self.subject:
			self.subject = "No Subject"

	@abstractmethod
	def send_email(self):
		pass

