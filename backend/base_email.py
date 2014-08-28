import cgi
import webapp2

from abc import ABCMeta, abstractmethod
from request import *

class BaseEmail(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def __init__(self):
		self.data = {}
		self.url = ''
		self.required = {}
		self.auth = ()
		pass

	def prune_data(self):
		for key in list(self.data.keys()):
			if not self.data[key] and key not in self.required:
				del self.data[key]

	def send_email(self):
		self.prune_data()
		request = Request(self.url, self.data, self.auth)
		return request.send_request(Request.POST)
		

