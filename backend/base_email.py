import urllib
import urllib2
import cgi
import webapp2

from abc import ABCMeta, abstractmethod
from account_info import *

class BaseEmail(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def __init__(self):
		self.data = {}
		self.url = ''
		self.required = {}
		pass

	def prune_data(self):
		for key in list(self.data.keys()):
			if not self.data[key] and key not in self.required:
				del self.data[key]

	def send_email(self):
		self.prune_data()
		print
		print self.data
		print
		data = urllib.urlencode(self.data)
		req = urllib2.Request(self.url, data)
		response = urllib2.urlopen(req)
		return response

